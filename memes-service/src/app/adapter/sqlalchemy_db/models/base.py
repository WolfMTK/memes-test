from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
