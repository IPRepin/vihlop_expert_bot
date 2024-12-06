import re

def is_valid_phone(phone: str) -> bool:
    # Регулярное выражение для проверки российских номеров с учетом скобок, дефисов и пробелов
    pattern = r"^(?:\+7|8)?[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"
    return bool(re.fullmatch(pattern, phone))


def clean_phone_number(phone: str) -> str:
    # Удаляем все лишние символы из номера перед сохранением
    clean_phone = re.sub(r"[^\d]", "", phone)
    if clean_phone.startswith("8"):
        clean_phone = "+7" + clean_phone[1:]  # Приводим номера, начинающиеся с "8", к формату "+7"
        return clean_phone

