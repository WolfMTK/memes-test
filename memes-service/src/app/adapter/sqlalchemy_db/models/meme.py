import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.sqlalchemy_db.models import BaseModel


# INFO: я бы еще дополнил другим функционалом, например, категориями
# (М:М связь тогда была бы).
class Meme(BaseModel):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        autoincrement=False
    )
    text: Mapped[str] = mapped_column(
        nullable=False,
        comment='Текст мема'
    )
    image: Mapped[str] = mapped_column(
        nullable=False,
        comment='Название файла с изображением'
    )
    url_image: Mapped[str] = mapped_column(
        nullable=False,
        comment='Ссылка на изображение'
    )
