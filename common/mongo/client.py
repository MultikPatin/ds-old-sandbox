from collections.abc import Sequence
from typing import TYPE_CHECKING

from beanie import init_beanie
from pymongo import AsyncMongoClient

if TYPE_CHECKING:
    from beanie import Document, UnionDoc, View
    from pymongo.asynchronous.client_session import AsyncClientSession
    from pymongo.asynchronous.collection import AsyncCollection
    from pymongo.asynchronous.database import AsyncDatabase

    from .settings import Settings


class Client:
    _client: AsyncMongoClient  # type: ignore
    _database_name: str

    def __init__(self, settings: "Settings") -> None:
        self._client = AsyncMongoClient(
            settings.dsn.unicode_string(),
            compressors="snappy",
            # maxPoolSize=75,
        )
        self._database_name = settings.DATABASE

    @property
    def client(self) -> AsyncMongoClient:  # type: ignore
        return self._client

    @property
    def database(self) -> "AsyncDatabase":  # type: ignore
        return self._client[self._database_name]

    async def drop_database(self) -> None:
        await self._client.drop_database(self._database_name)

    @property
    async def collection_names(self) -> list[str]:
        return await self.database.list_collection_names()

    def get_collection(self, name: str) -> "AsyncCollection":  # type: ignore
        return self.database[name]

    async def drop_collection(self, name: str) -> None:
        collection = self.get_collection(name)
        await collection.drop()

    def start_session(self) -> "AsyncClientSession":
        return self._client.start_session()

    async def initialize(
        self,
        document_models: Sequence[
            type["Document"] | type["UnionDoc"] | type["View"]
        ],
    ) -> None:
        await init_beanie(
            database=self.database,
            document_models=document_models,
        )

    async def aclose(self) -> None:
        await self._client.aclose()
