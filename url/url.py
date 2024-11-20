from controller import product, user

urls = [
    ('/', user.index),
    ('/index', user.index),
    ('/signup', user.signup),
    ('/signin', user.signin),
    ('/signout', user.signout),
    ('/products', product.products),
    ('/products/new', product.new_product),
    ('/products/<key>', product.get_product),
    ('/products/<key>/delete', product.delete_product),
    ('/products/<key>/update', product.update_product),
    ('/users', user.users),
    ('/users/<key>', user.update_user),
]


