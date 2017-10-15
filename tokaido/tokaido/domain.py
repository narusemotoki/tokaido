import logging
from typing import (
    List,
    Set,
)

import tokaido.models


logger = logging.getLogger(__name__)


class Step:
    @classmethod
    def all(cls) -> List[tokaido.models.Step]:
        return list(tokaido.models.Step.all())

    @classmethod
    def create(cls, title: str) -> tokaido.models.Step:
        return tokaido.models.Step.create(title)

    @classmethod
    def get(cls, id: int) -> tokaido.models.Step:
        return tokaido.models.Step.find_by_id(id)

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
