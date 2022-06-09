from fastapi import FastAPI

app = FastAPI()


@app.get(path='/')
def index():
    return {"message": "Hello World"}