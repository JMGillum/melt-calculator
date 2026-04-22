from enum import Enum

class SQLType(Enum):
    MYSQL = 1

sql_type_in_use = SQLType.MYSQL

Updates = None
Inserts = None
Deletes = None
Queries = None
name = None
display_name = None


if sql_type_in_use == SQLType.MYSQL:
    from .mysql import update, delete, insert, queries
    name = "mysql"
    display_name = "MySQL"
    Queries = queries


