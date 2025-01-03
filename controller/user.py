import traceback

from controller.decorators import requires_authentication, validate_csrf
from exception import ValidationException, AuthenticationException
from server.response import Response
from service import user as user_service


def index(request):
    if request.user and request.session:
        Response.redirect('/products')
    return Response.render(
        request,
        template_name='index.html'
    )


@requires_authentication
def users(request):
    if not request.user.is_super:
        return Response.unauthorized(request)

    data = user_service.get_users()
    return Response.render(
        request,
        template_name='/users/users.html',
        context={'users': data}
    )


@requires_authentication
@validate_csrf
def update_user(request, key):
    if not request.user.is_super:
        return Response.unauthorized(request)

    if request.method != 'POST':
        return Response.redirect('/users')

    try:
        user_service.update_user_role(key, request.form_data)
    except ValidationException:
        print(traceback.format_exc())
    return Response.redirect('/users')


def signup(request):
    if request.user and request.session:
        Response.redirect('/products')
    if request.method == "POST":
        try:
            user_service.signup_service(**request.form_data)
        except ValidationException as e:
            print(traceback.format_exc())
            return Response.render(
                request,
                status='400 Bad Request',
                template_name='/auth/signup.html',
                context={"error": e}
            )
        return Response.redirect('/signin')
    return Response.render(
        request,
        template_name='/auth/signup.html'
    )


def signin(request):
    if request.user and request.session:
        Response.redirect('/products')
    if request.method == "POST":
        try:
            token, expires_at = user_service.signin_service(**request.form_data)
        except AuthenticationException:
            print(traceback.format_exc())
            return Response.render(
                request,
                status='400 Bad Request',
                template_name='/auth/signin.html',
            )

        date_format = "%a, %d %b %Y %H:%M:%S GMT"
        response = Response.redirect('/products')
        response.set_cookie(
            'session_token',
            token,
            expires=expires_at.strftime(date_format),
            path='/',
            HttpOnly=True,
            Secure=True,
            SameSite='Strict',
        )
        return response

    return Response.render(
        request,
        template_name='/auth/signin.html'
    )


@requires_authentication
def signout(request):
    token = request.get_cookie('session_token')
    user_service.signout_service(token)
    response = Response.redirect('/')
    response.set_cookie(
        'session_token',
        '',
        expires=0,
        path='/',
        HttpOnly=True,
        Secure=True,
        SameSite='strict'
    )
    return response


