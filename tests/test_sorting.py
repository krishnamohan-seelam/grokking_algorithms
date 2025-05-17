import pytest
from grokking_algorithms.sorting import RecursiveQuickSort

def test_recursive_quick_sort_empty_list():
    sorter = RecursiveQuickSort([])
    assert sorter.sort() == []

def test_recursive_quick_sort_single_element():
    sorter = RecursiveQuickSort([1])
    assert sorter.sort() == [1]

def test_recursive_quick_sort_sorted_list():
    sorter = RecursiveQuickSort([1, 2, 3, 4, 5])
    assert sorter.sort() == [1, 2, 3, 4, 5]

def test_recursive_quick_sort_reverse_sorted_list():
    sorter = RecursiveQuickSort([5, 4, 3, 2, 1])
    assert sorter.sort() == [1, 2, 3, 4, 5]

def test_recursive_quick_sort_unsorted_list():
    sorter = RecursiveQuickSort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    assert sorter.sort() == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

def test_recursive_quick_sort_with_duplicates():
    sorter = RecursiveQuickSort([4, 2, 4, 3, 1, 2, 4])
    assert sorter.sort() == [1, 2, 2, 3, 4, 4, 4]