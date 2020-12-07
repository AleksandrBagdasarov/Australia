from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


class DataBase:

    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/australia')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()
        logger.info('DATA BASE __init__')

    async def save_row(self, row: dict, classname) -> None:
        try:
            row_for_save = classname(**row)
            self.session.add(row_for_save)
            self.session.commit()
            logger.info(f'{row}')
        except Exception as e:
            logger.debug('already exist')
            # logger.debug(f'{e}')
            self.session.rollback()

    def get_all_rows(self, classname):
        logger.info(f'Start QUERY: {classname}')
        data = self.session.query(classname).all()
        logger.info(f'Return QUERY: {classname}')
        return data

    def get_rows(self, classname, row_limit, filter_):
        # logger.info(f'Start QUERY: {classname}')
        data = self.session.query(classname).order_by(classname.id).filter(filter_).limit(row_limit)
        # logger.info(f'Return QUERY: {classname}')
        return data
