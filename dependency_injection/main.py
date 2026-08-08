from fastapi import FastAPI, Depends

app = FastAPI()


def get_message():
    return "Hello from Dependency"


@app.get("/")
def home(message: str = Depends(get_message)):
    return {"message": message}