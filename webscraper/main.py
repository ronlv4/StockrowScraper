from fastapi import FastAPI

from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/{name}')
def greeting(name):
    return f'Hello {name}'
