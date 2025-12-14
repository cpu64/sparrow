# Sparrow Docker Setup

This project uses Docker to set up a Flask application with a PostgreSQL database. The following instructions will guide you through building and running the containerized application.

## Prerequisites

Ensure you have Docker installed on your machine. If you don't, follow the instructions in the [Docker documentation](https://docs.docker.com/get-docker/) to install it.

You'll also need Google Cloud Storage secrets file `gcs-key.json` placed in `./app` directory.
To adjust different GCS credential or bucket variables adjust these `Dockerfile` lines:
```
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcs-key.json \
    GCS_BUCKET_NAME=sparrow-flask-images-2025
```

## Build the Docker Image

To build the Docker image for the application, run the following command in the root directory of the project:

```bash
docker build -t cpu64/sparrow .
```

This will build the image using the Dockerfile in the current directory.
## Running the Application
Base Run Command

Once the image is built, you can run the application with this base command:

```bash
docker run -p 5000:5000 cpu64/sparrow
```

This will expose the Flask application on port 5000.
## Additional Options

You can customize the Docker run command with the following options:
```bash
docker run \
  --name sparrow \                # Name of the container
  -it \                           # Interactive terminal (for debugging or running commands inside)
  --rm \                          # Automatically remove the container when it stops
  -v ./app:/app \                 # Mount the app directory for live updates (use during development)
  -v ./db:/db \                   # Mount the db directory to persist data
  -v ./db/init:/db/init \         # Mount the db/init directory to initialize the database using ./db/init/init.sql (not needed if -v ./db:/db is used)
  -p 5432:5432 \                  # Expose PostgreSQL port 5432 to view the database outside the container (default configuration below)
  -e PGDATABASE=sparrow \         # PostgreSQL database name
  -e PGUSER=sparrow \             # PostgreSQL user
  -e PGPASSWORD=overwriteme \     # PostgreSQL password (change this in production)
  -e PGHOST=localhost \           # PostgreSQL host (should be localhost if running within the same container)
  -e PGPORT=5432 \                # PostgreSQL port (should match the exposed PostgreSQL port "-p 5432:5432")
  -p 5000:5000 \                  # Expose Flask port 5000
  -e FLASK_HOST=0.0.0.0 \         # Bind Flask to all network interfaces (required for Docker deployment)
  -e FLASK_PORT=5000 \            # Flask port (should match the exposed Flask port "-p 5000:5000")
  cpu64/sparrow
```
### Example Commands

Development example command using db/init/init.sql, but without persistant database:
```bash
docker run --name sparrow -it --rm -v ./app:/app -v ./db/init:/db/init -p 5432:5432 -p 5000:5000 cpu64/sparrow
```
Development example command using db/init/init.sql, with persistant database:
```bash
docker run --name sparrow -it --rm -v ./app:/app -v ./db:/db -p 5432:5432 -p 5000:5000 cpu64/sparrow
```
Development example command, with different ports:
```bash
docker run --name sparrow -it --rm -v ./app:/app -p 6000:5432 -p 7000:5432 cpu64/sparrow
```
Producion example command, with db/init/init.sql for dummy data:
```bash
docker run --name sparrow -it --rm -v ./db/init:/db/init -p 5432:5432 -p 5000:5000 cpu64/sparrow
```
Running bash shell inside the container instead of Flask:
```bash
docker run -it --rm -p 5432:5432 -p 5000:5000 cpu64/sparrow bash
```

### Notes
> [!CAUTION]
> Make sure to change the PGPASSWORD environment variable to something secure for production.
