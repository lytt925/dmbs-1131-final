from fastapi import FastAPI
from app.database import db
import app.routers.user as user

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)