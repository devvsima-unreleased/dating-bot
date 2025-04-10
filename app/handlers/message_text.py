from loader import _

"""
Текст вынес в отдельный файл для более удобного редактирования
"""


class UserMessageText:
    @property
    def WELCOME(self):
        return _("""
Привет! 👋

Бот предназначен для знакомств и общения, а также для поиска и предложения услуг.
""")

    @property
    def MENU(self):
        return _("""
💘 Знакомства
💼 Услуги

✉️ Пригласить друзей
""")

    @property
    def DATING_MENU(self):
        return _("""
🔍 Смотреть анкеты
👤 Посмотреть свой профиль

🗄 Посмотреть лайки
""")

    @property
    def DATING_PROFILE_MENU(self):
        return _("""
🔄 Заполнить анкету заново
🖼 Изменить фотографию
✍️ Изменить описание
❌ Отключить анкету

💘 Вернутся в меню знакомств
""")

    @property
    def OFFER_MENU(self):
        return _("""
🔎 Смотреть анкеты
💰 Посмотреть свой профиль

💠 Посмотреть лайки
""")

    @property
    def OFFER_PROFILE_MENU(self):
        return _("""
🔃 Заполнить анкету заново
📸 Изменить фотографию
📝 Изменить описание
🔴 Отключить анкету

💼 Вернутся в меню услуг
""")

    @property
    def UNKNOWN_COMMAND(self):
        return _("Неизвестная команда. Если заблудился, напиши /start.")

    @property
    def INFO(self):
        return _("""
👋
Немного информации о боте:
Этот бот был создан по аналогии с популярным ботом для знакомств <a href='https://t.me/leomatchbot?start=i_VwRd0'>Дайвинчик</a>
Весь код бота открыт и доступен на <a href='https://github.com/devvsima/dating-bot'>GitHub</a>

По вопросам и предложениям можно писать сюда: @devvsima.
""")

    @property
    def SEARCH(self):
        return _("🔍 Выполняется поиск...")

    @property
    def INVALID_PROFILE_SEARCH(self):
        return _("Подходящих анкет нет. Попробуй указать другой город. 🌍")

    @property
    def EMPTY_PROFILE_SEARCH(self):
        return _("Больше анкет нет. Попробуйте позже! 😊")

    def LIKE_PROFILE(self, language: str):
        return _("Кому-то понравилась тваоя анкета! Хочешь посмотреть? 👀", locale=language)

    def LIKE_ACCEPT(self, language: str):
        return _("Отлично! Надеюсь хорошо проведете время ;) <a href='{}'>{}</a>", locale=language)

    @property
    def LIKE_ARCHIVE(self):
        return _("Тебя ещё никто не лайкнул, но всё впереди!")

    @property
    def GENDER(self):
        return _("Укажи, свой пол: 👤")

    @property
    def FIND_GENDER(self):
        return _("Выбери, кого ты ищешь: 💕")

    @property
    def PHOTO(self):
        return _("Пришли своё фото! 📸")

    @property
    def NAME(self):
        return _("Как тебя зовут? ✍️")

    @property
    def AGE(self):
        return _("Сколько тебе лет? 🎂")

    @property
    def CITY(self):
        return _("Укажи свой город: 🏙️")

    @property
    def DESCRIPTION(self):
        return _("Расскажи немного о себе! Это поможет другим лучше тебя узнать. 📝")

    @property
    def DISABLE_PROFILE(self):
        return _("""
❌ Ваша анкета отключена, некоторые функции теперь недоступны.
💬 Чтобы активировать анкету, напишите команду /start.""")

    @property
    def ACTIVATE_PROFILE_ALERT(self):
        return _("✅ Твоя анкета успешно восстановлена! Теперь ты снова можешь пользоваться ботом.")

    @property
    def INVALID_RESPONSE(self):
        return _("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝")

    @property
    def INVALID_LONG_RESPONSE(self):
        return _("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")

    @property
    def INVALID_CITY_RESPONSE(self):
        return _("Такой город не найдет :(")

    @property
    def INVALID_PHOTO(self):
        return _(
            "Неверный формат фотографии! Пожалуйста, загрузите изображение в правильном формате. 🖼️"
        )

    @property
    def INVALID_AGE(self):
        return _("Неверный формат, возраст нужно указывать цифрами. 🔢")

    @property
    def INVITE_FRIENDS(self):
        return _(
            "Приглашай друзей и получай бонусы!\n\nПриглашенные пользователи: <b>{}</b>\n\nСсылка для друзей:\n<code>https://t.me/{}?start={}</code>"
        )

    @property
    def CHANGE_LANG(self):
        return _("Выбери язык бота, на который хочешь переключиться: 🌐")

    def DONE_CHANGE_LANG(self, language: str):
        return _("Язык бота изменён! ✅", locale=language)

    @property
    def REPORT_TO_USER(self):
        return _(
            "Пользователь <code>{}</code> (@{}) отправил жалобу на анкету пользователя: <code>{}</code> (@{})"
        )

    @property
    def REPORT_TO_PROFILE(self):
        return _("✅ Жалоба отправлена на рассмотрение!")

    @property
    def SERVICE_TYPES(self):
        return _("Введите типы услуг через запятую (например, Маникюр, Стрижка, Окрашивание).")

    @property
    def RESON_OF_REPORTING(self):
        return _("""
Укажи причину жалобы:
🔞 Неприличный материал
💰 Реклама
🔫 Другое

Если жалоба ошибочная, то можете вернутся назад.
""")


user_message_text = UserMessageText()
