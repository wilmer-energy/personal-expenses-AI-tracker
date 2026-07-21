from fastapi import FastAPI

app = FastAPI(title="Personal Expenses Tracker")


@app.get("/")
def hello_world():
    return "Hello world"
