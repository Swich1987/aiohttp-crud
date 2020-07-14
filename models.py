from typing import List

from pydantic import BaseModel
from sqlalchemy import Table


def model_validator_factory(table: Table, with_id=True):
    kwargs = {}

    for column in table.c:
        if with_id or column.name != 'id':
            kwargs[str(column.name)] = column.type.python_type

    class_name = f'Pydantic{table.name.capitalize()}'
    return type(class_name, (BaseModel,), {'__annotations__': kwargs})


def rows_validator_factory(table: Table, with_id=True):
    pydantic_model_class = model_validator_factory(table, with_id=with_id)
    kwargs = {'rows': List[pydantic_model_class]}
    class_name = f'{table.name.capitalize()}RequestRows'
    return type(class_name, (BaseModel,), {'__annotations__': kwargs})


class TestPy(BaseModel):
    name: str
    address: str


class TestPyList(BaseModel):
    users: List[TestPy]
