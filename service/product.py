from data.model import Product


def get_products(field_names=None, filter_by=None):
    return Product.objects.select(
        # field_names=["name", "description", "price", "stock_quantity"],
        filter_by=filter_by
    )


