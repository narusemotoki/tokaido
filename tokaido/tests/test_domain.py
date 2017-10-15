import tokaido.domain
import tokaido.models


def test_index():
    for step in tokaido.domain.index():
        assert isinstance(step, tokaido.models.Step)
