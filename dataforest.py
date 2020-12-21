from sqlalchemy import Column, String, Integer, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_URL = 'postgresql+psycopg2://postgres:[pg:p}P"xBq6HB;m@54.162.48.11:5432'


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    color = Column(String(16))
    price = Column(Integer)
    description = Column(String(256))


class DataBase:

    def __init__(self):
        self.engine = create_engine(f'{DB_URL}/postgres')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()
        logger.info('DATA BASE __init__')

    def save_row(self, row: dict, classname) -> None:
        try:
            row_for_save = classname(**row)
            self.session.add(row_for_save)
            self.session.commit()
            logger.info(f'{row}')
        except Exception as e:
            logger.debug(f'{e}')
            self.session.rollback()

    def get_all_rows(self, classname):
        logger.info(f'Start QUERY: {classname}')
        data = self.session.query(classname).all()
        logger.info(f'Return QUERY: {classname}')
        return data

    def save_many(self, rows, classname):
        logger.info(f'Start save for many: {classname}')
        self.session.bulk_save_objects(rows)


def start():
    db = DataBase()
    cars = ({'name': 'old bmw',
             'color': 'black',
             'price': 850,
             'description': 'car for young people'},
            {'name': 'old opel',
             'color': 'silver',
             'price': 800,
             'description': 'car for people'},
            {'name': 'old ferrari',
             'color': 'red',
             'price': 3000,
             'description': 'cool car'},
            {'name': 'old reno',
             'color': 'white',
             'price': 750,
             'description': 'car'},
            )
    rows = [Test(**kwargs) for kwargs in cars]
    db.save_many(rows=rows, classname=Test)


if __name__ == '__main__':
    start()
