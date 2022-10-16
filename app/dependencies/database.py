from __future__ import annotations

import types
import typing

import psycopg
from config import settings

unknown_err = "the connection is lost"


@typing.final
class Postgresql:
    """
    Class for dealing with Postgresql
    """
    __slots__ = ("_connection",)

    def __init__(self):
        self._connection: psycopg.AsyncConnection[typing.Any] = ...

    async def __aenter__(self) -> Postgresql:
        # self._connection = await self._connect()
        self._connection = ""
        return self

    async def __aexit__(
            self,
            exc_type: typing.Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: types.TracebackType | None,
    ):
        ...
        # await self._connection.__aexit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)

    @staticmethod
    async def _connect() -> psycopg.AsyncConnection[typing.Any]:
        """
        Connect to Postgres

        Returns:
            database connection
        """
        return await psycopg.AsyncConnection.connect(
            conninfo=settings().DATABASE_URL, sslmode="require"  # , row_factory=class_row(`class`)
        )
