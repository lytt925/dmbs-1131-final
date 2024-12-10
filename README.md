# DBMS 1131 Final Project

This project is a web application built using FastAPI for the server-side.<br/>
The presentation video is [here](https://youtu.be/5WRRdEJFbns).<br/>
screenshot of the system:<br/>
<img width="470" alt="image" src="https://github.com/user-attachments/assets/ff40257d-3699-4c39-be33-e59afa423d11">

## Running the Server

To run the server, you can follow these steps:

1. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   
2. Navigate to the server directory:
   ```sh
   cd ./server
   ```

3. Run the server using `uvicorn`:
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

   Alternatively, you can run the server using Python:
   ```sh
   python -m app.main
   ```
## Running the Client

To run the client, you can follow these steps:

1. Navigate to the client directory:
   ```sh
   cd ./client
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Navigate to the `client/app` directory:
   ```sh
   cd app
   ```

4. Run the client using Python:
   ```sh
   python3 main.py
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
