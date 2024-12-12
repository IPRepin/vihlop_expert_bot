import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from pydantic import ValidationError

from data.db_connect import get_session
from data.user_requests import get_all_users
from keyboards.admin_keyboards.main_admin_keyboards import get_confirm_button, confirm_keyboard, add_mailing_button, \
    admin_keyboards
from utils.logging_settings import setup_logging
from utils.states import MailingState

logger = logging.getLogger(setup_logging())

admin_mailing_router = Router()


@admin_mailing_router.message(F.text == "📨Отправить рассылку")
async def admin_mailing_handler(message: Message, state: FSMContext):
    await message.answer("Добавьте текст рассылки")
    await state.set_state(MailingState.MAIL_TEXT)


@admin_mailing_router.message(MailingState.MAIL_TEXT)
async def add_button_choice(message: Message, state: FSMContext):
    await state.update_data(mailing_text=message.text,
                            message_id=message.message_id,
                            chat_id=message.from_user.id)
    await state.set_state(MailingState.ADD_BUTTON)
    await message.answer("Добавить кнопку к рассылке?",
                         reply_markup=await get_confirm_button())


@admin_mailing_router.callback_query(MailingState.ADD_BUTTON,
                                     F.data.in_(['add_mailing_button',
                                                 'no_mailing_button', ], ), )
async def add_button_mailing(callback_query: CallbackQuery,
                             state: FSMContext,
                             ):
    if callback_query.data == 'add_mailing_button':
        await callback_query.message.answer("Введи текст кнопки, например\n"
                                            "🤗Подписаться", reply_markup=None)
        await state.set_state(MailingState.BUTTON_TEXT)
    elif callback_query.data == 'no_mailing_button':
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer("Добавь фото к рассылке")
        await state.set_state(MailingState.ADD_MEDIA)
    await callback_query.answer()


@admin_mailing_router.message(MailingState.BUTTON_TEXT)
async def get_text_button(message: Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer("Теперь добавь ссылку для кнопки, например\n"
                         "https://ya.ru/",
                         disable_web_page_preview=True)
    await state.set_state(MailingState.BUTTON_URL)


@admin_mailing_router.message(MailingState.BUTTON_URL)
async def get_url_button(message: Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    await state.set_state(MailingState.ADD_MEDIA)
    await message.answer("Добавь фото к рассылке")


async def confirm(
        message: Message,
        bot: Bot,
        photo_id: str,
        message_text: str,
        chat_id: int,
        reply_markup: InlineKeyboardMarkup = None,
):
    await bot.send_photo(chat_id=chat_id,
                         photo=photo_id,
                         caption=message_text,
                         reply_markup=reply_markup)
    await message.answer("Вот рассылка которая будет оправлена\n"
                         "Подтвердить отрпавку.",
                         reply_markup=await confirm_keyboard()
                         )


@admin_mailing_router.message(MailingState.ADD_MEDIA, F.photo)
async def sending_mailing(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    message_text = data.get("mailing_text")
    chat_id = int(data.get("chat_id"))
    photo_id = data.get("photo")
    await confirm(message=message,
                  bot=bot,
                  photo_id=photo_id,
                  message_text=message_text,
                  chat_id=chat_id)


async def send_mails(
        photo: str,
        mailing_text: str,
        bot: Bot,
        button_message
):
    async for session in get_session():
        users = await get_all_users(session)
        for user in users:
            try:
                await bot.send_photo(chat_id=user.user_id,
                                     photo=photo,
                                     caption=mailing_text,
                                     reply_markup=button_message)
                await asyncio.sleep(0.5)
            except TelegramRetryAfter as e:
                logger.error(e)
                await asyncio.sleep(e.retry_after)
                await bot.send_photo(chat_id=user.user_id,
                                     photo=photo,
                                     caption=mailing_text,
                                     reply_markup=button_message)


@admin_mailing_router.callback_query(F.data.in_(['confirm_mailing',
                                                 'cancel_mailing', ], ),
                                     )
async def sender_mailing(
        call: CallbackQuery,
        bot: Bot,
        state: FSMContext,
):
    if call.data == 'confirm_mailing':
        data = await state.get_data()
        await state.clear()
        photo = data.get('photo')
        mailing_text = data.get('mailing_text')
        button_text = data.get('button_text')
        button_url = data.get('button_url')
        try:
            button_message =await add_mailing_button(
                text_button=button_text,
                url_button=button_url,
            )
        except ValidationError as error:
            logger.info(error)
            button_message = None
        try:
            await call.message.answer("К сожалению телеграм имеет ограничения "
                                      "на отправку сообщений "
                                      "поэтому отправка может занять некоторое время.\n"
                                      "Дождитесь уведомления об успешной отправке")
            await send_mails(
                photo,
                mailing_text,
                bot,
                button_message
            )
            await call.message.answer("Рассылка отправлена")
        except TelegramBadRequest as e:
            logger.error(e)
            await call.message.answer(f"Ошибка при отправке рассылки {e}"
                                      ",\nпопробуйте создать новую рассылку",
                                      reply_markup=await admin_keyboards())
    else:
        await state.clear()
        await call.message.answer("Вы отменили рассылку")
    await call.answer()
    await call.message.answer("Главное меню", reply_markup=await admin_keyboards())


@admin_mailing_router.message(MailingState.ADD_MEDIA, ~F.photo)
async def incorrect_mailing_photo(message: Message, state: FSMContext) -> None:
    await message.answer("Нужно загрузить фотографию!")
