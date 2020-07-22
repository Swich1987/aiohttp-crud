GET_ROWS = '''  /crud/{table_name}/:
    get:
      summary: Get {table_name} table rows
      description: Get list of rows from {table_name} table. Support filtering, ordering, paggination.
      produces:
        - application/json
      tags:
        - {table_name}
      responses:
        200:
          description: OK
          {schema}
        "400":
          description: wrong request params
'''

INSERT_ROWS = '''  /crud/{table_name}/create/:
    post:
      summary: Insert new rows to {table_name} table
      description: Insert new rows to {table_name} table
      produces:
        - application/json
      tags:
        - {table_name}
      parameters:
        - in: body
          name: {table_name} rows
          description: the array of rows to insert
          {req_schema}
      responses:
        200:
          description: OK
          {res_schema}
                    
        "400":
          description: wrong request params
'''

DELETE_ROWS = '''  /crud/{table_name}/delete/:
    post:
      summary: Delete rows from {table_name} table by ids
      description: Delete rows from {table_name} by ids
      produces:
        - application/json
      tags:
        - {table_name}
      parameters:
        - in: body
          description: the array of ids to delete
          name: list of ids
          schema:
            type: array
            items:
              type: integer
      responses:
        200:
          description: OK
          schema:
            type: object
            properties:
              deleted_rows:
                type: integer
                example:
                  1
        "400":
          description: wrong request params
'''

UPDATE_ROWS = '''  /crud/{table_name}/update/:
    post:
      summary: Update existing rows in {table_name} table by ids
      description: Update existing rows in {table_name} table by ids
      produces:
        - application/json
      tags:
        - {table_name}
      parameters:
        - in: body
          name: {table_name} rows
          description: the array of {table_name} rows to update by ids
          {schema}
      responses:
        200:
          description: OK
          schema:
            type: object
            properties:
              updated_rows:
                type: integer
                example:
                  1
        "400":
          description: wrong request params
'''
