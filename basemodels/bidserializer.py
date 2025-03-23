from datetime import datetime

from pydantic import BaseModel


class AuctionBids(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    price: float


class BidCreate(BaseModel):
    price: float
