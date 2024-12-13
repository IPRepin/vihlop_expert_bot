'''
Модуль содержит дополнительный функционал для работы с ботом
'''
import csv
from datetime import datetime


def new_file(data, query):
    name_file = datetime.now().strftime('%d-%m-%Y')
    with open(f'data/{query}_{name_file}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # Записываем заголовки
        writer.writerow(["id", "user_id", "user_name", "user_email", "user_url"])
        # Преобразуем объекты User в строки CSV
        for user in data:
            writer.writerow([user.id, user.user_id, user.user_name, user.user_email, user.user_url])
