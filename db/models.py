import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from db.database import Base


class AuctionStatus(str, enum.Enum):
    active = "active"
    closed = "closed"
    finished = "finished"


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(SQLAEnum(UserRole), default=UserRole.user)
    password = Column(String)

    bids = relationship("Bid", back_populates="user")


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    description = Column(String)
    status = Column(SQLAEnum(AuctionStatus), default=AuctionStatus.active)
    start_price = Column(Float)
    current_price = Column(Float)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    bids = relationship("Bid", back_populates="auction")


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    auction = relationship("Auction", back_populates="bids")
    user = relationship("User", back_populates="bids")
