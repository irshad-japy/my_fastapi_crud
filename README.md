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