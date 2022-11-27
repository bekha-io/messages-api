import typing

from db.db import AbstractDatabase


class MemoryDatabase(AbstractDatabase):
    """A simple implementation of memory-based storage for testing purposes"""
    _storage: typing.Dict[typing.Any, dict]

    def __init__(self):
        self._storage = dict()

    def get_by_pk(self, index: str, pk: typing.Any) -> typing.Any:
        if index in self._storage.keys():
            t = self._storage[index]
            if pk in t.keys():
                return t[pk]

    def pop_by_pk(self, index: str, pk: typing.Any) -> bool:
        if index in self._storage.keys():
            t = self._storage[index]
            if pk in t.keys():
                t.pop(pk)
                return True
        return False

    def update_by_pk(self, index: str, pk: typing.Any, model_to_update: typing.Any) -> bool:
        if index in self._storage.keys():
            t = self._storage[index]
            if pk in t.keys():
                t[index] = model_to_update
                return True
        return False

    def get_by_field(self, index: str, field_name: str, value: str) -> typing.Optional:
        raise NotImplementedError()
