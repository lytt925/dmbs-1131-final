# DBMS 1131 Final Project

This project is a web application built using FastAPI for the server-side.
The presentation video is [here](https://youtu.be/5WRRdEJFbns)

## Running the Server

To run the server, you can follow these steps:

1. Navigate to the server directory:
   ```sh
   cd ./server
   ```

2. Run the server using `uvicorn`:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

   Alternatively, you can run the server using Python:
   ```sh
   python -m app.main
   ```

## Modules Overview

### Main Application (`server/app/main.py`)

The main application includes several routers for different functionalities:

- **User Router**: Handles user-related operations.
- **Care Router**: Manages care-related functions.
- **Registration Router**: Deals with user activities registrations.
- **Shelter Router**: Manages shelter operations.
- **Animal Router**: Handles animal-related informations.
- **Application Router**: Manages adoption applications.
- **Employee Router**: Handles employee-related operations.
- **Activity Router**: Manages various activities.

### Mock Module

The mock folder is used for generating mock data in the database. 
