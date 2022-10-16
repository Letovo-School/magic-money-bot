import typing

from pyrogram import Client, types

from app.dependencies import (
    Postgresql
)

choose_an_option_below_text = "Choose an option below ↴"
back_btn_text = "« Back"


class CallbackQuerySenders:
    """

    Args:
        client (pyrogram.Client): an instance of ``Client`` with credentials filled in
        db (Postgresql): connection to the database with users' usage analytics
    """
    __slots__ = ("client", "_db")

    def __init__(
            self, client: Client, db: Postgresql
    ):
        self.client: Client = client
        self._db: Postgresql = db

    async def send_greeting(self, sender: types.User) -> types.Message:
        """
        Send a greeting to the end user

        Args:
            sender (types.User): end user

        Returns:
            types.Message
        """
        payload = f'{fn if (fn := sender.first_name) else ""} {ln if (ln := sender.last_name) else ""}'.strip()
        return await self.client.send_message(
            chat_id=sender.id,
            text=f"Greetings, **{payload}**!",
            reply_markup=types.ReplyKeyboardMarkup([
                [
                    types.KeyboardButton("Options")
                ]
            ], resize_keyboard=True)
        )

    async def send_help_page(
            self, sender: types.User, no_register: bool = False
    ) -> types.Message:
        """
        Send help page

        Args:
            sender (types.User): end user
            no_register (bool): either add button for registering or not

        Returns:
            types.Message
        """
        if not no_register:
            reply_markup = types.ReplyKeyboardMarkup([
                [
                    types.KeyboardButton(
                        text="Click here to register",
                        web_app=types.WebAppInfo(url="https://letovo-analytics.web.app/webview")
                    )
                ]
            ], resize_keyboard=True)
        else:
            reply_markup = None

        return await self.client.send_message(
            chat_id=sender.id,
            text="Some help info",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    async def send_about_page(self, sender: types.User) -> types.Message:
        """
        Send `about developers` page

        Args:
            sender (types.User): end user

        Returns:
            types.Message
        """
        return await self.client.send_message(
            chat_id=sender.id,
            text="**Arseny Kurin**\n"
                 "• 2024kurin.av@student.letovo.ru\n"
                 "• [Github](https://github.com/arsikurin)\n"
                 "• [Telegram](https://t.me/arsikurin)\n\n"
                 "**Gleb Genken**\n"
                 "• 2024genken.gg@student.letovo.ru\n"
                 "• [Github](https://github.com/ggenken)\n"
                 "• [Telegram](https://t.me/genken)\n\n"
                 "**Nikita Kurlaev**\n"
                 "• 2024kurlaev.nX@student.letovo.ru\n"
                 "• [Github](https://github.com/yakuri354)\n"
                 "• [Telegram](https://t.me/ogleanenjoyer)\n"
            ,
        )

    async def send_landing_page(self, sender: types.User) -> types.Message:
        """
        Send landing page

        Args:
            sender (types.User): end user

        Returns:
            types.Message
        """
        return await self.client.send_message(
            chat_id=sender.id,
            text=choose_an_option_below_text,
            reply_markup=types.InlineKeyboardMarkup([
                [
                    types.InlineKeyboardButton("Send money", b"send")
                ], [
                    types.InlineKeyboardButton("Transactions »", b"trans"),
                ], [
                    types.InlineKeyboardButton("My balance »", b"balance"),
                ]
            ])
        )


class CallbackQueryEventEditors(CallbackQuerySenders):
    @staticmethod
    async def to_landing_page(event: types.CallbackQuery):
        """
        Display `landing` page

        Args:
            event (types.CallbackQuery): a return object of CallbackQuery
        """
        await event.edit_message_text(
            choose_an_option_below_text,
            reply_markup=types.InlineKeyboardMarkup([
                [
                    types.InlineKeyboardButton("Send money", b"send")
                ], [
                    types.InlineKeyboardButton("Transactions »", b"trans"),
                ], [
                    types.InlineKeyboardButton("My balance »", b"balance"),
                ]
            ])
        )
        await event.answer()


@typing.final
class CallbackQuery(CallbackQueryEventEditors):
    """
    Class for dealing with callback query
    """
