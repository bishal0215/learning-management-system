from database import SessionLocal
import models, utils
def init_admin():
    db = SessionLocal()
    try:
        admin= db.query(models.DBUser).filter(models.DBUser.is_superuser==True).first()

        if not admin:
            hashed_pwd = utils.hash_password("admin12345")
            default_admin = models.DBUser(
                username="admin",
                email="admin@gov.com",
                password= hashed_pwd,
                is_superuser= True
            )
            db.add(default_admin)
            db.commit()
            print("--- Default Admin Created (username: admin, password: admin12345) ---")
    finally:
        db.close()