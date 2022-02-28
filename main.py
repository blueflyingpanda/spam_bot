import telebot
from datetime import datetime


def get_participants_dict(adm: bool = False):
    if adm:
        file_name = "admins.txt"
    else:
        file_name = "id_to_user.txt"
    with open(file_name, 'r+') as file:
        data = file.read()
    if data is None:
        raise Exception('Could not open id_to_user.txt or admins.txt')
    data = data.split('\n')
    ret = {}
    for d in data:
        sep = d.find('@')
        ret[int(d[0:sep])] = d[sep + 1:]
    return ret


def get_adm_str(adm):
    ret = ''
    for a in adm.values():
        ret += '@' + a + '\n'
    return ret


def send_all(sender, participants, bot, msg):
    if msg.photo:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_photo(participant_id, msg.photo[1].file_id, caption=msg.caption)
    elif msg.sticker:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_sticker(participant_id, msg.sticker.file_id)
    elif msg.document:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_document(participant_id, msg.document.file_id)
    elif msg.audio:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_audio(participant_id, msg.audio.file_id)
    elif msg.video:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_video(participant_id, msg.video.file_id)
    elif msg.voice:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_voice(participant_id, msg.voice.file_id)
    elif msg.animation:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_animation(participant_id, msg.animation.file_id)
    else:
        for participant_id in participants.keys():
            if participant_id != sender:
                bot.send_message(participant_id, msg.text)


def main():
    try:
        participants = get_participants_dict()
        admins = get_participants_dict(adm=True)
    except Exception as e:
        print(e)
        exit(1)
    with open("token.txt") as t:
        token = t.read()
    try:
        bot = telebot.TeleBot(token)
    except:
        print("Wrong token!")
        exit(1)

    @bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "voice", "animation"])
    def get_messages(message):
        if len(participants) == 0:
            bot.send_message(message.from_user.id,
                             "Никто не получит это сообщение. Ты единственный пользователь \U0001F9D0")
            return
        if message.text == "/start":
            if message.from_user.id not in participants:
                participants[message.from_user.id] = message.from_user.username
                with open("id_to_user.txt", 'a') as file:
                    file.write('\n' + str(message.from_user.id) + '@' + message.from_user.username)
                bot.send_message(message.from_user.id, "Добро пожаловать! Теперь ты будешь получать спам")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, 'твой id: ' + str(message.from_user.id) + '\nтвой ник: '
                             + str(message.from_user.username) + '\n\nадмины:\n' + get_adm_str(admins))
        elif message.text == "/stop":
            if message.from_user.id in admins:
                exit(0)
        else:
            if message.from_user.id in admins:
                send_all(message.from_user.id, participants, bot, message)
            elif message.text:
                with open('log.txt', 'a') as log:
                    log.write(message.from_user.username + ' ' + datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + ':\n' + message.text + '\n===============================\n')

    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()






