from datetime import datetime
from multiprocessing import Process

from db.database import get_db
from db.models import Auction


class AuctionWorker(Process):
    def __init__(self):
        super(AuctionWorker, self).__init__()

        self.name = f"AuctionWorker"

    # override the run function
    def run(self):
        """
        Object thread run() method
        Returns no return
        -------
        """
        while True:
            db = next(get_db())
            try:
                auctions = db.query(Auction).filter(Auction.status == "active").all()

                for auction in auctions:
                    if datetime.utcnow() >= auction.end_time:
                        auction.status = "closed"

                db.commit()
            except Exception as e:
                print(f"[AuctionWorker] Something went wrong: {e}")
            finally:
                db.close()
