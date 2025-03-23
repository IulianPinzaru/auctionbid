from fastapi import FastAPI

from api import user, bid, auction
from db import models, database
from workers.auction_worker import AuctionWorker

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(bid.router)
app.include_router(auction.router)


@app.on_event("startup")
async def startup_event():
    # No time to use celery for cron jobs.
    auction_worker = AuctionWorker()
    auction_worker.start()
