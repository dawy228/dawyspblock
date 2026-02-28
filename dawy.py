import telebot
from telebot import types

TOKEN = "8539742084:AAG_cLpIDo4UTiSHhhTy9f_uuuxmaWm9Af8"
ADMIN_ID = 78379079

bot = telebot.TeleBot(TOKEN)
user_dict = {}


@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker'])
def forward_to_admin(message):
    if message.from_user.id == ADMIN_ID:
        return

    user = message.from_user
    user_id = user.id
    user_dict[user_id] = user_id

    username = f"@{user.username}" if user.username else "нет username"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    info_text = (
        f"📩 Новое сообщение\n\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user_id}"
    )

    markup = types.InlineKeyboardMarkup()
    reply_button = types.InlineKeyboardButton(
        "✉️ Ответить",
        callback_data=f"reply_{user_id}"
    )
    markup.add(reply_button)

    bot.send_message(ADMIN_ID, info_text, reply_markup=markup)
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def callback_reply(call):
    user_id = int(call.data.split("_")[1])
    msg = bot.send_message(ADMIN_ID, "✍️ Введите ответ пользователю:")
    bot.register_next_step_handler(msg, send_reply, user_id)


def send_reply(message, user_id):
    if message.from_user.id != ADMIN_ID:
        return

    header = (
        "━━━━━━━━━━━━━━\n"
        "📩 Ответ от администрации\n"
        "━━━━━━━━━━━━━━\n\n"
    )

    try:
        if message.content_type == "text":
            bot.send_message(user_id, header + (message.text or ""))

        elif message.content_type == "photo":
            bot.send_photo(
                user_id,
                message.photo[-1].file_id,
                caption=header + (message.caption or "")
            )

        elif message.content_type == "video":
            bot.send_video(
                user_id,
                message.video.file_id,
                caption=header + (message.caption or "")
            )

        elif message.content_type == "document":
            bot.send_document(
                user_id,
                message.document.file_id,
                caption=header + (message.caption or "")
            )

        elif message.content_type == "audio":
            bot.send_audio(
                user_id,
                message.audio.file_id,
                caption=header + (message.caption or "")
            )

        elif message.content_type == "voice":
            bot.send_message(user_id, header)
            bot.send_voice(user_id, message.voice.file_id)

        elif message.content_type == "video_note":
            bot.send_message(user_id, header)
            bot.send_video_note(user_id, message.video_note.file_id)

        elif message.content_type == "sticker":
            bot.send_message(user_id, header)
            bot.send_sticker(user_id, message.sticker.file_id)

        bot.send_message(ADMIN_ID, "✅ Ответ отправлен")

    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")


print("Бот запущен...")
bot.infinity_polling()