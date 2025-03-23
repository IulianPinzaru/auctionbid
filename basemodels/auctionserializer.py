from datetime import datetime

from pydantic import BaseModel


class AuctionCreate(BaseModel):
    item_name: str
    description: str
    start_price: float
    end_time: datetime


class AuctionResponse(BaseModel):
    id: int
    item_name: str
    description: str
    start_price: float
    status: str
    end_time: datetime
    created_at: datetime
