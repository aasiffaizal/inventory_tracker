from fastapi import FastAPI
from controller import item, warehouse, inventory


app = FastAPI()
app.include_router(item.router)
app.include_router(warehouse.router)
app.include_router(inventory.router)


@app.get("/")
async def root():
    return {"message": "Index Page. Please checks /docs to get the info of APIs"}

