import datetime
import os

import aiohttp_swagger

from db_handlers.postgres import PostgresDB
from swagger.swagger_templates import GET_ROWS, INSERT_ROWS, UPDATE_ROWS, \
    DELETE_ROWS


class SwaggerConstructor:
    SWAGGER_TYPES = {
        int: 'integer',
        float: 'number',
        str: 'string',
        bool: 'boolean',
        bytes: 'string',
        datetime.date: 'string',
        datetime.datetime: 'string',
    }

    def __init__(self):
        self.postgres_db = PostgresDB()
        cur_dir = os.path.dirname(__file__)
        self.static_filename = os.path.join(cur_dir,
                                            'static_part_of_swagger.yaml')
        self.swagger_filename = os.path.join('swagger/swagger.yaml')

    @staticmethod
    def _get_schema_ident(template_text, schema_str):
        rows = template_text.split('\n')
        schema_row = ''

        for row in rows:
            if f'{{{schema_str}}}' in row:
                schema_row = row
                break

        ident = schema_row.find('{')
        return ident * ' ' if ident > 0 else ' '

    def get_schema(self, table_name, template_text, with_id=True,
                   schema_str='schema'):
        row = self.postgres_db.select(table_name, limit=1)[0]
        ident = self._get_schema_ident(template_text, schema_str=schema_str)

        result = f'''
{ident}schema:
{ident}  type: array
{ident}  items:
{ident}    type: object
{ident}    properties:'''

        field_swagger = '''
{ident}      {field_name}:
{ident}        type: {field_type}
{ident}        example:
{ident}          {example}
'''

        for field_name in row:
            if not with_id and field_name == 'id':
                continue
            value = row[field_name]
            kwargs = {'field_name': field_name,
                      'field_type': self.SWAGGER_TYPES[type(value)],
                      'example': value,
                      'ident': ident}
            result += field_swagger.format(**kwargs)

        return result

    def construct(self):
        with open(self.static_filename, 'r') as static_file:
            text = static_file.read()

        tables = self.postgres_db.get_tables()
        for table_name in tables:
            schema = self.get_schema(table_name, GET_ROWS)
            text += GET_ROWS.format(table_name=table_name, schema=schema)

            req_schema = self.get_schema(table_name, INSERT_ROWS, with_id=False,
                                         schema_str='req_schema')
            res_schema = self.get_schema(table_name, INSERT_ROWS, with_id=True,
                                         schema_str='res_schema')
            text += INSERT_ROWS.format(table_name=table_name,
                                       req_schema=req_schema,
                                       res_schema=res_schema,
                                       with_id=False)

            text += DELETE_ROWS.format(table_name=table_name)

            schema = self.get_schema(table_name, UPDATE_ROWS)
            text += UPDATE_ROWS.format(table_name=table_name, schema=schema)

        with open(self.swagger_filename, 'w') as swagger_file:
            swagger_file.write(text)

        return self.swagger_filename


def setup_swagger(app):
    swagger_constructor = SwaggerConstructor()
    swagger_filename = swagger_constructor.construct()

    swagger_description = "Simple CRUD(Create, Read, Update, Delete) for tables"
    aiohttp_swagger.setup_swagger(
        app,
        title="CRUD",
        description=swagger_description,
        swagger_from_file=swagger_filename
    )


if __name__ == '__main__':
    swagger_constr = SwaggerConstructor()
    swagger_constr.construct()
    print('End')
