class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls, connection):
        connection.autocommit = True
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        try:
            cursor.execute(query, params)
        finally:
            cursor.close()

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *, field_names=None, filter_by=None, chunk_size=2000):
        # Build SELECT query
        if field_names is None:
            field_names = [self.model_class.primary_key] + self.model_class.fields

        fields_format = ", ".join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"

        if filter_by:
            field, value = filter_by
            query = f"{query} WHERE {field}={value}"

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)

        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(result) < chunk_size

        return model_objects

    def select_by_pk(self, key):
        query = f"SELECT * FROM {self.model_class.table_name} WHERE {self.model_class.primary_key} = %s"
        cursor = self._get_cursor()
        try:
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            if result:
                row_data = dict(zip(self.model_class.fields, result))
                return self.model_class(**row_data)
            else:
                return None
        finally:
            cursor.close()

    def insert(self, instance):
        fields_format = ", ".join(instance.fields)
        values_format = ", ".join(["%s"] * len(instance.fields))
        query = f"INSERT INTO {instance.table_name} ({fields_format}) VALUES ({values_format})"
        params = [getattr(instance, field) for field in instance.fields]
        self._execute_query(query, params)

    def update(self, key, new_data: dict):
        field_names = new_data.keys()
        placeholder_format = ", ".join(
            [f"{field_name} = %s" for field_name in field_names]
        )
        query = (
            f"UPDATE {self.model_class.table_name} SET {placeholder_format}WHERE {self.model_class.primary_key} = %s"
        )
        params = list(new_data.values()) + [key]

        # Execute query
        self._execute_query(query, params)

    def delete(self, key):
        # Build DELETE query
        query = f"DELETE FROM {self.model_class.table_name} WHERE {self.model_class.primary_key} = %s"

        # Execute query
        self._execute_query(query, key)
