import asyncio
import random
import time
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
    delay = random.choice([0.5, 1])
    print(f"Очікую {delay}c на отримання інформації про користувача {uid}")
    await asyncio.sleep(delay)
    name = UUIDS2NAME[uid]
    print(f"Інформація про користувача {uid} завантажено: {name}")
    return name


async def get_company_name_by_uid_async(uid: UUID) -> str:
    delay = random.choice([0.5, 1, 2, 3])
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
        delay = random.choice([0.5, 1])
        print(f"Очікую {delay}c на можливість отримати запит про користувача {self.uid}")
        await asyncio.sleep(delay)
        return await get_name_by_uid_async(self.uid)

    @company_name.resolver
    async def _company_name(self, *_) -> str:
        delay = random.choice([0.5, 1])
        print(f"Очікую {delay}c на можливість отримати запит про компанію {self.uid}")
        await asyncio.sleep(delay)
        return await get_company_name_by_uid_async(self.company_uid)


async def main():
    st = time.time()
    users = []
    for uid, company_uid in zip(UUIDS2NAME, UUIDS2COMPANY):
        users.append(User(uid, company_uid))
    await asyncio.gather(*(u.complete() for u in users))
    print(f"Витрачений час: {time.time() - st}")


if __name__ == "__main__":
    asyncio.run(main())


