import logging
from typing import (
    List,
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

    return [step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8, step_9, step_10]
