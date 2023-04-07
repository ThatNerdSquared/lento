from abc import ABC, abstractmethod
from uuid import UUID

from data_store import DSOperation


class AbstractDataBackend(ABC):
    def __init__(self):
        self.OPS_TABLE = {DSOperation.RETRIEVE_WEBSITE_LIST: self.retrieve_website_list}

    def query(self, op: DSOperation):
        res = self.OPS_TABLE[op]()
        return (self.get_backend_type(), res)

    @abstractmethod
    def get_backend_type(self):
        """Will be implemented by children."""

    @abstractmethod
    def retrieve_website_list(self, card_id: UUID):
        """Will be implemented by children."""
