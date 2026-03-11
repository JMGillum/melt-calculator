from enum import Enum

class SQLType(Enum):
    MYSQL = 1

sql_type_in_use = SQLType.MYSQL

update = None
insert = None
delete = None
queries = None


if sql_type_in_use == SQLType.MYSQL:
    from .mysql import update, delete, insert, queries


