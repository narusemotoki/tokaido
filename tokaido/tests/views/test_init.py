import unittest.mock

import pyramid.testing

import tokaido.views


@unittest.mock.patch('tokaido.domain.Step.all')
def test_index(mock_index):
    steps = [
        unittest.mock.MagicMock(id=1)
    ]

    expected = {
        'steps': steps
    }
    mock_index.return_value = steps

    response = tokaido.views.index(pyramid.testing.DummyRequest())
    assert response == expected
