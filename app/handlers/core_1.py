import re

import pyrogram
from pyrogram import Client, types

from app.utils import run_sequence, run_parallel, Firestore, Postgresql


async def init(client: Client):
    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*start")))
    async def _start_page(_client: Client, message: types.Message):
        sender: types.User = message.from_user
        sender_id = str(sender.id)

        payload = f'{fn if (fn := sender.first_name) else ""} {ln if (ln := sender.last_name) else ""}'.strip()
        await run_parallel(
            run_sequence(
                _client.send_message(
                    chat_id=sender.id,
                    text=f"Greetings, **{payload}**!",
                    reply_markup=types.ReplyKeyboardMarkup([
                        [
                            types.KeyboardButton("Options")
                        ]
                    ], resize_keyboard=True)
                ),
                _client.send_message(sender_id, "lol"),
            ),
        )
        raise pyrogram.StopPropagation

    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*options")))
    async def _options_page(_client: Client, message: types.Message):
        sender = message.from_user
        payload = f'{fn if (fn := sender.first_name) else ""} {ln if (ln := sender.last_name) else ""}'.strip()
        await _client.send_message(
            chat_id=sender.id,
            text=f"Greetings, **{payload}**!",
            reply_markup=types.ReplyKeyboardMarkup([
                [
                    types.KeyboardButton("Options")
                ]
            ], resize_keyboard=True)
        )
        await client.send_message(sender.id, "options")

        raise pyrogram.StopPropagation
