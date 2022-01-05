import pandas as pd


class ArrInterval:
    def __init__(self, start: pd.Timestamp, end: pd.Timestamp, arr: float, closed: str = "both") -> None:
        self._interval = pd.Interval(start, end, closed=closed)
        self._arr = float(arr)

    @classmethod
    def empty_interval(cls):
        return cls(pd.Timestamp.min, pd.Timestamp.max, 0.0, closed="neither")

    @property
    def start(self) -> pd.Timestamp:
        return self._interval.left

    @property
    def end(self) -> pd.Timestamp:
        return self._interval.right

    @property
    def arr(self) -> float:
        return self._arr

    @property
    def closed(self) -> str:
        return self._interval.closed

    def overlaps(self, other) -> bool:
        return self._interval.overlaps(other._interval)

    def __eq__(self, other) -> bool:
        return (self.start, self.end, self.arr, self.closed) == (other.start, other.end, other.arr, other.closed)

    def __lt__(self, other) -> bool:
        return (self.start, self.end, self.arr, self.closed) < (other.start, other.end, other.arr, other.closed)

    def __gt__(self, other) -> bool:
        return (self.start, self.end, self.arr, self.closed) > (other.start, other.end, other.arr, other.closed)

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __le__(self, other) -> bool:
        return (self.start, self.end, self.arr, self.closed) <= (other.start, other.end, other.arr, other.closed)

    def __ge__(self, other) -> bool:
        return (self.start, self.end, self.arr, self.closed) >= (other.start, other.end, other.arr, other.closed)

    def __repr__(self) -> str:
        return f'ArrInterval({repr(self.start)}, {repr(self.end)}, {self.arr}, closed="{self.closed}")'


class ArrTimeline:
    def __init__(self) -> None:
        pass
