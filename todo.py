import argparse
import json
import os

from flask import Flask, g, jsonify, render_template, request, abort

from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = RethinkDB()

RDB_HOST = os.environ.get('RDB_HOST') or '0.0.0.0'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
DEMO_DB = 'demo_db'

def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(DEMO_DB).run(connection)
        r.db(DEMO_DB).table_create('demo_table').run(connection)
        print('Database setup completed. Now run the app without --setup.')
    except RqlRuntimeError:
        print('App database already exists. Run the app without --setup.')
    finally:
        connection.close()


app = Flask(__name__)
app.config.from_object(__name__)


#### Managing connections

# The pattern we're using for managing database connections is to have **a connection per request**. 
# We're using Flask's `@app.before_request` and `@app.teardown_request` for 
# [opening a database connection](http://www.rethinkdb.com/api/python/connect/) and 
# [closing it](http://www.rethinkdb.com/api/python/close/) respectively.
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=DEMO_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


#### Listing existing todos

# To retrieve all existing tasks, we are using
# [`r.table`](http://www.rethinkdb.com/api/python/table/)
# command to query the database in response to a GET request from the
# browser. When `table(table_name)` isn't followed by an additional
# command, it returns all documents in the table.
#    
# Running the query returns an iterator that automatically streams
# data from the server in efficient batches.
@app.route("/todos", methods=['GET'])
def get_todos():
    selection = list(r.table('demo_table').run(g.rdb_conn))
    return json.dumps(selection)


#### Creating a todo

# We will create a new todo in response to a POST request to `/todos`
# with a JSON payload using
# [`table.insert`](http://www.rethinkdb.com/api/python/insert/).
#
# The `insert` operation returns a single object specifying the number
# of successfully created objects and their corresponding IDs:
# 
# ```
# {
#   "inserted": 1,
#   "errors": 0,
#   "generated_keys": [
#     "773666ac-841a-44dc-97b7-b6f3931e9b9f"
#   ]
# }
# ```

@app.route("/todos", methods=['POST'])
def new_todo():
    inserted = r.table('demo_table').insert(request.json).run(g.rdb_conn)
    return jsonify(id=inserted['generated_keys'][0])


@app.route("/")
def show_todos():
    return render_template('todo.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Flask todo app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        dbSetup()
    else:
        app.run(host='0.0.0.0', debug=True)

#
# Licensed under the MIT license: <http://opensource.org/licenses/mit-license.php>
#
# Copyright (c) 2012 RethinkDB
#
