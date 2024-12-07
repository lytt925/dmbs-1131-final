from fastapi import FastAPI
from app.database import db
import app.routers.user as user
import app.routers.care as care
import app.routers.registration as registration
import app.routers.shelter as shelter
import app.routers.animal as animal
import app.routers.application as application
import app.routers.employee as employee

app = FastAPI()

@app.get("/test-connection")
async def test_connection():
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return {"message": "Connection successful!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}


# Register routers
app.include_router(user.router)
app.include_router(care.router)
app.include_router(registration.router)
app.include_router(shelter.router)
app.include_router(animal.router)
app.include_router(application.router)
app.include_router(employee.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)