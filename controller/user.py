from server.response import Response
from view.template import render_template
from service import user as user_service


def index(request):
    return render_template('index.html')


def signup(request):
    if request.method == "POST":
        user_service.signup_service(**request.form_data)
        return Response.redirect('/signin')
    return Response(render_template('/auth/signup.html'))


def signin(request):
    if request.method == "POST":
        try:
            user_service.signin_service(**request.form_data)
        except :
            return Response.redirect('/signin')

        return Response.redirect('/products')

    return Response(render_template('/auth/signin.html'))

