from fastapi import APIRouter

router = APIRouter(tags=["order"])


@router.get("/orders")
async def get_orders():

    return {"message": "success orders"}
