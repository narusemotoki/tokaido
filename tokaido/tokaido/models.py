from typing import (
    List,
)

from sqlalchemy import (
    Column,
    Integer,
    Text,
)
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import zope.sqlalchemy


DBSession = sqlalchemy.orm.scoped_session(
    sqlalchemy.orm.sessionmaker(
        extension=zope.sqlalchemy.ZopeTransactionExtension(),
        expire_on_commit=False
    )
)
Base = sqlalchemy.ext.declarative.declarative_base()


class Step(Base):  # type: ignore
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    next_steps: List['Step'] = []


def mark_changed() -> None:
    zope.sqlalchemy.mark_changed(DBSession())
