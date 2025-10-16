from .blocks import (
    InputSingleRepositoryProtocol,
    InputTableChunkRepositoryProtocol,
    InputTableRepositoryProtocol,
)
from .card import InputCardRepositoryProtocol
from .input import InputRepositoryProtocol

__all__ = [
    "InputCardRepositoryProtocol",
    "InputRepositoryProtocol",
    "InputSingleRepositoryProtocol",
    "InputTableChunkRepositoryProtocol",
    "InputTableRepositoryProtocol",
]
