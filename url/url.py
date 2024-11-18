from controller import product, user

urls = [
    ('/', user.index),
    ('/index', user.index),
    ('/signup', user.signup),
    ('/signin', user.signin),
    ('/products', product.products),
    ('/products/new', product.new_product),
    ('/products/<key>', product.get_product_by_id),
    ('/products/<key>/delete', product.delete_product),
]


