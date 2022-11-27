import typing
from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def get_by_pk(self, index: str, pk: typing.Any) -> typing.Any:
        """An unimplemented method for getting an object by its primary key"""

    @abstractmethod
    def get_by_field(self, index: str, field_name: str, value: str) -> typing.Optional:
        """An unimplemented method for getting an object by its primary key"""

    @abstractmethod
    def pop_by_pk(self, index: str, pk: typing.Any) -> bool:
        """An unimplemented method for deleting an object by its primary key"""

    @abstractmethod
    def update_by_pk(self, index: str, pk: typing.Any, model_to_update: typing.Any) -> bool:
        """An unimplemented method for updating an object by its primary key"""
