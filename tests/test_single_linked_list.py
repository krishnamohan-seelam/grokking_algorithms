import pytest
from grokking_algorithms.linked_lists.single_linked_list import Node, SingleLinkedList

def test_node_init_and_properties():
    n = Node(5)
    assert n.data == 5
    assert n.next is None
    n.data = 10
    assert n.data == 10
    n2 = Node(20)
    n.next = n2
    assert n.next == n2
    assert n.has_next()
    assert str(n) == "10"
    assert repr(n) == "10"

def test_node_append_and_type_error():
    n1 = Node(1)
    n2 = Node(2)
    n1.append(n2)
    assert n1.next == n2


def test_single_linked_list_empty():
    sll = SingleLinkedList()
    assert sll.is_empty()
    assert len(list(sll)) == 0
    assert sll.size() == 0
    assert str(sll) == ""
    assert repr(sll) == "SingleLinkedList()"

def test_insert_to_front_and_back():
    sll = SingleLinkedList()
    sll.insert_to_front(1)
    assert not sll.is_empty()
    assert list(sll) == [1]
    sll.insert_to_front(2)
    assert list(sll) == [2, 1]
    sll.insert_to_back(3)
    assert list(sll) == [2, 1, 3]
    sll.insert_to_back(4)
    assert list(sll) == [2, 1, 3, 4]

def test_traverse_and_iter():
    sll = SingleLinkedList()
    for i in range(3):
        sll.insert_to_back(i)
    result = list(sll.traverse(lambda x: x * 2))
    assert result == [0, 2, 4]
    assert list(sll) == [0, 1, 2]

def test_len_and_size():
    sll = SingleLinkedList()
    for i in range(5):
        sll.insert_to_back(i)
    assert len(sll) == 5
    assert sll.size() == 5

def test_search_and_contains():
    sll = SingleLinkedList()
    for i in [10, 20, 30]:
        sll.insert_to_back(i)
    assert sll.search(lambda x: x == 20) == 20
    assert sll.search(lambda x: x == 99) is None
    assert 10 in sll
    assert 99 not in sll

def test_get_valid_and_invalid():
    sll = SingleLinkedList()
    for i in [5, 6, 7]:
        sll.insert_to_back(i)
    assert sll.get(0) == 5
    assert sll.get(2) == 7
    with pytest.raises(IndexError):
        sll.get(-1)
    with pytest.raises(IndexError):
        sll.get(3)

def test_delete_existing_and_not_found():
    sll = SingleLinkedList()
    for i in [1, 2, 3, 2]:
        sll.insert_to_back(i)
    sll.delete(2)
    assert list(sll) == [1, 3, 2]
    sll.delete(2)
    assert list(sll) == [1, 3]
    with pytest.raises(ValueError):
        sll.delete(99)

def test_delete_from_front():
    sll = SingleLinkedList()
    sll.insert_to_back(100)
    sll.insert_to_back(200)
    data = sll.delete_from_front()
    assert data == 100
    assert list(sll) == [200]
    sll.delete_from_front()
    assert sll.is_empty()
    with pytest.raises(ValueError):
        sll.delete_from_front()

def test_str_and_repr():
    sll = SingleLinkedList()
    for i in [1, 2, 3]:
        sll.insert_to_back(i)
    assert str(sll) == "1 -> 2 -> 3"
    assert repr(sll) == "SingleLinkedList(1 ->2 ->3)"