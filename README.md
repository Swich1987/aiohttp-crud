# Simple CRUD for PostgreSQL tables

## Installation
`pip install -r requirements.txt`

## Description

This is a simple auto CRUD to show usage of SQLAlchemy Core, Pydantic, aiohttp. swagger, docker.
It can auto-detect all tables, and allow batch access to them: select, insert, update, delete. Swagger docs are auto-generated for every table with examples of usage, so you can easily try and understand how it works.
SQLAlchemy Core is used in counter to SQLAlchemy ORM, for speed up all operation with DB ([benchmark](https://docs.sqlalchemy.org/en/13/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow)).
Currently support only PostgreSQL table with id as primary key.

## nearest TODO:
- catch and show nice error message for wrong json body in requests
- return id's on update rows (updated+non existing)
- return id's of deleted rows (deleted+non existing)
- move all aiohttp settings to yaml file
- add tests

extend functionality:
- adding pagination
- adding sorting
- adding filtration