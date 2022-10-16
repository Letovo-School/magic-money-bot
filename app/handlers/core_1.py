import re

import pyrogram
from pyrogram import Client, types

from app.callbackquery import CallbackQuery
from app.dependencies import run_sequence, run_parallel


async def init(client: Client, cbQuery: CallbackQuery):
    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*start")))
    async def _start_page(_client: Client, message: types.Message):
        sender = message.from_user
        sender_id = str(sender.id)

        await run_parallel(
            run_sequence(
                cbQuery.send_greeting(sender),
                _client.send_message(sender_id, "lol"),
            ),
        )
        raise pyrogram.StopPropagation

    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*options")))
    async def _options_page(_client: Client, message: types.Message):
        sender = message.from_user
        await run_sequence(
            cbQuery.send_greeting(sender),
            cbQuery.send_landing_page(sender)
        )

        raise pyrogram.StopPropagation

    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*help")))
    async def _options_page(_client: Client, message: types.Message):
        sender = message.from_user
        await run_sequence(
            cbQuery.send_greeting(sender),
            cbQuery.send_help_page(sender)
        )

        raise pyrogram.StopPropagation

    @client.on_message(pyrogram.filters.regex(pattern=re.compile(r"(?i).*about")))
    async def _options_page(_client: Client, message: types.Message):
        sender = message.from_user
        await run_sequence(
            cbQuery.send_greeting(sender),
            cbQuery.send_about_page(sender)
        )

        raise pyrogram.StopPropagation
