from controller import controller

urls = [
    ('/', controller.index),
    ('/index', controller.index),
    ('/home', controller.home),
    ('/signup', controller.signup),
    ('/signin', controller.signin),
    ('/product', controller.all_products),
    ('/product/<key_id>', controller.product)
]


