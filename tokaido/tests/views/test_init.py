import unittest.mock

import pyramid.testing

import tokaido.views


@unittest.mock.patch('tokaido.domain.index')
def test_hello_world(mock_index):
    steps = [
        unittest.mock.MagicMock(id=1)
    ]

    expected = {
        'steps': steps
    }
    mock_index.return_value = steps

    response = tokaido.views.index(pyramid.testing.DummyRequest())
    assert response == expected
