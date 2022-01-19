from fastapi import FastAPI

from controller import item, warehouse, inventory

app = FastAPI(
    title="Inventory Tracker",
    version="0.1",
    contact={
        "name": "Aasif Faizal",
        "url": "https://github.com/aasiffaizal",
        "email": "aasif.faizal@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/aasiffaizal/inventory_tracker/blob/main/LICENSE",
    },
)
app.include_router(item.router)
app.include_router(warehouse.router)
app.include_router(inventory.router)


@app.get("/")
async def root():
    return {
        "message": "Index Page. Please checks /docs to get the info of APIs"
    }
