from enum import Enum


class ProblemType(Enum):
    prosess = 'prosess'
    cancelled = 'cancelled'
    finished = 'finished'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)