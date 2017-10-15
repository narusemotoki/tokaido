from typing import (
    Iterator,
)

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import zope.sqlalchemy

import tokaido.exceptions


DBSession = sqlalchemy.orm.scoped_session(
    sqlalchemy.orm.sessionmaker(
        extension=zope.sqlalchemy.ZopeTransactionExtension(),
        expire_on_commit=False
    )
)
Base = sqlalchemy.ext.declarative.declarative_base()


class NextStep(Base):  # type: ignore
    __tablename__ = 'next_steps'

    step_id = Column(ForeignKey('steps.id'), primary_key=True)
    next_step_id = Column(ForeignKey('steps.id'), primary_key=True)

    @classmethod
    def create(cls, step_id: int, next_step_id: int) -> 'NextStep':
        next_step = cls(step_id=step_id, next_step_id=next_step_id)
        DBSession.add(next_step)
        DBSession.flush()

        return next_step

    def delete(self) -> None:
        DBSession.delete(self)


class Step(Base):  # type: ignore
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)

    next_steps = sqlalchemy.orm.relationship(
        NextStep, lazy='joined', primaryjoin=id == NextStep.step_id)

    @classmethod
    def create(cls, title: str) -> 'Step':
        step = cls(title=title)
        DBSession.add(step)
        DBSession.flush()

        return step

    @classmethod
    def find_by_id(cls, id: int) -> 'Step':
        step = DBSession.query(cls).get(id)
        if step:
            return step
        raise tokaido.exceptions.ResourceNotFoundError()

    @classmethod
    def all(cls) -> Iterator['Step']:
        return DBSession.query(cls).all()


def mark_changed() -> None:
    zope.sqlalchemy.mark_changed(DBSession())
