from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from basemodels.bidserializer import BidCreate
from db.database import get_db
from utils.create_bid import place_bid
from utils.jwt import get_current_user

router = APIRouter(prefix="/api/bids")


@router.post("/{auction_id}/", tags=["bids"])
def create_bid(auction_id: int, bid: BidCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    bid = place_bid(db=db, auction_id=auction_id, user_id=user.id, bid=bid)
    if not bid:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={
                                "message": "Something went wrong while creating the user. Please try again later."})
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Bid placed."})
