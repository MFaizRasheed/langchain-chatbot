from fastapi import FastAPI

app = FastAPI()


# Post api is when you sign up
# Get api when you response
@app.get("/")  # buildin decorator
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
