import asyncio
import logging as log
import os

from pyrogram import Client, compose

# noinspection PyUnresolvedReferences
import essential
from app import handlers, CallbackQuery
from app.dependencies import Postgresql, run_sequence
from config import settings


async def main():
    client = Client(
        name="magic-money", api_id=settings().TG_API_ID, api_hash=settings().TG_API_HASH,
        bot_token=settings().TG_BOT_TOKEN, workers=min(32, (os.cpu_count() or 1) + 4),
        test_mode=~settings().production + 2, in_memory=~settings().production + 2
    )
    print(asyncio.get_event_loop())
    async with Postgresql() as db:
        # noinspection PyPep8Naming
        cbQuery = CallbackQuery(client=client, db=db)
        # noinspection PyPep8Naming

        log.debug("Entered mainloop")
        await run_sequence(
            handlers.init(
                client=client, cbQuery=cbQuery, db=db
            ),
            compose([client]),
        )


if __name__ == "__main__":
    asyncio.run(main())
