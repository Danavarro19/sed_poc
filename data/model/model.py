from data.orm import BaseModel


class Product(BaseModel):
    table_name = 'product'
    primary_key = 'product_id'
    fields = ['name', 'description', 'price', 'stock_quantity']


class User(BaseModel):
    table_name = 'appuser'
    primary_key = 'user_id'
    fields = ['username', 'password', 'email']


if __name__ == '__main__':
    from pprint import pprint

    data = User.objects.select(field_names=['username', 'email'])
    pprint(data)
