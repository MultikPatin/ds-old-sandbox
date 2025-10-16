from .blocks import (
    InputSingleServiceProtocol,
    InputTableChunkServiceProtocol,
    InputTableServiceProtocol,
)
from .card import InputCardServiceProtocol
from .input import InputServiceProtocol
from .template import InputTemplateServiceProtocol

__all__ = [
    "InputCardServiceProtocol",
    "InputServiceProtocol",
    "InputSingleServiceProtocol",
    "InputTableChunkServiceProtocol",
    "InputTableServiceProtocol",
    "InputTemplateServiceProtocol",
]
