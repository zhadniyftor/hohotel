import datetime

import telebot

import Take_info_Module as tim
import Take_photo_Module as tpm

bot = telebot.TeleBot("7092973112:AAEV6kO_FJcrikXXZjodLq6JVOmSeoKhkbQ")

information = {}
history_store = {}
list_of_hotels_for_history = []


@bot.message_handler(content_types=['text'])
def start(message):
    global information
    if message.text == '/bestdeal':
        information[message.from_user.id] = {"city": None, "count_of_hotel": 0, "adults": 0, "maxSum": 99999999999999,
                                             'children': [],
                                             "minSum": 1, "in_data": None,
                                             "out_data": None, "count_of_photo": 0, "status": None,
                                             "photo_status": None}
        bot.send_message(message.from_user.id, "В каком городе нужно найти отель (отели)? На английском языке ")

        # WHAT
        information[message.from_user.id]['status'] = message.text

        bot.register_next_step_handler(message, get_city)
        # следующий шаг – функция get_name
    elif message.text == '/lowprise':
        information[message.from_user.id] = {"city": None, "count_of_hotel": 0, "adults": 0, "maxSum": 99999999999999,
                                             "minSum": 1, "in_data": None,
                                             "out_data": None, "count_of_photo": 0, "status": None,
                                             "photo_status": None}
        information[message.from_user.id]['minSum'] = 1
        information[message.from_user.id]["maxSum"] = 99999999999999
        bot.send_message(message.from_user.id, "В каком городе нужно найти отель (отели) на английском языке? ")
        information[message.from_user.id]['status'] = message.text
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/highprice':
        information[message.from_user.id] = {"city": None, "count_of_hotel": 0, "adults": 0, "maxSum": 99999999999999,
                                             "minSum": 1, "in_data": None,
                                             "out_data": None, "count_of_photo": 0, "status": None,
                                             "photo_status": None}
        bot.send_message(message.from_user.id, "В каком городе нужно найти отель (отели) на английском языке? ")
        information[message.from_user.id]['minSum'] = 500
        information[message.from_user.id]["maxSum"] = 99999999999999
        information[message.from_user.id]['status'] = message.text
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/history':
        bot.send_message(message.from_user.id, "Сейчас посмотрим, что вы запрашивали...")
        print(history_store)
        if message.from_user.id in history_store:
            for user_id, nes in history_store.items():
                if user_id == message.from_user.id:
                    for hotels in nes:
                        print(hotels)
                        bot.send_message(message.from_user.id, hotels)
        else:
            bot.send_message(message.from_user.id, "Пока что в истории ничего нету(")
        bot.send_message(message.chat.id, "Это всё :)")
    else:
        bot.send_message(message.from_user.id, 'Вот такие команды я умею выполнять: \n'
                                               '/bestdeal\n'
                                               '/lowprise\n'
                                               '/highprice \n'
                                               '/history \n')


def get_city(message):
    global information
    information[message.from_user.id]['city'] = message.text
    bot.send_message(message.from_user.id, 'Сколько нужно вывести отелей?')
    bot.register_next_step_handler(message, get_count_of_hotels)
    print(information[message.from_user.id]['city'])


def get_count_of_hotels(message):
    global information
    if message.text.isdigit():
        information[message.from_user.id]["count_of_hotel"] = int(message.text)
        bot.send_message(message.from_user.id, "Сколько будет взрослых?")
        bot.register_next_step_handler(message, get_count_of_adults)
        print(information[message.from_user.id]["count_of_hotel"])
    else:
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста!!!")
        bot.register_next_step_handler(message, get_count_of_hotels)


