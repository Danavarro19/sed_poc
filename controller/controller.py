from server.response import Response
from view.template import render_template
from service import product as product_service, user as user_service


def index(request):
    return render_template('index.html')


def home(request):
    pass


def signup(request):
    if request.method == "POST":
        user_service.signup_service(**request.form_data)
        return Response.redirect('/')
    return Response(render_template('/auth/signup.html'))


def signin(request):
    pass


def all_products(request):
    template = '/product/products.html'
    if request.query_string:
        template = '/product/table.html'
        data = product_service.get_products(request.query_string)
    else:
        data = product_service.get_products()
    return Response(render_template(template, context={'products': data}))


def product(request, key):
    data = product_service.get_product(key)
    return Response(render_template('/product/detail.html', context={'product': data}))


def delete_product(request, key):
    product_service.delete_product(key)
    return Response.redirect('/products')
