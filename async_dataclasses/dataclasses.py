import asyncio
import dataclasses
import functools
from asyncio import Task
from typing import Any

import async_dataclasses


class AsyncDataclass:

    def as_coro(self):
        async def wrapped():
            await self
        return wrapped()

    def __await__(self):
        """
            TODO: timeout
        """
        tasks = []
        for field_name, field in self.__dataclass_fields__.items():
            if isinstance(field, async_dataclasses.Field):
                tasks.extend(self._field_as_task(field_name))

        results: list[tuple[Any, str]] = yield from asyncio.gather(*tasks)  # noqa
        for new_value, field_name in results:
            setattr(self, field_name, new_value)

    @staticmethod
    def _field_wrapper_async(aw, field_name):
        @functools.wraps(aw)
        async def wrapped(*args, **kwargs):
            return await aw(*args, **kwargs), field_name
        return wrapped

    def _field_as_task(self, field_name):
        field = self.__dataclass_fields__[field_name]
        if not field.resolvers:
            return asyncio.sleep(0)
        for aw in field.resolvers:
            orig_value = getattr(self, field_name)
            coro = self._field_wrapper_async(aw, field_name)(self, orig_value)
            yield Task(coro)


def dataclass(*args, **kwargs):
    """
        TODO: docstring
    """

    new_cls = type(
        args[0].__name__,
        (AsyncDataclass, dataclasses.dataclass(*args, **kwargs)),
        {},
    )
    return new_cls
