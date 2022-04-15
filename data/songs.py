import sqlalchemy

from .db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):  # класс добавляемойс трочки
    __tablename__ = 'songs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # генерируемый id
    name = sqlalchemy.Column(sqlalchemy.String)  # название песни
    qr = sqlalchemy.Column(sqlalchemy.String)  # ее qr, удивительно да?
    song = sqlalchemy.Column(sqlalchemy.String)  # id песни
    text = sqlalchemy.Column(sqlalchemy.String, index=True)  # текст песни
    image = sqlalchemy.Column(sqlalchemy.String)  # фоточка, тут лежит гифка с диском
