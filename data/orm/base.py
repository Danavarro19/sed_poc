from .manager import BaseManager
from .conn import connection_pool


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        if cls.manager_class.connection is None:
            cls.manager_class.set_connection(connection_pool.getconn())
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""
    primary_key = "id"
    fields = []

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join(
            [f"{field}={value}" for field, value in self.__dict__.items()]
        )
        return f"<{self.__class__.__name__}: ({attrs_format})>"

    def save(self):
        self.__class__.objects.insert(self)
