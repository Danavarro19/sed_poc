from data.model import Product


def get_all_products():
    return Product.objects.select(
        field_names=["name", "description", "price", "stock_quantity"],
        # filter_by=("stock_quantity", 50)
    )
