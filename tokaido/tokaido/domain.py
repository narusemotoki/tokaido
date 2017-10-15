import logging
from typing import (
    List,
    Set,
)

import tokaido.models


logger = logging.getLogger(__name__)


def index() -> List[tokaido.models.Step]:
    step_1 = tokaido.models.Step(id=1, title="Show graph with static HTML")
    step_2 = tokaido.models.Step(id=2, title="Show graph with on time generated objects")
    step_3 = tokaido.models.Step(id=3, title="Model class for SQLAlchemy")
    step_4 = tokaido.models.Step(id=4, title="API for adding step")
    step_5 = tokaido.models.Step(id=5, title="Show graph with database")
    step_6 = tokaido.models.Step(id=6, title="Interface for adding step")
    step_7 = tokaido.models.Step(id=7, title="Test database and Interface")
    step_8 = tokaido.models.Step(id=8, title="Setup TypeScript")
    step_9 = tokaido.models.Step(id=9, title="Extend model for link to Pivotal Tracker")
    step_10 = tokaido.models.Step(id=10, title="Extend interface for link to Pivotal Tracker")

    step_1.next_steps = [step_2]
    step_2.next_steps = [step_3]
    step_3.next_steps = [step_4]
    step_4.next_steps = [step_5, step_6]
    step_5.next_steps = [step_7]
    step_6.next_steps = [step_7]
    step_8.next_steps = [step_6]
    step_7.next_steps = [step_9]
    step_9.next_steps = [step_10]

    steps = [step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8, step_9, step_10]

    return steps


class Step:
    @classmethod
    def create(cls, title: str) -> tokaido.models.Step:
        return tokaido.models.Step.create(title)

    @classmethod
    def update(cls, id: int, title: str, next_step_ids: Set[int]) -> tokaido.models.Step:
        step = tokaido.models.Step.find_by_id(id)
        existing_next_step_ids = set()
        for next_step in step.next_steps:
            if next_step.next_step_id in next_step_ids:
                existing_next_step_ids.add(next_step.next_step_id)
            else:
                next_step.delete()

        for new_next_step_id in next_step_ids - existing_next_step_ids:
            tokaido.models.NextStep.create(step.id, new_next_step_id)

        step.title = title
        tokaido.models.DBSession.flush()
        tokaido.models.DBSession.refresh(step)

        return step
