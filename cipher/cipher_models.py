# # from sqlalchemy import Column, Integer, ForeignKey, String
# # from sqlalchemy.orm import relationship
# #
# # from database.db import Base
# #
# #
# # class MessageCipher(Base):
# #     """
# #     Класс для хранения зашифрованных сообщений в БД
# #     """
# #     __tablename__ = 'message_cipher'
# #     id = Column(Integer, primary_key=True, index=True)
# #     cipher_message = Column(String, nullable=False)
# #     key_cipher = Column(String, nullable=False)
# #     pass_phrase = Column(String, nullable=False)
# #     url = Column(String, nullable=False)
# #
# #     user_id = Column(Integer, ForeignKey("users.id"))
# #     user = relationship("User", back_populates="messages")
#
# from sqlalchemy import Column, Table, Integer, String, ForeignKey
#
# from database.db import metadata
#
# cipher = Table(
#     'cipher',
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("cipher_message", String, nullable=False),
#     Column("key_cipher", String, nullable=False),
#     Column("pass_phrase", String, nullable=False),
#     Column("url", String, nullable=False),
#     Column("user_id", Integer, ForeignKey("user.id")),
# )
