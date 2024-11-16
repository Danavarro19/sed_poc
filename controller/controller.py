from server.response import Response
from view.template import render_template
from service import product as product_service, user as user_service


def index(request):
    return render_template('index.html')


def signup(request):
    if request.method == "POST":
        user_service.signup_service(**request.form_data)
        return Response.redirect('/signin')
    return Response(render_template('/auth/signup.html'))


def signin(request):
    if request.method == "POST":
        print(request.form_data)
    return Response(render_template('/auth/signin.html'))


def products(request):
    if request.method == "GET":
        template = '/product/products.html'
        if request.query_string:
            template = '/product/table.html'
            data = product_service.get_products(request.query_string)
        else:
            data = product_service.get_products()
        return Response(render_template(template, context={'products': data}))
    if request.method == "POST":
        product_service.add_product(request.form_data)
        return Response.redirect('/products')


def new_product(request):
    return Response(render_template('/product/new.html'))


def get_product_by_id(request, key):
    data = product_service.get_product(key)
    return Response(render_template('/product/detail.html', context={'product': data}))


def delete_product(request, key):
    product_service.delete_product(key)
    return Response.redirect('/products')
