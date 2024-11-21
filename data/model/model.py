from data.orm import BaseModel
from datetime import datetime
import re


class Product(BaseModel):
    table_name = 'product'
    primary_key = 'product_id'
    fields = ['name', 'description', 'price', 'stock_quantity', 'sku', 'weight', 'is_available']

    def clean(self):
        if not self.is_valid_name():
            raise Exception('Nombre no valido.')

        if not self.is_valid_price():
            raise Exception('Precio no valido.')

        if not self.is_valid_stock_quantity():
            raise Exception('Cantidad disponible no valida.')

        if not self.is_valid_sku():
            raise Exception('SKU no valido.')
        sku = getattr(self, 'sku')
        setattr(self, 'sku', sku.upper())

        if not self.is_valid_weight():
            raise Exception('Peso no valido.')

    def is_valid_name(self):
        name = getattr(self, 'name', '')
        return bool(name) and len(name) <= 50

    def is_valid_price(self):
        price = getattr(self, 'price', '')
        try:
            price = float(price)
            return price > 0
        except ValueError:
            return False

    def is_valid_stock_quantity(self):
        stock_quantity = getattr(self, 'stock_quantity', '')
        try:
            stock_quantity = int(stock_quantity)
            return stock_quantity >= 0
        except ValueError:
            return False

    def is_valid_sku(self):
        sku = getattr(self, 'sku', '')
        pattern = r"^[A-Za-z]{2}[0-9]+$"
        return bool(re.match(pattern, sku)) and len(sku) <= 50

    def is_valid_weight(self):
        weight = getattr(self, 'weight', None)
        if not weight:
            return True
        try:
            weight = float(weight)
            return bool(weight) and weight >= 0
        except ValueError:
            return False


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

    def clean(self):
        if not self.is_valid_email():
            raise Exception('Correo no valido.')

        if not self.is_valid_username():
            raise Exception('Nombre de usuario no valido')

    def is_valid_email(self):
        email = getattr(self, 'email')
        domain = 'sedproject.com'

        pattern = rf"^[a-zA-Z0-9._%+-]+@{re.escape(domain)}$"
        return bool(re.match(pattern, email))

    def is_valid_username(self):
        username = getattr(self, 'username')

        pattern = rf"^[a-zA-Z0-9._]+"
        return bool(re.match(pattern, username))


class Session(BaseModel):
    table_name = 'session'
    primary_key = 'session_id'
    fields = ['user_id', 'session_token', 'created_at', 'expires_at', 'csrf_token']

    @property
    def revoked(self):
        return getattr(self, 'expires_at') < datetime.now()
