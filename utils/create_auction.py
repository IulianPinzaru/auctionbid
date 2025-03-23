from basemodels.auctionserializer import AuctionCreate
from db.models import Auction


def create_auction(db, auction: AuctionCreate):
    db_auction = None
    try:
        db_auction = Auction(**auction.dict())
        db.add(db_auction)
        db.commit()
        db.refresh(db_auction)
    except Exception as e:
        print(f"[create_auction] Something went wrong: {e}")
        db_auction = None
    finally:
        return db_auction
