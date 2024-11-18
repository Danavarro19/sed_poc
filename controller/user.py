from controller.decorators import requires_authentication
from server.response import Response
from service import user as user_service


def index(request):

    return Response.render(
        request,
        template_name='index.html'
    )


def signup(request):
    if request.method == "POST":
        user_service.signup_service(**request.form_data)
        return Response.redirect('/signin')
    return Response.render(
        request,
        template_name='/auth/signup.html'
    )


def signin(request):
    if request.method == "POST":
        try:
            token = user_service.signin_service(**request.form_data)
        except Exception as e:
            print(e)
            return Response.redirect('/signin')
        return Response.redirect('/products', cookies={'session_token': token})

    return Response.render(
        request,
        template_name='/auth/signin.html'
    )


@requires_authentication
def signout(request):
    token = request.get_cookie('session_token')
    user_service.signout_service(token)
    return Response.redirect('/')

