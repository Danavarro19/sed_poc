from data.model import Product
from data.orm.manager import Filter


def get_products(filter_by=None):
    if filter_by is None:
        return Product.objects.select()
    filters = []
    if filter_by['name']:
        filters.append(Filter(field='name', value=f"%{filter_by['name']}%", criteria="ILIKE"))

    return Product.objects.select(filter_by=filters)


def get_product(key):
    product = Product.objects.select_by_pk(key)
    if not product:
        raise Exception('Product not found')

    return product


def add_product(data):
    product = Product(**data)
    product.save()


def delete_product(key):
    Product.objects.delete(key)
