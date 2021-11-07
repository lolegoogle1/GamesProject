from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from . import Base, session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)

    password = Column(String, nullable=False)
    type = Column(String)

    reviews = relationship("Review", back_populates="user")


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    founded_date = Column(Date, nullable=False)

    games = relationship("Game", back_populates="companies")

    @classmethod
    def get_companies(cls):
        try:
            companies = cls.query.all()
            session.commit()
            return companies
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, company_id):
        try:
            company = cls.query.filter(Company.id == company_id).first()
            if not company:
                raise Exception('No such company!')
            return company
        except Exception:
            session.rollback()
            raise

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        print(self)
        session.commit()

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    description = Column(String)
    release_date = Column(Date, nullable=False)

    companies = relationship("Company", back_populates="games")
    reviews = relationship("Review", back_populates="game")
    screenshots = relationship("Screenshot", back_populates="game")


class Screenshot(Base):
    __tablename__ = 'screenshots'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    file_name = Column(String)
    thumbnail_name = Column(String)

    game = relationship("Game", back_populates="screenshots")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    rating = Column(String, nullable=False)

    game = relationship("Game", back_populates="reviews")
    user = relationship("User", back_populates="reviews")