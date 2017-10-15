from sqlalchemy import (
    Column,
    ForeignKey,
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


class NextStep(Base):  # type: ignore
    __tablename__ = 'next_steps'

    step_id = Column(ForeignKey('steps.id'), primary_key=True)
    next_step_id = Column(ForeignKey('steps.id'), primary_key=True)


class Step(Base):  # type: ignore
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)

    next_steps = sqlalchemy.orm.relationship(
        NextStep, lazy='joined', primaryjoin=id == NextStep.step_id)


def mark_changed() -> None:
    zope.sqlalchemy.mark_changed(DBSession())
