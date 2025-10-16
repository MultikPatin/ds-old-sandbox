import functools
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from .protocols import SessionProtocol


def transaction[**P, T](
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Coroutine[Any, Any, T]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if "session" not in kwargs:
            func_name = func.__name__
            msg = (
                "'session' keyword argument is expected,"
                f"but it has not been passed to the function: {func_name}"
            )
            raise RuntimeError(msg)

        session = kwargs.get("session")

        if session is None:
            return await func(*args, **kwargs)

        if not isinstance(session, SessionProtocol):
            msg = "The object does not implement the SessionProtocol interface"
            raise TypeError(msg)

        if session.in_transaction:
            return await func(*args, **kwargs)
        async with await session.start_transaction():
            return await func(*args, **kwargs)

    return wrapper
