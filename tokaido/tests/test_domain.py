import transaction

import tests
import tokaido.domain
import tokaido.models


class TestStep:
    def setup_method(self):
        tests.setup_db()

    def teardown_method(self):
        tests.teardown_db()

    def test_update(self):
        with transaction.manager:
            first_step_id = tokaido.domain.Step.create("first").id
            second_step_id = tokaido.domain.Step.create("second").id

        with transaction.manager:
            new_title = "updated first"
            updated_first = tokaido.domain.Step.update(
                first_step_id, new_title, {second_step_id})

            assert updated_first.id == first_step_id
            assert updated_first.title == new_title
            assert len(updated_first.next_steps) == 1
            assert updated_first.next_steps[0].next_step_id == second_step_id

    def test_all(self):
        with transaction.manager:
            step_id = tokaido.domain.Step.create("first").id

        with transaction.manager:
            steps = tokaido.domain.Step.all()
            assert len(steps) == 1
            assert steps[0].id == step_id
