from data.orm import BaseModel
from datetime import datetime


class Product(BaseModel):
    table_name = 'product'
    primary_key = 'product_id'
    fields = ['name', 'description', 'price', 'stock_quantity']


class User(BaseModel):
    table_name = 'appuser'
    primary_key = 'user_id'
    fields = ['username', 'password', 'email', 'role']

    def is_role(self, role):
        return getattr(self, 'role') == role

    @property
    def is_super(self):
        return self.is_role('super')

    @property
    def is_admin(self):
        return self.is_role('admin') or self.is_role('super')


class Session(BaseModel):
    table_name = 'session'
    primary_key = 'session_id'
    fields = ['user_id', 'session_token', 'created_at', 'expires_at']

    @property
    def revoked(self):
        return getattr(self, 'expires_at') < datetime.now()
