from view.template import render_template
from service import get_all_products
from pprint import pprint 


def index(request):
    return render_template('index.html')


def home(request):
    pass


def signup(request):
    if request.method == "POST":
        data = request.form_data
        pprint(data)
        return render_template('index.html')
    return render_template('signup.html')


def signin(request):
    pass


def all_products(request):
    data = get_all_products()
    return render_template('products.html', context={'products': data})


def product(request, key):
    pass
