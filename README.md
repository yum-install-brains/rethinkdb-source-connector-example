# RethinkDB
RethinkDB is built to store JSON documents, and scale to multiple machines with very little effort. 
It has a pleasant query language that supports really useful queries like table joins and group by, 
and is easy to setup and learn.

For additional info visit https://rethinkdb.com/docs/rethinkdb-vs-mongodb/ and https://rethinkdb.com/docs/comparison-tables.

# Demo
1. Install project
```bash
git clone https://github.com/yum-install-brains/rethinkdb-source-connector-example.git \
&& cd rethinkdb-source-connector-example 
```

2. Start app, RethinkDB, Kafka, Zookeeper and Connect: `docker-compose up --build`

3. Add some data to be replicated from RethinkDB to Kafka: http://localhost:5000/

4. Check if data is written to RethinkDB in admin console: http://localhost:8080/#tables/

5. Start source connector `docker exec -it connect ./start_connector.sh | jq '.'`

6. Check if data is replicated to Kafka
```bash
docker exec -it kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic rethinkdb.connector.demo \
--from-beginning > result.json
```

7. Show result 
```bash
cat result.json | jq  '.payload.new_val'
```

8. Tear down
```bash
docker-compose down -v
```

# Connect CheatSheet
Check connect status
```bash
curl localhost:8083/ | jq '.'
curl localhost:8083/connector-plugins | jq '.'
```

Check active connectors
```bash
curl localhost:8083/connectors | jq '.'
curl localhost:8083/connectors/rethinkdb-connector/status | jq '.'
```

Start new connector
```bash
curl -X POST -H "Content-Type: application/json" \
    --data "@create-connector.json" \
    http://localhost:8083/connectors | jq '.'
```

Update connector
```bash
curl -X PUT -H "Content-Type: application/json" \
    --data "@create-connector.json" \
    http://localhost:8083/connectors/rethinkdb-connector/config | jq '.'
```

Delete connector
```bash
curl -X DELETE localhost:8083/connectors/rethinkdb-connector
```


# License #
This demo application is licensed under the MIT license: <http://opensource.org/licenses/mit-license.php> 
and based on repo https://github.com/rethinkdb/rethinkdb-example-flask-backbone-todo.git
