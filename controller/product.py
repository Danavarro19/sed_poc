from controller.decorators import requires_authentication
from server.response import Response
from view.template import render_template
from service import product as product_service


@requires_authentication
def products(request):
    if request.method == "GET":
        template = '/product/products.html'
        if request.query_string:
            template = '/product/table.html'
            data = product_service.get_products(request.query_string)
        else:
            data = product_service.get_products()
        return Response.render(request, template_name=template, context={'products': data})
    if request.method == "POST":
        product_service.add_product(request.form_data)
        return Response.redirect('/products')


@requires_authentication
def new_product(request):
    return Response.render(
        request,
        template_name='/product/new.html'
    )


@requires_authentication
def get_product(request, key):
    data = product_service.get_product(key)
    return Response.render(
        request,
        template_name='/product/detail.html',
        context={'product': data}
    )


@requires_authentication
def delete_product(request, key):
    product_service.delete_product(key)
    return Response.redirect('/products')
