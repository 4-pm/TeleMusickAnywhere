import sqlalchemy

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):  # класс добавляемойс трочки
    __tablename__ = 'profile'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # генерируемый id
    user_id = sqlalchemy.Column(sqlalchemy.String)  # id пользователя
    qr_back_image = sqlalchemy.Column(sqlalchemy.String)  # фон qr
    gif_back_image = sqlalchemy.Column(sqlalchemy.String)  # фон gif
    statistic = sqlalchemy.Column(sqlalchemy.String)  # статистика пользователя