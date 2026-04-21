# Big Dipper

Big Dipper is a data-driven travel agency management platform built by the
NorthStar Travelers team for CS 3200 at Northeastern University.

The application connects travelers, planners, agency managers, and vendors in
one system. Trip planning is often spread across emails, spreadsheets, and
third-party booking tools; Big Dipper centralizes traveler preferences, vendor
inventory, trip planning, booking workflows, notifications, and operational
analytics so travel agencies can plan and manage trips more effectively.

## User Roles

- **Planner**: Builds itineraries, compares lodging and activity options, tracks
  trip budgets, and coordinates group trips with different traveler preferences.
- **Traveler**: Views trip details, submits food and lodging preferences, votes
  on proposed activities, saves listings, and receives trip notifications.
- **Vendor**: Manages listings and promotions, keeps offerings accurate, and
  monitors booking demand and engagement.
- **Manager**: Reviews booking trends, spending patterns, vendor performance,
  destination demand, and data quality across the platform.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask REST API
- **Database**: MySQL 9
- **Infrastructure**: Docker Compose
- **Local development language**: Python 3.11

## Repository Structure

- `app/`: Streamlit frontend application.
- `app/src/pages/`: Role-specific Streamlit pages for travelers, planners,
  vendors, managers, admins, and the About page.
- `api/`: Flask REST API and backend application code.
- `api/backend/northstar/`: Big Dipper API routes, endpoint logic, validation,
  and response helpers.
- `database-files/`: SQL files used to create and seed the `Northstar` MySQL
  database. These run in alphabetical order when the database container is first
  created.
- `datasets/`: Project datasets, if needed.
- `docker-compose.yaml`: Team development Docker Compose stack.
- `sandbox.yaml`: Optional personal sandbox Docker Compose stack with alternate
  host ports.

## Prerequisites

- Git and access to this repository.
- Docker Desktop or Docker Engine with Docker Compose.
- A Python distribution. The course-supported options are
  [Anaconda](https://www.anaconda.com/download) or
  [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install).
- VS Code with the Python extension, or another Python editor.

## Initial Setup

### 1. Create the local Python environment

Create a Python 3.11 Conda environment named `db-proj`:

```bash
conda create -n db-proj python=3.11
conda activate db-proj
```

Install the backend and frontend Python dependencies into that environment:

```bash
cd api
pip install -r requirements.txt
cd ../app/src
pip install -r requirements.txt
cd ../..
```

The application runs in Docker, but installing dependencies locally lets your
editor provide autocomplete, linting, import resolution, and error highlighting.

### 2. Create the API environment file

Create `api/.env` from the template:

```bash
cp api/.env.template api/.env
```

Then edit `api/.env` and replace the placeholder values:

```env
SECRET_KEY=<change-this-to-a-random-secret>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=Northstar
MYSQL_ROOT_PASSWORD=<change-this-to-a-strong-password>
```

Do not reuse a password from another service.

## Running the Project

Use the team Docker Compose stack for normal development:

```bash
docker compose up -d
```

After the containers start, open:

- Streamlit app: `http://localhost:8501`
- Flask API: `http://localhost:4000`
- MySQL from your host machine: `localhost:3200`

Useful Docker commands:

```bash
# Start all containers in the background
docker compose up -d

# Stop and remove the containers
docker compose down

# Start only one service, such as db, api, or app
docker compose up db -d

# Stop containers without deleting them
docker compose stop

# Restart containers after a crash or config change
docker compose restart
```

You can also use Docker Desktop to start, stop, inspect, and view logs for the
containers.

## Optional Personal Sandbox

The sandbox stack uses alternate host ports so it can run separately from the
main team stack:

```bash
# Start all sandbox containers in the background
docker compose -f sandbox.yaml up -d

# Stop and remove sandbox containers
docker compose -f sandbox.yaml down

# Start only one sandbox service, such as db, api, or app
docker compose -f sandbox.yaml up db -d

# Stop sandbox containers without deleting them
docker compose -f sandbox.yaml stop
```

Sandbox URLs and ports:

- Streamlit app: `http://localhost:8502`
- Flask API: `http://localhost:4001`
- MySQL from your host machine: `localhost:3201`

## Development Notes

- The Streamlit app and Flask API source directories are mounted into their
  containers, so most code changes hot reload after files are saved.
- In Streamlit, click **Always Rerun** in the browser when prompted so frontend
  changes refresh automatically.
- If a code error causes a container to stop, fix the bug and restart the
  affected container in Docker Desktop or run `docker compose restart`.
- The app container talks to the API over the Docker network on port `4000`.
- The API talks to MySQL using the values in `api/.env`.

## Database Initialization and Reset

When the MySQL container is created for the first time, it runs the SQL files in
`database-files/` in alphabetical order. The current database is named
`Northstar` and includes DDL plus sample data for planners, travelers, vendors,
trips, notifications, promotions, listings, bookings, funding requests,
preferences, amenities, and votes.

If you change any SQL file in `database-files/`, recreate the MySQL container
and volume so the initialization scripts run again:

```bash
docker compose down db -v && docker compose up db -d
```

For the sandbox stack, use:

```bash
docker compose -f sandbox.yaml down db -v && docker compose -f sandbox.yaml up db -d
```

Check the MySQL container logs in Docker Desktop if database initialization
fails. SQL errors usually appear there.

## Team

NorthStar Travelers:

- Laurence Ehrhardt: Point Person
- Gaurav Koratagere: Traveler Persona
- Kavya Karthik: Planner Persona
- Simon Coleman: Manager Persona
- Gabrielle Tugano: Vendor Persona

## Course

CS 3200, Northeastern University, Spring 2026.
