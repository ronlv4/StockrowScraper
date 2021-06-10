from fastapi import FastAPI
import uvicorn
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/about')
def about():
    return "Hello\nThis is a webscraper"

@app.get('/{name}')
def greeting(name):
    return f'Hello {name}'


if __name__ == '__main__':
    uvicorn.run(app,port=9000)  # for debug purposes
