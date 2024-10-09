# Real-Estate-Estimator


## Getting Started

To set up and run the project, follow these steps:

1. Ensure Docker is installed on your machine.
2. Start Docker.
3. Open a terminal and navigate to the project directory.
4. Run the following commands:

   ```bash
   docker-compose down
   docker-compose up --build
This will start the application. Once it's running, open your web browser and go to http://localhost:5000.

### Environment Configuration
Before starting the application, create a .env file in the project directory with the following keys and structure:

```ini
# configurations used by the docker compose file

WEB_PORT=5000
DB_PORT=3306
INIT_FILE=./resources
HOSTNAME=test1
MYSQL_DATABASE=ree
MYSQL_ROOT_PASSWORD=changeme
MYSQL_USER=dbuser1
MYSQL_PASSWORD=changeme
SCHEMA=ree
SECRET_KEY=my_secret_key_here
```
