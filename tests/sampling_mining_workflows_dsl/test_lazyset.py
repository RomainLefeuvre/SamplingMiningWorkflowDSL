import math

from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata


def test_lazyset():
    it1 = ((str(x), x, 2*x) for x in range(10))
    ls1 = LazySet(it1)
    it2 = ((str(x), x, math.factorial(x % 200)) for x in range(1000000))
    ls2 = LazySet(it2)
    assert(len(list(ls1)) == 10)

def test_union():
    it1 = ((str(x), x, 2*x) for x in range(10))
    ls1 = LazySet(it1)
    it2 = ((str(x), x, 2*x) for x in range(100,103))
    ls2 = LazySet(it2)
    
    lsu = ls1.union(ls2)
    
    assert(isinstance(lsu, LazySet) and len(list(lsu)) == 13)

def test_intersection():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    elements = [{"val": x, "id": str(x), "double": x+x} for x in range(10)]
    ls1 = LazySet.from_iter_of_maps(metadatas, elements)
    it2 = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x%10], "id": str(x), "double": 2*x} for x in (101, 102, 103, 4, 5, 15, 16)]
    eg2 = EagerSet.from_iter_of_maps(metadatas, it2)
    
    lsi = ls1.intersection(eg2)
    
    assert(isinstance(lsi, LazySet) and len(list(lsi)) == 2)

def test_difference():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    it1 = ({"val": x, "id": str(x), "double": x+x} for x in range(10))
    ls1 = LazySet.from_iter_of_maps(metadatas, it1)
    it2 = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x%10], "id": str(x), "double": 2*x} for x in (101, 102, 103, 4, 5, 15, 16)]
    eg2 = EagerSet.from_iter_of_maps(metadatas, it2)

    lsd = ls1.difference(eg2)
    
    assert(isinstance(lsd, LazySet) and len(list(lsd)) == 8)

def test_get_id():
    id, val, double, fact = (Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double"), Metadata.of_integer("fact"))
    meta1 = [id, val, double]
    it1 = ({"val": x, "id": str(x), "double": x+x} for x in range(10))
    ls1 = LazySet.from_iter_of_maps(meta1, it1)
    meta2 = [id, val, fact]
    it2 = ({"val": x, "id": str(x), "fact": math.factorial(x % 200)} for x in range(10))
    ls2 = LazySet.from_iter_of_maps(meta2, it2)

    i1 = ls1.get_id()
    i2 = ls2.get_id()
    
    assert(isinstance(i1, str) and isinstance(i2, str) and i1 != i2)

def test_flatten_set():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    it1 = ({"val": x, "id": str(x), "double": x+x} for x in range(10))
    ls1 = LazySet.from_iter_of_maps(metadatas, it1)
    it2 = ({"val": x, "id": str(x), "double": x+x} for x in range(100, 103))
    ls2 = LazySet.from_iter_of_maps(metadatas, it2)
    it3 = ({"val": x, "id": str(x), "double": x+x} for x in range(200, 205))
    ls3 = LazySet.from_iter_of_maps(metadatas, it3)
    
    lsa = LazySet(iter((ls1, ls2)))

    lsb = LazySet(iter((lsa, ls3)))

    lsf = lsb.flatten_set()
    assert(isinstance(lsf, LazySet) and len(list(lsf)) == 10+3+5)

def test_get_random_subset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("fact")]
    elements = [{"val": x, "irrelevant": chr(ord('A') + x%26), "id": str(x), "fact": math.factorial(x % 200)} for x in range(1000)]
    ls1 = LazySet.from_iter_of_maps(metadatas, elements)
    ls2 = LazySet.from_iter_of_maps(metadatas, elements)
    
    subset_size, seed = (10, 42)
    rand_lazy_1 = ls1.get_random_subset(subset_size, seed)
    assert(isinstance(rand_lazy_1, LazySet))
    rand_eager_1 = EagerSet.from_lazyset(rand_lazy_1)
    assert(len(rand_eager_1.elements) == subset_size)

    rand_lazy_2 = ls2.get_random_subset(subset_size, seed)
    rand_eager_2 = EagerSet.from_lazyset(rand_lazy_2)
    assert(rand_eager_1 == rand_eager_2)

    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("fact")]
    eg = EagerSet.from_iter_of_maps(metadatas, elements)
    assert rand_eager_1.is_subset(eg)
