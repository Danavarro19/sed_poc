from controller import controller

urls = [
    ('/', controller.index),
    ('/index', controller.index),
    ('/signup', controller.signup),
    ('/signin', controller.signin),
    ('/products', controller.get_products),
    ('/products/<key>', controller.get_product_by_id),
    ('/products/<key>/delete', controller.delete_product),
]


