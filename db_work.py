from typing import Tuple, List
from db_context_manager import DBContextManager


def select(db_config: dict, sql: str):
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return schema, result


def select_dict(db_config: dict, sql: str):
    result = []
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    return result


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)

        res = cursor.callproc(proc_name, param_list)
    return res


def select_createp(db_config: dict, sql: str):
    _, res = select(db_config, sql)
    result = {}
    for line in res:
        if line[0] not in result:
            result[line[0]] = [line[1]]
        else:
            result[line[0]].append(line[1])
    return result


def select_showp(db_config: dict, sql: str):
    _, res = select(db_config, sql)
    closed = []
    opened = []
    for line in res:
        if line[1] is None:
            opened.append([*line])
        else:
            closed.append([*line])
    return opened, closed