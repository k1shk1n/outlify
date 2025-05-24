from unittest.mock import Mock, patch

import pytest

from outlify.decorators import timer


@pytest.mark.unit
@pytest.mark.parametrize(
    'name,start,end,result',
    [
        (None, 1.0, 1.1, "Function 'dummy_func' took 00h 00m 00.100s"),
        ("TestFunc", 1.0, 1.5, "TestFunc took 00h 00m 00.500s"),

        ("fake", 0.0, 1.0, "fake took 00h 00m 01.000s"),
        ("fake", 0.0, 1.123, "fake took 00h 00m 01.123s"),
        ("fake", 0.0, 60.0, "fake took 00h 01m 00.000s"),
        ("fake", 0.0, 61.0, "fake took 00h 01m 01.000s"),
        ("fake", 0.0, 3600.0, "fake took 01h 00m 00.000s"),
        ("fake", 0.0, 3601.0, "fake took 01h 00m 01.000s"),
        ("fake", 0.0, 3660.0, "fake took 01h 01m 00.000s"),
        ("fake", 0.0, 3661.0, "fake took 01h 01m 01.000s"),
    ]
)
def test_timer_decorator_outputs_timing(name: str, start: float, end: float, result: str):
    output_mock = Mock()

    params = {"output_func": output_mock}
    if name is not None:
        params["name"] = name
    @timer(**params)
    def dummy_func(x, y):
        return x + y

    with patch("outlify.decorators.time.perf_counter", side_effect=[start, end]):
        dummy_result = dummy_func(2, 3)

    assert dummy_result == 5
    output_mock.assert_called_once()
    message = output_mock.call_args[0][0]
    assert message == result
