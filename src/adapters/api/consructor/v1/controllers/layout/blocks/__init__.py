# from .card import router as card_router
from .massage import router as massage_router
from .single import router as single_router
from .table import router as table_router

__all__ = [
    "massage_router",
    "single_router",
    # "card_router",
    "table_router",
]
