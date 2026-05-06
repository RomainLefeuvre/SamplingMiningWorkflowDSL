import pytest

from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

def test_from_dataset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    dataset = {"val": list(range(10)), "irrelevant": list("ABCDEFGHIJ"), "id": list(map(str, range(10))), "double": list(range(0,20,2))}

    eager_set = EagerSet.from_dataset(metadatas, dataset)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size() == 10)

    element0 = eager_set.get_element_by_index(0)
    e = Repository(metadatas[0])
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)

def test_from_iter_of_maps():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    it = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x], "id": str(x), "double": 2*x} for x in range(10)]

    eager_set = EagerSet.from_iter_of_maps(metadatas, it)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size() == 10)

    element0 = eager_set.get_element_by_index(0)
    e = Repository(metadatas[0])
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)
    
def test_from_lazyset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    it1 = ({"val": x, "id": str(x), "double": x+x} for x in range(10))
    lazy_set = LazySet.from_iter_of_maps(metadatas, it1)

    eager_set = EagerSet.from_lazyset(lazy_set)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size() == 10)

    element0 = eager_set.get_element_by_index(0)
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    e = Repository(metadatas[0])
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)
    
def test_allcreationsareequal():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    dataset = {"val": list(range(10)), "irrelevant": list("ABCDEFGHIJ"), "id": list(map(str, range(10))), "double": list(range(0,20,2))}
    maps = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x], "id": str(x), "double": 2*x} for x in range(10)]
    lazy_set = LazySet.from_iter_of_maps(metadatas, maps)

    set_from_ds = EagerSet.from_dataset(metadatas, dataset)
    set_from_maps = EagerSet.from_iter_of_maps(metadatas, maps)
    set_from_lazy = EagerSet.from_lazyset(lazy_set)

    assert(set_from_ds == set_from_maps)
    assert(set_from_maps == set_from_lazy)

def test_hash():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(100, 103)))
    assert(hash(es1) != hash(es2))
    s = {es1, es2}
    
def test_eq():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(100, 103)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    
    assert(es1 == es1)
    assert(es1 != es2)
    assert(es1 == es3)
    
    assert(es2 != es1)
    assert(es2 == es2)
    assert(es2 != es3)

    assert(es3 == es1)
    assert(es3 != es2)
    assert(es3 == es3)
    
def test_get_element_by_index():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    
    with pytest.raises(IndexError):
        es1.get_element_by_index(-11)
    with pytest.raises(IndexError):
        es1.get_element_by_index(11)
    
    e = es1.get_element_by_index(2)
    i, v, d = metadatas
    r = Repository(i)
    r.add_metadata_values([i.create_metadata_value("2"), v.create_metadata_value(2), d.create_metadata_value(2+2)])
    assert(e == r)
    
def test_remove_all_elements():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, [{"id": str(x), "val": x, "double": 2*x} for x in range(10)])
    es2 = EagerSet.from_iter_of_maps(metadatas, [])
    es1.remove_all_elements()
    assert(es1.size() == 0)
    assert(es1 == es2)

def test_add_element():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]

    es1 = EagerSet.from_iter_of_maps(metadatas, [])
    i, v, d = metadatas
    for x in range(10):
        r = Repository(i)
        r.add_metadata_values([i.create_metadata_value(str(x)), v.create_metadata_value(x), d.create_metadata_value(x+x)])
        es1.add_element(r)
    
    es2 = EagerSet.from_iter_of_maps(metadatas, [{"id": str(x), "val": x, "double": 2*x} for x in range(10)])
    assert(es1 == es2)

# #def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> "EagerSet":
# def test_sort_by_metadata():
#     pass

# def test_get_depth():
#     pass

def test_union():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(100, 103)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in list(range(10))+list(range(100,103))))
    
    esu = es1.union(es2)

    assert(esu == es3)

def test_intersection():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(10)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 12, 5, 13)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 5)))
    
    esi = es1.intersection(es2)
    assert(esi == es3)

def test_difference():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(5)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 12, 5, 0, 13)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3)))
    es4 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (12, 5, 13)))
    
    es1d2 = es1.difference(es2)
    assert(es1d2 == es3)
    es2d1 = es2.difference(es1)
    assert(es2d1 == es4)

