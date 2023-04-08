from typing import List
from uuid import UUID

from . import DSOperation
from .card_items import LentoWebsiteItem


class _DataStore:
    operations = {}

    def __init__(self, backends: list):
        self.backends = backends

    def add_backend(self, backend):
        self.backends.append(backend)

    def query(self, op: DSOperation, *args):
        ds_response = {}
        for backend in self.backends:
            (backend_type, res) = backend.query(op, *args)
            ds_response[backend_type] = res
        return ds_response


internal_store = _DataStore([])


def init_datastore(backends=[]):
    for backend in backends:
        internal_store.add_backend(backend)


def get_website_list(card_id: UUID) -> List[LentoWebsiteItem]:
    internal_store.query(DSOperation.GET_WEBSITE_LIST, card_id)
