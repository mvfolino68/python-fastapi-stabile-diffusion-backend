from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from image import config
from image.routers import router as v1
from image.services.repository import get_mongo_meta
from image.utils import get_logger, init_mongo
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


global_settings = config.get_settings()

if global_settings.environment == "local":
    get_logger("uvicorn")


app = FastAPI()

app.include_router(v1, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    app.state.logger = get_logger(__name__)
    app.state.logger.info("Starting image generator...mmm")
    (
        app.state.mongo_client,
        app.state.mongo_db,
        app.state.mongo_collection,
    ) = await init_mongo(
        global_settings.db_name, global_settings.db_url, global_settings.collection
    )

    # set up limiter for api calls
    limiter = Limiter(key_func=get_remote_address, default_limits=["2/minutes"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("shutdown")
async def shutdown_event():
    app.state.logger.info("Parking tractors in garage...")


@app.get("/health-check")
async def health_check():
    # # TODO: check settings dependencies passing as args and kwargs
    # a = 5
    # try:
    #     assert 5 / 0
    # except Exception:
    #     app.state.logger.exception("My way or highway...")
    return await get_mongo_meta()
