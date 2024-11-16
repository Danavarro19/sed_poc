from view.template import render_template
from service import get_products,  get_product, signup_service
from pprint import pprint 


def index(request):
    return render_template('index.html')


def home(request):
    pass


def signup(request):
    if request.method == "POST":
        signup_service(**request.form_data)
        return render_template('index.html')
    return render_template('signup.html')


def signin(request):
    pass


def all_products(request):
    template = '/product/products.html'
    if request.query_string:
        template = '/product/table.html'
        data = get_products(request.query_string)
    else:
        data = get_products()
    return render_template(template, context={'products': data})


def product(request, key):
    data = get_product(key)
    return render_template('/product/detail.html', context={'product': data})
