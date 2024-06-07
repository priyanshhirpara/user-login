from database import engine


from sqlalchemy.orm import sessionmaker


seessiolocal = sessionmaker(autoflush=False, bind=engine)
