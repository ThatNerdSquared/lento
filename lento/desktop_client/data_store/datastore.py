from uuid import UUID

from data_store import DSOperation


class _DataStore:
    operations = {}

    def __init__(self, backends: list):
        self.backends = backends

    def add_backend(self, backend):
        self.backends.append(backend)

    def query(self, op: DSOperation):
        ds_response = {}
        for backend in self.backends:
            (backend_type, res) = backend.query(op)
            ds_response[backend_type] = res
        return ds_response


internal_store = _DataStore([])


def init_datastore(backends=[]):
    for backend in backends:
        internal_store.add_backend(backend)


def retrieve_website_list(card_id: UUID):
    internal_store.query(DSOperation.RETRIEVE_WEBSITE_LIST)
