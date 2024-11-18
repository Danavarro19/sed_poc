from data.orm import BaseModel


class Product(BaseModel):
    table_name = 'product'
    primary_key = 'product_id'
    fields = ['name', 'description', 'price', 'stock_quantity']


class User(BaseModel):
    table_name = 'appuser'
    primary_key = 'user_id'
    fields = ['username', 'password', 'email']


class Session(BaseModel):
    table_name = 'session'
    primary_key = 'session_id'
    fields = ['user_id', 'session_token', 'created_at', 'expires_at']
