 
from fastapi import FastAPI 
from preferred_item_service.utils.logger import custom_logger 
from fastapi_route_logger_middleware import RouteLoggerMiddleware

from preferred_item_service.app.preferreditem_service import router as pis_router
from preferred_item_service.app.item_service import router as item_router 
from preferred_item_service.app.masterdata_service import router as masterdata_router 
 
from mangum import Mangum 

logger = custom_logger(__file__)
app = FastAPI(
    description="Preferred Item Service",
    version="0.1",
    title="Preferred Item Service",
)
# # Include routers from each endpoint file
# app.include_router(brick_router, prefix="/bricks", tags=["Bricks"])
app.include_router(item_router, prefix="/items", tags=["Items"])
app.include_router(masterdata_router, prefix="/masterdata", tags=["Master Data"])
app.include_router(pis_router, prefix="/preferreditem", tags=["Preferred Item"])

logger.info("Handler start") 
app.add_middleware(RouteLoggerMiddleware)

handler = Mangum(app, lifespan="off") 

