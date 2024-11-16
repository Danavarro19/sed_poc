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
    return Product.objects.select_by_pk(key)
