# # from sqlalchemy.orm import relationship
# # from sqlalchemy import Column, Integer, String
# # from database.db import Base
# #
# #
# # class User(Base):
# #     """
# #     Класс для хранения ключей шифрования в БД
# #     """
# #     __tablename__ = 'users'
# #     id = Column(Integer, primary_key=True, index=True)
# #     email = Column(String, nullable=False, unique=True)
# #     password = Column(String, nullable=False)
# #
# #     messages = relationship('MessageCipher', back_populates='user')
# from datetime import datetime
#
# from sqlalchemy import Column, Table, Integer, String, TIMESTAMP
#
# from database.db import metadata
#
# user = Table(
#     'user',
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("register_date", TIMESTAMP, default=datetime.utcnow),
# )
