from typing import List
from uuid import UUID

from . import DSOperation
from .card_items import LentoWebsiteItem
from .json_data_backend import JSONDataBackend

from PySide6.QtGui import QIcon


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

    def query_bundled_asset(self, asset_id: str) -> QIcon:
        for backend in self.backends:
            if isinstance(backend, JSONDataBackend):
                return backend.icon_manager.load_bundled_icon(asset_id)


internal_store = _DataStore([])


def init_datastore(backends=[]):
    for backend in backends:
        internal_store.add_backend(backend)


def get_website_list(card_id: UUID) -> List[LentoWebsiteItem]:
    return internal_store.query(DSOperation.GET_WEBSITE_LIST, card_id)


def get_asset(asset_id: str) -> QIcon:
    return internal_store.query_bundled_asset(asset_id)
