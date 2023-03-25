# async-dataclasses

## TODO
- pre-commit
- автоматичне формування .md файлу з прикладом використання
- "TODO" по бібліотеці

## Приклад використання
```python 
import asyncio
import contextlib
import random
import time
from asyncio import Task
from uuid import UUID, uuid4

import async_dataclasses


UUIDS2NAME = {
    uuid4(): "Anthony Kelly",
    uuid4(): "Finley Stevens",
    uuid4(): "Jordan Clark",
    uuid4(): "Reece Powell",
    uuid4(): "Malakai Wilder",
}

UUIDS2COMPANY = {
    uuid4(): "Tech Vibe",
    uuid4(): "Box Tech",
    uuid4(): "WOW Tech",
    uuid4(): "Tech mint",
    uuid4(): "Phoenix Tech",
}


async def get_name_by_uid_async(uid: UUID) -> str:
    # delay = random.choice([0.5, 1])
    delay = 1
    print(f"Очікую {delay}c на отримання інформації про користувача {uid}")
    await asyncio.sleep(delay)
    name = UUIDS2NAME[uid]
    print(f"Інформація про користувача {uid} завантажено: {name}")
    return name


async def get_company_name_by_uid_async(uid: UUID) -> str:
    # delay = random.choice([0.5, 1, 2, 3])
    delay = 1
    print(f"Очікую {delay}c на отримання інформації про компанію {uid}")
    await asyncio.sleep(delay)
    name = UUIDS2COMPANY[uid]
    print(f"Інформація про компанію {uid} завантажено: {name}")
    return name


@async_dataclasses.dataclass
class User:
    uid: UUID
    company_uid: UUID
    name: async_dataclasses.Field[str] = async_dataclasses.field(default="N/A")
    company_name: async_dataclasses.Field[str] = async_dataclasses.field(default="N/A")

    @name.resolver
    async def _name(self, *_) -> str:
        # delay = random.choice([0.5, 1])
        delay = 1
        print(f"Очікую {delay}c на можливість отримати запит про користувача {self.uid}")
        await asyncio.sleep(delay)
        return await get_name_by_uid_async(self.uid)

    @company_name.resolver
    async def _company_name(self, *_) -> str:
        # delay = random.choice([0.5, 1])
        delay = 1
        print(f"Очікую {delay}c на можливість отримати запит про компанію {self.uid}")
        await asyncio.sleep(delay)
        return await get_company_name_by_uid_async(self.company_uid)


async def single():
    lazy_user = User(list(UUIDS2NAME)[0], list(UUIDS2COMPANY)[0])
    await lazy_user


async def task_by_task():
    u1 = User(list(UUIDS2NAME)[0], list(UUIDS2COMPANY)[0])
    u2 = User(list(UUIDS2NAME)[1], list(UUIDS2COMPANY)[1])
    u3 = User(list(UUIDS2NAME)[3], list(UUIDS2COMPANY)[3])
    t1 = asyncio.create_task(u1.as_coro())
    t2 = asyncio.create_task(u2.as_coro())
    t3 = asyncio.create_task(u3.as_coro())
    await t1
    await t2
    await t3


async def as_completed():
    tasks = []
    for uid, company_uid in zip(UUIDS2NAME, UUIDS2COMPANY):
        user = User(uid, company_uid)
        tasks.append(user.as_coro())
    for coro in asyncio.as_completed(tasks):
        await coro


async def gather():
    tasks = []
    for uid, company_uid in zip(UUIDS2NAME, UUIDS2COMPANY):
        user = User(uid, company_uid)
        tasks.append(user.as_coro())
    await asyncio.gather(*tasks)


@contextlib.contextmanager
def timeit(alias: str):
    st = time.time()
    yield
    print(alias, time.time() - st)


async def main():
    with timeit("single"):
        await single()
    with timeit("\n\ntask_by_task"):
        await task_by_task()
    with timeit("\n\nas_completed"):
        await as_completed()
    with timeit("\n\ngather"):
        await gather()


if __name__ == "__main__":
    asyncio.run(main())

```

