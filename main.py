from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.products import router as products_router
from routers.orders import router as orders_router

app = FastAPI()

app.include_router(orders_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}