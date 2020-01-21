# What is it #

A demo web application in the spirit of [TodoMVC](http://addyosmani.github.com/todomvc/) showing how to use **RethinkDB as a backend for Flask and Backbone.js applications**.

As any todo application, this one implements the following functionality:

* Managing database connections
* List existing todos
* Create new todo
* Retrieve a single todo
* Edit a todo or mark a todo as done
* Delete a todo

One feature we've left out as an exercise is making this Flask todo app force  users to complete their tasks. In time.

# Complete stack #

* [Flask](http://flask.pocoo.org)
* [Backbone](http://backbonejs.org)
* [RethinkDB](http://www.rethinkdb.com)

# Installation #

```
git clone git://github.com/rethinkdb/rethinkdb-example-flask-backbone-todo.git
pip install Flask
pip install rethinkdb
```

# Start RethinkDB #

Make sure you have RethinkDB running.  
If you are not running RethinkDB on your local machine with the default settings,
update the `todo.py` file on lines 21 and 22.

_Note_: If you don't have RethinkDB installed, you can follow [these instructions to get it up and running](http://www.rethinkdb.com/docs/install/). 



# Running the application #



Firstly we'll need to create the database `todoapp` and the table used by this app: `todos`. You can
do this by running:

```
python todo.py --setup
```

Flask provides an easy way to run the app:

```
python todo.py
```

Then open a browser: <http://localhost:5000/>.

# Connect
check connect status
```bash
curl localhost:8083/ | jq '.'
curl localhost:8083/connector-plugins | jq '.'
```

check active connectors
```bash
curl localhost:8083/connectors
curl localhost:8083/connectors/rethinkdb-connector/status

```

start new connector
```bash
curl -X POST -H "Content-Type: application/json" --data "@create-connector.json" http://localhost:8083/connectors

```

update connector
```bash
curl -X PUT -H "Content-Type: application/json" --data "@create-connector.json" http://localhost:8083/connectors/rethinkdb-connector/config

```

start new task
```bash
curl localhost:8083/connectors/local-file-sink/tasks | jq
[
  {
    "id": {
      "connector": "local-file-sink",
      "task": 0
    },
    "config": {
      "task.class": "org.apache.kafka.connect.file.FileStreamSinkTask",
      "topics": "connect-test",
      "file": "test.sink.txt"
    }
  }
]
```

delete connector
```bash
curl -X DELETE localhost:8083/connectors/rethinkdb-connector
```

# Kafka
List topics
```bash

```

Read from topic
```bash
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic rethinkdb-todo-topic \
--from-beginning
```


# Demo
```bash
docker-compose up --build
```

```bash
docker exec -it connect bash
curl -X POST -H "Content-Type: application/json" --data "@create-connector.json" http://localhost:8083/connectors
```

add some todos http://localhost:5000/

check if data is written to rethinkdb http://localhost:8080/#tables/

check if data is in kafka
```bash
docker exec -it rethinkdb-source-connector-example_kafka_1 bash

kafka-topics --zookeeper zookeeper:2181 --list

kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic rethinkdb-todo-topic \
--from-beginning
```

# License #

This demo application is licensed under the MIT license: <http://opensource.org/licenses/mit-license.php>
