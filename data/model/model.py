from data.orm import BaseModel


class Product(BaseModel):
    table_name = 'product'


class User(BaseModel):
    table_name = 'appuser'


if __name__ == '__main__':
    from pprint import pprint

    data = User.objects.select(field_names=['username', 'email'])
    pprint(data)