def test_symmetric_difference():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in range(5)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 12, 5, 0, 13)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3, 12, 5, 13)))
    
    esd = es1.symmetric_difference(es2)
    assert(esd == es3)

def test_is_subset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 12, 1, 5, 0, 2, 13)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3, 12, 5, 13)))

    assert(es0.is_subset(es0) is True)
    assert(es0.is_subset(es1) is True)
    assert(es0.is_subset(es2) is True)
    assert(es0.is_subset(es3) is True)

    assert(es1.is_subset(es0) is False)
    assert(es1.is_subset(es1) is True)
    assert(es1.is_subset(es2) is True)
    assert(es1.is_subset(es3) is False)

    assert(es2.is_subset(es0) is False)
    assert(es2.is_subset(es1) is False)
    assert(es2.is_subset(es2) is True)
    assert(es2.is_subset(es3) is False)

    assert(es3.is_subset(es0) is False)
    assert(es3.is_subset(es1) is False)
    assert(es3.is_subset(es2) is False)
    assert(es3.is_subset(es3) is True)

def test_is_superset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (4, 12, 1, 5, 0, 2, 13)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3, 12, 5, 13)))

    assert(es0.is_superset(es0) is True)
    assert(es0.is_superset(es1) is False)
    assert(es0.is_superset(es2) is False)
    assert(es0.is_superset(es3) is False)

    assert(es1.is_superset(es0) is True)
    assert(es1.is_superset(es1) is True)
    assert(es1.is_superset(es2) is False)
    assert(es1.is_superset(es3) is False)

    assert(es2.is_superset(es0) is True)
    assert(es2.is_superset(es1) is True)
    assert(es2.is_superset(es2) is True)
    assert(es2.is_superset(es3) is False)

    assert(es3.is_superset(es0) is True)
    assert(es3.is_superset(es1) is False)
    assert(es3.is_superset(es2) is False)
    assert(es3.is_superset(es3) is True)

def test_is_disjoint():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (3,)))
    assert(es0.is_disjoint(es0) is True)
    assert(es0.is_disjoint(es1) is True)
    assert(es0.is_disjoint(es2) is True)
    assert(es0.is_disjoint(es3) is True)

    assert(es1.is_disjoint(es0) is True)
    assert(es1.is_disjoint(es1) is False)
    assert(es1.is_disjoint(es2) is False)
    assert(es1.is_disjoint(es3) is True)

    assert(es2.is_disjoint(es0) is True)
    assert(es2.is_disjoint(es1) is False)
    assert(es2.is_disjoint(es2) is False)
    assert(es2.is_disjoint(es3) is False)

    assert(es3.is_disjoint(es0) is True)
    assert(es3.is_disjoint(es1) is True)
    assert(es3.is_disjoint(es2) is False)
    assert(es3.is_disjoint(es3) is False)

def test_is_empty():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2, 3)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (3,)))
    assert(es0.is_empty() is True)
    assert(es1.is_empty() is False)
    assert(es2.is_empty() is False)
    assert(es3.is_empty() is False)

def test_size():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    es2 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (1, 2,)))
    es3 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (3,)))
    assert(es0.size() == 0)
    assert(es1.size() == 3)
    assert(es2.size() == 2)
    assert(es3.size() == 1)

def test_get_element():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    es0 = EagerSet.from_iter_of_maps(metadatas, [])
    es1 = EagerSet.from_iter_of_maps(metadatas, ({"id": str(x), "val": x, "double": 2*x} for x in (0, 1, 2)))
    
    with pytest.raises(RuntimeError):
        x = es0.get_element("2")
    with pytest.raises(RuntimeError):
        x = es1.get_element("3")
    
    x = es1.get_element("2")
    i, v, d = metadatas
    y = Repository(i)
    y.add_metadata_values([i.create_metadata_value("2"), v.create_metadata_value(2), d.create_metadata_value(2+2)])
    assert(x == y)

# def test_flatten_set():
#     pass


# def test_get_random_subset():
#     pass
