from sqlalchemy import create_engine, MetaData, bindparam, tuple_
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from models import rows_validator_factory
from settings import POSTGRES_CRED

Session = sessionmaker(autoflush=False)


class PostgresDB:
    def __init__(self):
        self.engine = create_engine(URL('postgres', **POSTGRES_CRED),
                                    echo=False)
        self.tables = self.get_tables()

    def get_tables(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        return meta.tables

    def get_table_names(self):
        tables = self.get_tables()
        return list(tables.keys())

    def get_table(self, table_name):
        assert table_name in self.tables, f'Table "{table_name}" not exist.'
        return self.tables[table_name]

    def bulk_delete(self, table_name, raw_id_list):
        # delete rows by primary key in format [key1, key2, ...] with
        # auto-detected primary_key
        # TODO: validate that raw_rows is correct for that table

        table = self.get_table(table_name)

        with self.engine.connect() as connection:
            with connection.begin():
                primary_key_name = table.primary_key.columns.values()[0].name
                table_key = getattr(table.c, primary_key_name)

                stmt = table.delete(). \
                    where(table_key.in_(raw_id_list))

                updated_rows = connection.execute(stmt)

        return updated_rows.rowcount

    def bulk_update(self, table_name, raw_rows):
        # raw_rows in format [{}, {}, ...] with auto-detected primary_key
        table = self.get_table(table_name)

        rows_validator = rows_validator_factory(table, with_id=True)
        valid_rows = rows_validator(rows=raw_rows).dict()['rows']

        with self.engine.connect() as connection:
            with connection.begin():
                primary_key_name = table.primary_key.columns.values()[0].name
                table_key = getattr(table.c, primary_key_name)

                stmt = table.update(). \
                    where(table_key == bindparam(primary_key_name)). \
                    values({key: bindparam(key) for key in valid_rows[0]})

                updated_rows = connection.execute(stmt, valid_rows)

        return updated_rows.rowcount

    def bulk_insert(self, table_name, raw_rows):
        # raw_rows in format [{}, {}, ...] without id
        table = self.get_table(table_name)

        rows_validator = rows_validator_factory(table, with_id=False)
        valid_rows = rows_validator(rows=raw_rows).dict()['rows']

        with self.engine.connect() as connection:
            with connection.begin():
                connection.execute(table.insert(), valid_rows)

                keys = [col for col in table.c if col.name != 'id']
                values = [tuple(row.values()) for row in valid_rows]
                query = table.select().where(tuple_(*keys).in_(values))
                inserted_rows = [dict(row) for row in connection.execute(query)]

        return inserted_rows

    def select(self, table_name, limit=None):
        table = self.tables[table_name]

        with self.engine.connect() as connection:
            with connection.begin():
                query = table.select(limit=limit) if limit else table.select()
                rows = connection.execute(query)

                return [dict(row) for row in rows]


def main():
    postgres_db = PostgresDB()
    tables = postgres_db.get_tables()
    for table_name in tables:
        print(table_name, postgres_db.select(table_name))

    table_name = 'clients'
    rows = postgres_db.select(table_name, limit=1)
    # insert(engine, tables[table_name], rows)
    # update(engine, tables[table_name], rows)
    # delete(engine, tables[table_name], [4, 5])
    print('End')


if __name__ == '__main__':
    main()
