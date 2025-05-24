import functools
import time
from typing import Callable, ParamSpec, TypeVar  # noqa: UP035

__all__ = ["timer"]


P = ParamSpec("P")
R = TypeVar("R")


def timer(
        name: str | None = None,
        output_func: Callable[[str], None] = print,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Time the function.

    :param name: custom name instead of "Function {function name}",
    :param output_func: function for outputting measurements
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = _format_duration(time.perf_counter() - start)
            label = name if name else f"Function {func.__name__!r}"
            output_func(f"{label} took {duration}")
            return result
        return wrapper
    return decorator


def _format_duration(seconds: float) -> str:
    total_ms = int(seconds * 1000)
    ms, total_s = total_ms % 1000, total_ms // 1000
    s, total_m = total_s % 60, total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}h {m:02d}m {s:02d}.{ms:03d}s"


if __name__ == "__main__":  # pragma: no cover
    import time

    @timer()
    def dummy_func(a: int, b: int) -> int:
        time.sleep(0.001)
        return a + b

    @timer(name="Dummy")
    def dammy_func_with_custom_name(a: int, b: int) -> int:
        time.sleep(0.001)
        return a + b

    dummy_func(1, 2)
    dammy_func_with_custom_name(1, 2)
