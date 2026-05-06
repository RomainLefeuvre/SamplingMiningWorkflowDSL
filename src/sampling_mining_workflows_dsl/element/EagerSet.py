import random
from functools import cmp_to_key
from collections import OrderedDict
from itertools import chain
from typing import Iterable, Mapping, Self

from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.constraint.Constraint import Constraint



class EagerSet(LazySet):
    def __init__(self):
        self.elements: OrderedDict[str, Element] = OrderedDict()
        self.ids: set[str] = set()
        self.set_id = None
    
    @classmethod
    def from_dataset(cls, metadatas, ds):
        header = list(ds.keys())
        id = metadatas[0]
        col_indices = [header.index(m.name) for m in metadatas]
        eager_set = cls()
        for row in zip(*ds.values(), strict=True):
            repo = Repository(id)
            metadata_values = [m.create_metadata_value(row[c]) for m,c in zip(metadatas, col_indices)]
            repo.add_metadata_values(metadata_values)
            eager_set.add_element(repo)
        return eager_set

    @classmethod
    def from_lazyset(cls, it: LazySet):
        result = cls()
        for x in it:
            result.add_element(x)
        return result
    
    @classmethod
    def from_iter_of_maps(cls, metadatas, maps: Iterable[Mapping]) -> Self:
        id = metadatas[0]
        eager_set = cls()
        for row in maps:
            repo = Repository(id)
            metadata_values = [m.create_metadata_value(row[m.name]) for m in metadatas]
            repo.add_metadata_values(metadata_values)
            eager_set.add_element(repo)
        return eager_set

    def __iter__(self):
        yield from self.elements.values()

    def __hash__(self):
        return hash(tuple(self.elements.items())) + hash("EagerSet")

    def __eq__(self, other):
        if not isinstance(other, EagerSet):
            return False
        return self.elements == other.elements
    
    def get_element_by_index(self, index: int) -> Element:
        if index < 0 or index >= len(self.elements):
            raise IndexError("Index out of range")
        return list(self.elements.values())[index]
    def remove_all_elements(self) -> "EagerSet":
        self.elements.clear()
        self.ids.clear()
        return self
    def add_element(self, element: Element) -> "EagerSet":
        if not element.get_id() in self.ids:
            self.elements[element.get_id()]=element
            self.ids.add(element.get_id())
        else :
            print(f"{element.get_id()} Already present")

        return self

    def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> "EagerSet":
        # Sort the items of the OrderedDict
        sorted_items = sorted(
            self.elements.items(),
            key=cmp_to_key(lambda x, y: comparator.compare(x[1], y[1])),
            reverse=reverse
        )
    
        # Rebuild as OrderedDict
        self.elements = OrderedDict(sorted_items)
        return self

    def get_depth(self) -> int:
        max_depth = 1
        for element in self.elements.values():
            if isinstance(element, EagerSet):
                max_depth = max(max_depth, 1 + element.get_depth())
        return max_depth
    
    def union(self, other: Iterable) -> "LazySet":
        if isinstance(other, EagerSet):
            for element in other.elements.values():
                self.add_element(element)
            return self
        else:
            return LazySet(chain(iter(self), iter(other)))
    
    def filter(self, constraint: Constraint) -> Self:
        kept_elements = type(self)()
        for element in self.elements.values():
            if constraint.is_satisfied(element):
                kept_elements.add_element(element)
        return kept_elements
        
    def intersection(self, other: "EagerSet") -> "EagerSet":
        if not isinstance(other, EagerSet):
            raise NotImplementedError
        common_elements = type(self)()
        for id, element in self.elements.items():
            if id in other.elements.keys():
                common_elements.add_element(element)
        return common_elements
    
    def difference(self, other: "EagerSet") -> "EagerSet":
        if not isinstance(other, EagerSet):
            raise NotImplementedError
        """Return a new set with elements in this set but not in other"""
        diff_elements = type(self)()
        for id, element in self.elements.items():
            if id not in other.elements.keys():
                diff_elements.add_element(element)
        return diff_elements
    
    def symmetric_difference(self, other: "EagerSet") -> "EagerSet":
        if not isinstance(other, EagerSet):
            raise NotImplementedError
        """Return a new set with elements in either set but not in both"""
        sym_diff = type(self)()
        
        # Add elements from this set that are not in other
        for id, element in self.elements.items():
            if id not in other.elements.keys():
                sym_diff.add_element(element)
        
        # Add elements from other set that are not in this
        for id, element in other.elements.items():
            if id not in self.elements.keys():
                sym_diff.add_element(element)
        
        return sym_diff
    
    def is_subset(self, other: "EagerSet") -> bool:
        """Return True if all elements in this set are also in other"""
        for id in self.elements.keys():
            if id not in other.elements.keys():
                return False
        return True
    
    def is_superset(self, other: "EagerSet") -> bool:
        """Return True if all elements in other set are also in this set"""
        return other.is_subset(self)
    
    def is_disjoint(self, other: "EagerSet") -> bool:
        """Return True if this set and other have no elements in common"""
        for id in self.elements.keys():
            if id in other.elements.keys():
                return False
        return True
    
    def is_empty(self) -> bool:
        """Return True if the set is empty"""
        return len(self.elements) == 0
    
   

    def size(self) -> int:
        return len(self.elements)

    def get_element(self, id: str) -> Element:
        if id not in self.elements:
            raise RuntimeError(f"Element with id {id} not found in the set")
        return self.elements[id]
    
    # def set_id(self, set_id: str) -> "EagerSet":
    #     self.set_id = set_id
    #     return self 

    # def get_id(self):
    #     if self.set_id is not None:
    #         return self.set_id
        
    #     set_id = ""
    #     for id in self.elements.keys():
    #         set_id = set_id + "_" + str(id)
    #     return set_id

    def flatten_set(self) -> "EagerSet":
        flattened = EagerSet()
        for element in self.get_elements():
            if isinstance(element, EagerSet):
                # Recursively flatten nested Sets
                flattened.union(element.flatten_set())
            else:
                # Add non-Set, non-list elements directly
                flattened.add_element(element)
        return flattened


    def get_random_subset(self, subset_size: int, seed: int) -> "EagerSet":
        elements_list = self.get_elements()
        if subset_size > len(elements_list):
            print(
                f"Caution, subset size is larger than the size of the original set, subset size: {subset_size}, current set size: {len(elements_list)}"
            )
            subset_size = len(elements_list)

        random.seed(seed)
        random_indices = random.sample(range(len(elements_list)), subset_size)
        original_array = list(elements_list)

        result = EagerSet()
        for index in random_indices:
            result.add_element(original_array[index])

        return result

    def get_elements(self) -> list[Element]:
        return list(self.elements.values())
    
    def clone(self) -> "EagerSet":
        cloned_set = EagerSet()
        for element in self.get_elements():
            cloned_set.add_element(element)
        return cloned_set
    
    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        truncate_after = 10
        indent = "    " * level

        result = f"{indent}(size={len(self.elements)})["
        elements_list = self.get_elements()
        element_to_print = min(truncate_after, len(self.elements))

        for i in range(element_to_print):
            next_element = elements_list[i]

            if isinstance(next_element, EagerSet):
                # Recursively call to_string for nested Sets
                result += f"\n{next_element.to_string(level + 4)}"
            else:
                result += str(next_element)

            if i != element_to_print - 1:
                result += ","

        if len(self.elements) > truncate_after:
            result += "...]"
        else:
            result += "]"

        return result
