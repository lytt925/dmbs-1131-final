cd ./server

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

or 

python -m app.main