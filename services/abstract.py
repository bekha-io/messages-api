import typing
from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def get_by_pk(self, pk: typing.Any) -> typing.Optional[typing.Any]:
        """An abstract method for getting an object from database by its primary key"""

    @abstractmethod
    def delete_by_pk(self, pk: typing.Any) -> typing.Any:
        """An unimplemented method for deleting an object from database by its primary key"""
