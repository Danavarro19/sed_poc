class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls, connection):
        connection.autocommit = True  # https://www.psycopg.org/docs/connection.html#connection.commit
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *, field_names=None, filter_by=None, chunk_size=2000):
        # Build SELECT query
        if field_names:
            fields_format = ", ".join(field_names)
        else:
            fields_format = "*"

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

    def update(self, new_data: dict):
        # Build UPDATE query and params
        field_names = new_data.keys()
        placeholder_format = ", ".join(
            [f"{field_name} = %s" for field_name in field_names]
        )
        query = (
            f"UPDATE {self.model_class.table_name} SET {placeholder_format}"
        )
        params = list(new_data.values())

        # Execute query
        self._execute_query(query, params)

    def delete(self, key):
        # Build DELETE query
        query = f"DELETE FROM {self.model_class.table_name} "

        # Execute query
        self._execute_query(query)