def get_count_of_adults(message):
    global information
    if message.text.isdigit():
        if int(message.text) > 0:
            information[message.from_user.id]["adults"] = int(message.text)
            bot.send_message(message.from_user.id, "Будут ли дети с вами?")
            bot.register_next_step_handler(message, child_status)
            print(information[message.from_user.id]["adults"])
        else:
            bot.send_message(message.from_user.id, "Мало человеков!!!")
            bot.register_next_step_handler(message, get_count_of_adults)
    else:
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста!!!")
        bot.register_next_step_handler(message, get_count_of_adults)


def child_status(message):
    if message.text.lower() == "да":
        bot.send_message(message.from_user.id, "Ведите возраст детей, например: 1, 7, 10")
        bot.register_next_step_handler(message, children)
    else:
        bot.send_message(message.from_user.id, "Введите дату въезда (например: 01.01.1111) ")
        bot.register_next_step_handler(message, get_in_data)


def check_children(list_children):
    list_children = list_children.split(",")
    new_list_children = []
    for child in list_children:
        if child[0] == " ":
            child = child[1::]
        if child.isalpha() or child.isspace():
            return False, ''
        new_list_children.append(child)
    return True, new_list_children


def children(message):
    global information
    check = check_children(message.text)
    if check[0]:
        information[message.from_user.id]["children"] = check[1]
        bot.send_message(message.from_user.id, "Введите дату въезда (например: 01.01.1111) ")
        bot.register_next_step_handler(message, get_in_data)
        print(information[message.from_user.id]["children"])
    else:
        bot.send_message(message.from_user.id, "Некорректно ведён возраст!!!")
        bot.register_next_step_handler(message, children)


def check_data(data):
    data_for_normal_human = {1: 31, 2: [28, 29], 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30,
                             12: 31}
    try:
        data = data.split('.')
    except:
        pass
    try:
        if len(data) == 3:
            day = int(data[0])
            month = int(data[1])
            year = int(data[2])
            if year < 0:
                return False, "А ты походу в мезозое живёшь :)"
            elif year > datetime.datetime.now().year + 5:
                return False, "Для броньки рановато, замахнулся)"
            else:
                if year % 4 != 0 or year % 100 == 0 and year % 400 != 0:
                    if month in data_for_normal_human:
                        if month == 2:
                            if day <= data_for_normal_human[month][1] and day > 0:
                                return True, ''
                            else:
                                return False, "Я понимаю, дней не хватает, но столько нет дней в этом месяце :)"
                        if day <= data_for_normal_human[month] and day > 0:
                            print(data_for_normal_human[month])
                            return True, ''
                        else:
                            return False, "Я понимаю, дней не хватает, но столько нет дней в этом месяце! :)"
                    else:
                        return False, "Ты что!!! Нету столько месяцев в году!!! " \
                                      "Тебе надо отдохнуть, а я помогу, только дай мне верный месяц :)"
                else:
                    if month in data_for_normal_human:
                        if month == 2:
                            if day <= data_for_normal_human[month][0] and day > 0:
                                return True, ''
                            else:
                                return False, "Я понимаю, дней не хватает, но столько нет дней в этом месяце :)"
                        if day <= data_for_normal_human[month] and day > 0:
                            print(data_for_normal_human[month])
                            return True, ''
                        else:
                            return False, "Я понимаю, дней не хватает, но столько нет дней в этом месяце! :)"
                    else:
                        return False, "Ты что!!! Нету столько месяцев в году!!! " \
                                      "Тебе надо отдохнуть, а я помогу, только дай мне верный месяц :)"
        else:
            return False, "Дата есть дата, а это не дата!!! И я ещё тебя не понимаю!!!"
    except:
        return False, "Дата есть дата, а это не дата!!! И я ещё тебя не понимаю!!!"


def get_in_data(message):
    global information
    if check_data(message.text)[0]:
        information[message.from_user.id]["in_data"] = message.text
        bot.send_message(message.from_user.id, 'Введите дату выезда (например: 01.01.1111) ')
        bot.register_next_step_handler(message, get_out_data)
        print(information[message.from_user.id]["in_data"])
    else:
        bot.send_message(message.from_user.id, check_data(message.text)[1])
        bot.register_next_step_handler(message, get_in_data)


