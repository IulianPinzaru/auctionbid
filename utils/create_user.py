import bcrypt

from db.models import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_user(db, user):
    db_user = None
    try:
        db_user = User(**{
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hash_password(user.password),
            "role": user.role
        })
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        print(f"[create_user] Something went wrong: {e}")
        db_user = None
    finally:
        return db_user
