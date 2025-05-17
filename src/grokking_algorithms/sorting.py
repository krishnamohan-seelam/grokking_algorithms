from typing import Sequence ,TypeVar,Generic 


T = TypeVar('T')

class RecursiveQuickSort(Generic[T]):

    def __init__(self, data: Sequence[T]) -> None:
        self.data = data

    def sort(self) -> Sequence[T]:
        if len(self.data) <= 1:
            return self.data
        pivot = self.data[len(self.data) // 2]
        left = [x for x in self.data if x < pivot]
        middle = [x for x in self.data if x == pivot]
        right = [x for x in self.data if x > pivot]
        return RecursiveQuickSort(left).sort() + middle + RecursiveQuickSort(right).sort()