def get_out_data(message):
    global information
    if check_data(message.text)[0]:
        information[message.from_user.id]["out_data"] = message.text
        print(information[message.from_user.id]["out_data"])
        if information[message.from_user.id]["status"] != '/bestdeal':
            bot.send_message(message.from_user.id, 'Нужно вывести фотографию?')
            bot.register_next_step_handler(message, nes_for_hotel_photo)
        else:
            bot.send_message(message.from_user.id, "Введите Максимальную сумму в $")
            bot.register_next_step_handler(message, get_maxSum)
    else:
        bot.send_message(message.from_user.id, check_data(message.text)[1])
        bot.register_next_step_handler(message, get_out_data)


def get_maxSum(message):
    global information
    if message.text.isdigit():
        information[message.from_user.id]["maxSum"] = int(message.text)
        bot.send_message(message.from_user.id, "Введите минимальную сумму в $")
        bot.register_next_step_handler(message, get_minSum)
        print(information[message.from_user.id]["maxSum"])
    else:
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста!!!")
        bot.register_next_step_handler(message, get_maxSum)


def get_minSum(message):
    global information
    if message.text.isdigit():
        information[message.from_user.id]["minSum"] = int(message.text)
        bot.send_message(message.from_user.id, "Нужно вывести фотографию? ")
        bot.register_next_step_handler(message, nes_for_hotel_photo)
        print(information[message.from_user.id]["minSum"])
    else:
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста!!!")
        bot.register_next_step_handler(message, get_minSum)


def nes_for_hotel_photo(message):
    global information
    information[message.from_user.id]['photo_status'] = message.text.lower()
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, "Сколько нужно фото?")
        bot.register_next_step_handler(message, count_of_photos)
    elif message.text.lower() == "нет":
        if information[message.from_user.id]["status"] == '/bestdeal':
            bot.send_message(message.chat.id, "Вы уверены:\n"
                                              "{0} город\n"
                                              "{1} дата въезда\n"
                                              "{2} дата выезда\n"
                                              "{3} максимальная сумма\n"
                                              "{4} минимальная сумма\n"
                                              "{5} Количество отелей\n".format(
                information[message.from_user.id]['city'],
                information[message.from_user.id]['in_data'],
                information[message.from_user.id]['out_data'],
                information[message.from_user.id]['maxSum'],
                information[message.from_user.id]['minSum'],
                information[message.from_user.id]['count_of_hotel']))
        else:
            bot.send_message(message.chat.id, "Вы уверены:\n"
                                              "{0} город\n"
                                              "{1} дата въезда\n"
                                              "{2} дата выезда\n"
                                              "{3} Количество отелей\n".format(
                information[message.from_user.id]['city'],
                information[message.from_user.id]['in_data'],
                information[message.from_user.id]['out_data'],
                information[message.from_user.id]['count_of_hotel']))
        bot.register_next_step_handler(message, do_you_want)

    else:
        bot.send_message(message.chat.id, "Напишите, пожалуйста Да/Нет")
        bot.register_next_step_handler(message, nes_for_hotel_photo)


