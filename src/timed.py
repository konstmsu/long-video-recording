from collections import defaultdict
from contextlib import contextmanager
from typing import Dict, Iterable, List
import timeit
from dataclasses import KW_ONLY, dataclass


@dataclass
class Section:
    started_at: float
    finished_at: float

    @property
    def duration(self):
        return self.finished_at - self.started_at


@dataclass
class SectionTotals:
    _: KW_ONLY
    name: str
    duration: float
    count: int

    @classmethod
    def create(cls, name: str, sections: Iterable[Section]) -> "SectionTotals":
        duration = 0

        for section in sections:
            duration += section.finished_at - section.started_at

        return SectionTotals(
            name=name,
            duration=duration,
            count=len(sections),
        )


class TimedCode:
    def __init__(self):
        self.sections: Dict[str, List[Section]] = defaultdict(list)

    def section(self, name: str):
        @contextmanager
        def record_time():
            started_at = timeit.default_timer()
            try:
                yield
            finally:
                finished_at = timeit.default_timer()
                self.sections[name].append(Section(started_at, finished_at))

        return record_time()

    def summary(self):
        totals = [
            SectionTotals.create(name, sections)
            for name, sections in self.sections.items()
        ]
        return "\n".join(
            f"All {t.count} {t.name} took {t.duration:.2f}" for t in totals
        )


class FpsCounter:
    def __init__(self):
        self.started_at = timeit.default_timer()
        self.frame_count = 0

    def increment(self):
        self.frame_count += 1

    def summary(self):
        duration = timeit.default_timer() - self.started_at
        fps = self.frame_count / duration
        return f"FPS={fps:.2f}"
