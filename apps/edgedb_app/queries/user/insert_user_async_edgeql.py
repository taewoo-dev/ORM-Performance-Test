# AUTOGENERATED FROM 'queries/insert_user.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import gel
import uuid
from typing import cast


@dataclasses.dataclass
class InsertUserResult:
    id: uuid.UUID
    name: str
    email: str


async def insert_user(
    executor: gel.AsyncIOExecutor,
    *,
    name: str,
    email: str,
) -> InsertUserResult:
    return cast(InsertUserResult, await executor.query_single(
        """\
        WITH
          new_user := (
            INSERT User {
              name := <str>$name,
              email := <str>$email
            }
          )
        SELECT new_user {
          id,
          name,
          email
        };\
        """,
        name=name,
        email=email,
    ))
