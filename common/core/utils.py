import random
import secrets
import string
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import tzinfo

__all__ = [
    "generate_random_string",
    "generate_secure_random_string",
    "time_now",
]


_ALPHABET: str = string.ascii_letters + string.digits
_ALPHABET_BYTES: bytes = _ALPHABET.encode("ascii")
_ALPHABET_LEN: int = len(_ALPHABET)


def time_now(tz: "tzinfo" = UTC) -> datetime:
    return datetime.now(tz)


def generate_random_string(length: int = 16) -> str:
    """Сверхбыстрая: использует bytearray и getrandbits."""
    result = bytearray(length)
    for i in range(length):
        result[i] = _ALPHABET_BYTES[random.getrandbits(6) % _ALPHABET_LEN]
    return result.decode("ascii")


def generate_secure_random_string(length: int = 16) -> str:
    """
    Оптимизированная криптостойкая генерация.
    Использует secrets.randbelow для индексов
    """
    result = bytearray(length)
    for i in range(length):
        result[i] = _ALPHABET_BYTES[secrets.randbelow(_ALPHABET_LEN)]
    return result.decode("ascii")
