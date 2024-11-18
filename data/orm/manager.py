class Filter:
    def __init__(self, *, field, value, criteria="=", logical_operator=None):
        self.field = field
        self.value = value
        self.criteria = criteria
        self.logical_operator = logical_operator


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

        params = []
        if filter_by:
            filter_clauses = []

            for current_filter in filter_by:
                filter_clauses.append(f"{current_filter.field} {current_filter.criteria} %s")
                params.append(current_filter.value)
                if current_filter.logical_operator is None:
                    break
                else:
                    filter_clauses.append(current_filter.logical_operator)

            query += " WHERE " + " ".join(filter_clauses)

        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)

            model_objects = []
            while True:
                result = cursor.fetchmany(size=chunk_size)
                if not result:
                    break

                for row_values in result:
                    row_data = dict(zip(field_names or self.model_class.fields, row_values))
                    model_objects.append(self.model_class(**row_data))

            return model_objects
        finally:
            cursor.close()

    def select_by_field(self, field, key):
        query = f"SELECT * FROM {self.model_class.table_name} WHERE {field} = %s"
        cursor = self._get_cursor()
        try:
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            if result:
                row_data = dict(zip([self.model_class.primary_key] + self.model_class.fields, result))
                return self.model_class(**row_data)
            else:
                return None
        finally:
            cursor.close()

    def select_by_pk(self, key):
        return self.select_by_field(self.model_class.primary_key, key)

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
        self._execute_query(query, (key,))
