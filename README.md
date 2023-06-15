# Wine store flask application
_flask + postgres + mongodb(sharded) in docker-compose_

To run application follow this commands:
- To run build images and run docker-compsoe
```bash
docker-compose -f Docker/docker-compose.yaml up --build -d
```

- To apply mongo sharding:
```bash
docker exec -d cfgsvr1 mongosh /temp/init.js
docker exec -d shard1svr1 mongosh /temp/init.js
docker exec -d shard2svr1 mongosh /temp/init.js
docker exec -d mongos bash -c 'sleep 15; mongosh /temp/init.js'
```

Server runs on port 3000, you can access it from localhost with the same port

default login:password for regular user is asaprocky:qwerty1234;
default login:password for admin user is @prokhorkot:qwerty1234