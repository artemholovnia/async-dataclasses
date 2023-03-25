import asyncio
import dataclasses
import functools
from asyncio import Task

import async_dataclasses


def dataclass(*args, **kwargs):
    """
        TODO: docstring
    """

    cls = dataclasses.dataclass(*args, **kwargs)

    def field_wrapper_async(aw, field_name):
        @functools.wraps(aw)
        async def wrapped(*args, **kwargs):
            return await aw(*args, **kwargs), field_name
        return wrapped

    async def complete(self, timeout: int | None = None):
        tasks = []
        for field_name, field in self.__dataclass_fields__.items():
            if isinstance(field, async_dataclasses.Field) and field.resolvers:
                for aw in field.resolvers:
                    orig_value = getattr(self, field_name)
                    coro = field_wrapper_async(aw, field_name)(self, orig_value)
                    tasks.append(Task(coro))

        for task in asyncio.as_completed(tasks, timeout=timeout):
            new_value, field_name = await task
            setattr(self, field_name, new_value)

        return self

    cls.complete = complete
    return cls