def do_you_want(message):
    global information
    global list_of_hotels_for_history
    if message.text.lower() == "да":
        print(information)
        try:
            bot.send_message(message.from_user.id, 'Пожалуйста подождите...')
            print("Start_work")
            info = tim.Take_info()
            info.city(information[message.from_user.id]["city"])
            info.setter_data_in(information[message.from_user.id]['in_data'])
            info.setter_adult(information[message.from_user.id]['adults'])
            info.price_max_min(information[message.from_user.id]['maxSum'], information[message.from_user.id]['minSum'])
            info.setter_data_out(information[message.from_user.id]['out_data'])
            info.max_Sizes(information[message.from_user.id]['count_of_hotel'])
            info.payloads()
            info.responces()
            list_of_hotels = info.get_properties()
            for n in list_of_hotels:
                i = info.get_id_name_of_hotel(n)
                distance = info.get_distance_to_center(n)
                summary = info.get_summary(n)
                info_photo = tpm.Take_info()
                list_of_hotels_for_history.append(i[1])
                bot.send_message(message.chat.id, i[1])
                bot.send_message(message.chat.id, "Цена {0}".format(summary))
                bot.send_message(message.chat.id, "Расстояние до центра {0} км".format(distance))
                if information[message.from_user.id]['photo_status'] == 'да':
                    try:
                        g = info_photo.setter_payload_response(i[0])
                        list_photo = info_photo.get_photos(g, information[message.from_user.id]['count_of_photo'])
                        list_for_print = info_photo.publish_photo(list_photo)
                        for img in list_for_print:
                            bot.send_photo(message.chat.id, img)
                            print("Success")
                    except:
                        print('Ошибка')
            print("Это всё :)")
            bot.send_message(message.chat.id, "Это всё :)")
        except:
            bot.send_message(message.chat.id, "Нет подходящих отелей")
            print('Что-то не так!')
        ##############################################################################################################
        print(list_of_hotels_for_history)
        try:
            user_id = message.from_user.id
            if user_id in history_store:
                history_store[user_id].append(datetime.datetime.now())
                history_store[user_id].append(information[message.from_user.id]['city'])
                history_store[user_id].extend(list_of_hotels_for_history)
            elif len(list_of_hotels_for_history) == 0:
                history_store[user_id].append(datetime.datetime.now())
                history_store[user_id].append(information[message.from_user.id]['city'])
                history_store[user_id].append("Ничего не найдено")
            else:
                history_store[user_id] = []
                history_store[user_id].append(datetime.datetime.now())
                history_store[user_id].append(information[message.from_user.id]['city'])
                history_store[user_id].extend(list_of_hotels_for_history)
            list_of_hotels_for_history = []
        except:
            print("Ошибка истории")
    ##############################################################################################################
    else:
        bot.send_message(message.chat.id, "Ну раз не уверены, то давайте по новой...")
        bot.send_message(message.from_user.id, 'Вот такие команды я умею выполнять: \n'
                                               '/bestdeal\n'
                                               '/lowprise\n'
                                               '/highprice \n'
                                               '/history \n')
        bot.register_next_step_handler(message, start)


def count_of_photos(message):
    global information
    if message.text.isdigit():
        information[message.from_user.id]["count_of_photo"] = int(message.text)
        if information[message.from_user.id]["status"] == '/bestdeal':
            bot.send_message(message.chat.id, "Вы уверены:\n"
                                              "{0} город\n"
                                              "{1} дата въезда\n"
                                              "{2} дата выезда\n"
                                              "{3} максимальная сумма\n"
                                              "{4} минимальная сумма\n"
                                              "{5} Количество отелей\n".format(
                information[message.from_user.id]['city'],
                information[message.from_user.id]['in_data'],
                information[message.from_user.id]['out_data'],
                information[message.from_user.id]['maxSum'],
                information[message.from_user.id]['minSum'],
                information[message.from_user.id]['count_of_hotel']))
        else:
            bot.send_message(message.chat.id, "Вы уверены:\n"
                                              "{0} город\n"
                                              "{1} дата въезда\n"
                                              "{2} дата выезда\n"
                                              "{3} Количество отелей\n".format(
                information[message.from_user.id]['city'],
                information[message.from_user.id]['in_data'],
                information[message.from_user.id]['out_data'],
                information[message.from_user.id]['count_of_hotel']))
    else:
        bot.send_message(message.from_user.id, "Цифрами, пожалуйста!!!")
        bot.register_next_step_handler(message, count_of_photos)
    bot.register_next_step_handler(message, do_you_want)


bot.polling(none_stop=True, interval=0)
