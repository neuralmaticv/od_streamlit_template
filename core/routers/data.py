from fastapi import APIRouter

# TODO: Add your API routes here.
data_router = APIRouter(
    prefix="/data",
    tags=["data"],
)

@data_router.get("/")
async def index():
    return {"message": "Data"}
