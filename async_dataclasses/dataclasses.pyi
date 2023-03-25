from typing import TypeVar, Coroutine, Any

FN = TypeVar("FN")

class AsyncDataclass(type):

    @staticmethod
    def _field_wrapper_async(aw, field_name: FN) -> Coroutine[Any, tuple[Any, FN]]: ...

    async def complete(self, timeout: int | None = None) -> "AsyncDataclass": ...


def dataclass(*args, **kwargs) -> AsyncDataclass: ...
