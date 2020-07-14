from functools import wraps

from aiohttp import web
from pydantic import ValidationError

from db_handlers.postgres import PostgresDB
from swagger.setup_swagger import setup_swagger

routes = web.RouteTableDef()
postgres_db = PostgresDB()


async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)


def catch_validation_errors(func):
    @wraps(func)
    async def catcher(*args, **kwargs):

        try:
            res = await func(*args, **kwargs)
            return res

        except ValidationError as err:
            return web.json_response({'errors': err.errors()})
        except AssertionError as err:
            return web.json_response({'errors': str(err)})

    return catcher


@routes.get('/crud/')
async def get_table_list(_):
    table_list = postgres_db.get_table_names()
    return web.Response(text=f'{table_list}')


@routes.get('/crud/{table_name}/')
async def table_select(request):
    rows = postgres_db.select(table_name=request.match_info['table_name'])
    return web.Response(text=f'{rows}')


@routes.post('/crud/{table_name}/create/')
@catch_validation_errors
async def table_bulk_insert(request):
    rows_data = await request.json()
    table_name = request.match_info['table_name']
    rows = postgres_db.bulk_insert(table_name=table_name,
                                   raw_rows=rows_data)
    return web.json_response({'count': len(rows), 'inserted_rows': rows})


@routes.post('/crud/{table_name}/delete/')
@catch_validation_errors
async def table_bulk_delete(request):
    id_list = await request.json()
    rows = postgres_db.bulk_delete(table_name=request.match_info['table_name'],
                                   raw_id_list=id_list)
    return web.json_response({'deleted_rows': rows})


@routes.post('/crud/{table_name}/update/')
@catch_validation_errors
async def table_bulk_update(request):
    rows_data = await request.json()
    rows = postgres_db.bulk_update(table_name=request.match_info['table_name'],
                                   raw_rows=rows_data)
    return web.json_response({'updated_rows': rows})


def main():
    app = web.Application()
    app.add_routes(routes)
    setup_swagger(app)
    web.run_app(app)


if __name__ == '__main__':
    print('==== SWAGGER on http://0.0.0.0:8080/api/doc/ ====')
    main()
