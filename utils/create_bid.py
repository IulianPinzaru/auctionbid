from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from basemodels.bidserializer import BidCreate
from db.models import Auction, Bid


def place_bid(db: Session, auction_id: int, user_id: int, bid: BidCreate):
    auction = db.execute(
        select(Auction).where(Auction.id == auction_id).with_for_update()).scalar_one_or_none()

    if not auction:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Auction not found"})

    if auction.status != "active":
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Auction is not active"})

    if auction.current_price is None:
        auction.current_price = bid.price
    elif bid.price <= auction.current_price:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Bid must be higher than current price"})

    new_bid = Bid(user_id=user_id, auction_id=auction_id, price=bid.price)
    db.add(new_bid)

    auction.current_price = bid.price

    try:
        db.commit()
        db.refresh(new_bid)
        return new_bid
    except IntegrityError:
        db.rollback()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Bid must be higher than current price"})
