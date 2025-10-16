from collections.abc import Sequence

from beanie import Document, UnionDoc, View, init_beanie
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession

from .settings import Settings


class Client:
    _client: AsyncMongoClient  # type: ignore
    _database: str

    def __init__(self, settings: Settings) -> None:
        self._client = AsyncMongoClient(settings.dsn.unicode_string())
        self._database = settings.database

    @property
    def client(self) -> AsyncMongoClient:  # type: ignore
        return self._client

    async def start_session(self) -> AsyncClientSession:
        return self._client.start_session()

    async def initialize(
        self,
        document_models: Sequence[type[Document] | type[UnionDoc] | type[View]],
    ) -> None:
        await init_beanie(
            database=getattr(self._client, self._database),
            document_models=document_models,
        )

    async def aclose(self) -> None:
        await self._client.aclose()
