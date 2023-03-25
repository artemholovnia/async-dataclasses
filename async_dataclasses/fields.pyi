import dataclasses
from asyncio import Task, Future
from typing import Generic, TypeVar, TypeAlias, Any, Coroutine

T = TypeVar("T")
AW: TypeAlias = Task | Future | Coroutine


class Field(dataclasses.Field, Generic[T]):
    resolvers: list[AW]

    def resolver(self, aw_or_callable: AW) -> Any: ...


def field(*args, **kwargs) -> Field: ...
