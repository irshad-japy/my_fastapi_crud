Explanation:
1. FastAPI app:
Defines CRUD operations for a User model.
Uses SQLAlchemy for database interaction.
Uses Depends to inject database session into routes.
2. Dockerfile:
Builds a Docker image based on Python 3.9-slim.
Installs dependencies from requirements.txt.
Copies the app code into the image.
Sets the command to start the Uvicorn server.
3. docker-compose.yml:
Defines two services: app and db.
app service builds and runs the FastAPI app.
db service uses the official MySQL image.
Exposes port 8000 for the app and 3306 for the database.
4. Build and run using Docker Compose:
   a. docker-compose up -d
   b. docker-compose up --build
   
5. to check sql connection in docker or not
docker-compose exec db mysql -u pocuser -p

http://localhost:8000/docs#/
http://localhost:8000/graphql

docker-compose down -v  # Clean slate
docker-compose up --build -d

6. run react frontent goto cd view and use below command
npm install
npm run dev

Note: If you face access denied for user then run below command.
docker-compose rm -v
References:https://github.com/docker-library/mysql/issues/51

Note: To login to mysql docker container use below command
> mysql -u pocuser -p
> Enter Password: rootpassword

Note: Redis related commands
1. To find keys
> redis-cli KEYS '*'

2. To list all keys
> redis-cli KEYS 'user:*'

References Token:
https://www.youtube.com/watch?v=hKoD29eYvKY
https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f

-----------------------------------------------------------------------------------------------------
1. build only mysql on docker below is the command
docker-compose down -v  # Clean slate
docker-compose up -d

2. for mysql and redis credential refer .env file which is not commited in github:
DB_USER=pocuser
DB_PASSWORD=rootpassword
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=test_db
REDIS_HOST=localhost
REDIS_PORT=6379

3. Run FastAPI app locally (outside Docker)
uvicorn app.main:app --reload

4. access running port below 
REST: http://localhost:8000/docs
GraphQL: http://localhost:8000/graphql

5. to run react code below is the command
npm run dev

6. To run graphql query use below query example
# to get data
query {
  products {
    id
    name
    price
  }
}

# create product
mutation {
  createProduct(name: "New Laptop", price: 999099) {
    id
    name
    price
  }
}

# to update data
mutation {
  updateProduct(id: 1, name: "Updated Phone", price: 5555) {
    id
    name
    price
  }
}

# delete data
mutation {
  deleteProduct(id: 1)
}