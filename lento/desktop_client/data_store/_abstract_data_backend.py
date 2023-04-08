from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from . import DSOperation
from .card_items import LentoWebsiteItem


class AbstractDataBackend(ABC):
    def __init__(self):
        self.OPS_TABLE = {DSOperation.GET_WEBSITE_LIST: self.get_website_list}

    def query(self, op: DSOperation, *args):
        res = self.OPS_TABLE[op](*args)
        return (self.get_backend_type(), res)

    @abstractmethod
    def get_backend_type(self):
        """Will be implemented by children."""

    @abstractmethod
    def get_website_list(self, card_id: UUID) -> List[LentoWebsiteItem]:
        """Will be implemented by children."""
