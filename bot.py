from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, FIRST_TYPE, SECOND_TYPE, HELP, JSONE_EXAMPLE, CSV_EXAMPLE
from io import BytesIO
import pandas as pd
import numpy as np
import logging
import pickle
import json
import re

logging. basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

diabetes_type_info = "где\n" \
                     "0: наличие СД любого типа у пациента не обнаружено\n" \
                     "1: у пациента обнаружен СД 1-го типа\n" \
                     "2: у пациента обнаружен СД 2-го типа\n"


def msg2list(text_data: str) -> list:
    """
    Функция обрабатывает текст из сообщения, которое отправил пользователь.
    Возрвращает список ["признак1: значение", "признак2: значение", "признак3: значение" ...]
    :param text_data: str
    :return: list
    """

    text_data = text_data.lower()
    text_data = text_data.replace(" ", "")
    text_data = text_data.replace("\n", "")
    text_data = re.split(';|,', text_data)
    if text_data[-1] in ["", " "]:
        text_data = text_data[:-1]
    return text_data


def msg2df(text_data: list) -> pd.DataFrame:
    """
    Функция преобразует список ["признак1: значение", "признак2: значение", "признак3: значение" ...]
    в датафрейм.
    :param text_data: list
    :return: pd.DataFrame
    """

    df = {'hba1c': [], 'ubp': [], 'lbp': [], 'bmi': [],
          'age': [], 'glycemia': [], 'gender': [], 'insulin': []}
    for data in text_data:
        data = data.split(":")
        if data[0] not in df.keys():  # проверка правильно ли пользоватьль указал признаки
            raise ValueError("Ошибка в имени признака!")
        df[data[0]].append(float(data[1]))
    df = pd.DataFrame.from_dict(df)
    return df


def file2df(file_path: str, file: BytesIO) -> pd.DataFrame:
    """
    Функция преобразует файлы типа json или csv в датафрейм.
    :param file_path: str
    :param file: BytesIO
    :return: pd.DataFrame
    """

    df = None
    if file_path[-4:] == "json":
        df = json.load(file)
        df = pd.DataFrame.from_dict(df)
        df = pd.concat([df.apply(pd.Series)], axis=1)
    elif file_path[-3:] == "csv":
        df = pd.read_csv(file)
    else:
        raise TypeError("Неверное расширение файла!")  # если файл с каким-то другим расширением

    # проверка правильно ли пользоватьль указал признаки
    if df.columns.tolist() != ['HbA1C', 'UBP', 'LBP', 'BMI', 'AGE', 'Glycemia', 'Gender', 'Insulin']:
        raise ValueError("Ошибка в имени признака!")

    return df


def predict(df: pd.DataFrame) -> str:
    """
    Функция предсказывает сд у пациентов.
    Для предсказания используется RandomForest.
    :param df: pd.DataFrame
    :return: str
    """

    loaded_model = pickle.load(open('models/diabetes_model.sav', 'rb'))
    predicted = loaded_model.predict(df)
    predicted = predicted.tolist()
    predicted = ", ".join(map(str, predicted))  # например: 2, 1, 0, 2
    return predicted


def select_file_type(file_path: str, df: pd.DataFrame) -> tuple:
    """
    Функия преобразует датафрейм в файл того же формата, что отправлял пользователь.
    :param file_path: str
    :param df: pd.DataFrame
    :return: tuple
    """

    if file_path[-4:] == "json":
        return "result.json", df.to_json(orient="records").encode()
    elif file_path[-3:] == "csv":
        return "result.csv", df.to_csv(index=False).encode()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ помогу тебе определить наличие или отсутствие сахарного диабета у пациент(а/ов), "
                        "укажу его тип при наличии и дам рекомендации по лечению и профилактике. Более подробно с тем "
                        "как загружать и какие признаки указывать, ты можешь ознакомиться, если введешь команду /help")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_document(message.from_user.id, HELP,
                            reply_to_message_id=message.message_id)


@dp.message_handler(commands=['1type'])
async def process_1type_command(message: types.Message):
    caption = "Более подробную информацию можно найти здесь:\n" \
              "https://rae-org.ru/system/files/documents/pdf/saharnyy_diabet_1_tipa_u_vzroslyh.pdf"
    await bot.send_document(message.from_user.id, FIRST_TYPE,
                            caption=caption,
                            reply_to_message_id=message.message_id)


@dp.message_handler(commands=['2type'])
async def process_2type_command(message: types.Message):
    caption = "Более подробную информацию можно найти здесь:\n" \
              "https://rae-org.ru/system/files/documents/pdf/saharnyy_diabet_2_tipa_u_vzroslyh.pdf"
    await bot.send_document(message.from_user.id, SECOND_TYPE,
                            caption=caption,
                            reply_to_message_id=message.message_id)


@dp.message_handler(commands=['examplefiles'])
async def process_example_command(message: types.Message):
    await bot.send_document(message.from_user.id, CSV_EXAMPLE)
    await bot.send_document(message.from_user.id, JSONE_EXAMPLE)


@dp.message_handler()
async def process_text_command(message: types.Message):
    """
    Функция получает данные о пациентах в виде текстового сообщения и
    определяет для каждого из пациентов наличие сд.
    """

    text_data = msg2list(str(message.text))

    try:
        df = msg2df(text_data)
    except Exception as e:
        await message.reply("Ошибка в имени признака или значении! Проверьте правильность ввода.")
        return

    predicted = predict(df)

    await message.reply("Тип(ы) диабета: " + predicted)
    await message.answer(diabetes_type_info)


@dp.message_handler(content_types=['document'])
async def process_document_command(message: types.Message):
    """
    Функция получает данные о пациентах в виде файла формата csv или json и
    определяет для каждого из пациентов наличие сд.
    """
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    try:
        df = file2df(file_path, file)
    except Exception as e:
        await message.reply("Файл содержит некоректные данные или"
                            " имеет формат отличный от json и csv!")
        return

    predicted = predict(df)
    predicted = predicted.replace(" ", "")
    predicted = [int(x) for x in predicted.split(",")]

    df["Outcome"] = np.array(predicted)

    user_id = message.from_user.id
    file_type = select_file_type(file_path, df)
    await bot.send_document(user_id, file_type, caption=diabetes_type_info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
