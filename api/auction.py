from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from basemodels.auctionserializer import AuctionCreate, AuctionResponse
from basemodels.bidserializer import AuctionBids
from db.database import get_db
from db.models import Auction, Bid
from utils.create_auction import create_auction
from utils.jwt import get_current_user

router = APIRouter(prefix="/api/auctions")


@router.get("/", tags=["auction"])
def all_auctions(user=Depends(get_current_user)):
    # TODO filter would be nice, but no time right now
    db = next(get_db())
    auctions = db.query(Auction).all()
    if not auctions:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Auctions not found."})

    auction_list = [AuctionResponse(**auction.__dict__).dict() for auction in auctions]
    print(auction_list)
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"auctions": jsonable_encoder(auction_list)})


@router.get("/{auction_id}/", tags=["auction"])
def auction_details(auction_id: int, user=Depends(get_current_user)):
    db = next(get_db())

    auction = db.query(Auction).filter(Auction.id == auction_id).first()

    if not auction:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Auction not found."})

    bids = db.query(Bid).filter(Bid.auction_id == auction.id).all()
    if not bids:
        auction_bids = []
    else:
        auction_bids = [AuctionBids(**bid.__dict__).dict() for bid in bids]
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"auction": jsonable_encoder(AuctionResponse(**auction.__dict__)),
                                 "bids": jsonable_encoder(auction_bids)})


@router.get("/winner/{auction_id}/", tags=["auction"])
def auction_winner(auction_id: int, user=Depends(get_current_user)):
    db = next(get_db())

    auction = db.query(Auction).filter(Auction.id == auction_id).first()

    if not auction:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Auction not found."})

    if auction.status != "closed":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": "Auction in progress."})

    winner = db.query(Bid).filter(Bid.auction_id == auction.id).order_by(Bid.id.desc()).first()
    if not winner:
        winner = "No winner"
    else:
        winner = f"{winner.user.email} won the auction. The user bid was: {winner.price}"
    db.close()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"winner": winner})


@router.post("/new-auctions/", tags=["auction"])
def new_auction(auction: AuctionCreate, user=Depends(get_current_user)):
    db = next(get_db())

    auction = create_auction(db=db, auction=auction)
    if not auction:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={
                                "message": "Something went wrong while creating the user. Please try again later."})
    db.close()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Auction created."})
