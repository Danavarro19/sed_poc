from controller import controller

urls = [
    ('/', controller.index),
    ('/index', controller.index),
    ('/home', controller.home),
    ('/signup', controller.signup),
    ('/signin', controller.signin),
    ('/products', controller.all_products),
    ('/products/<key>', controller.product),
    ('/products/<key>/delete', controller.delete_product),
]


