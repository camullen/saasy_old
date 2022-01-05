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
        return (
            self.arr == other.arr
            and self.start == other.start
            and self.end == other.end
            and self.closed == other.closed
        )


class ArrTimeline:
    def __init__(self) -> None:
        pass
