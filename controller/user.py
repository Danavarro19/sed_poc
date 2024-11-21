from controller.decorators import requires_authentication, validate_csrf
from server.response import Response
from service import user as user_service


def index(request):

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
    except Exception as e:
        print(e)
    return Response.redirect('/users')


def signup(request):
    if request.method == "POST":
        try:
            user_service.signup_service(**request.form_data)
        except Exception as e:
            print(e)
            return Response.render(
                request,
                template_name='/auth/signup.html',
                context={"error": e}
            )

        return Response.redirect('/signin')
    return Response.render(
        request,
        template_name='/auth/signup.html'
    )


def signin(request):
    if request.method == "POST":
        try:
            token, expires_at = user_service.signin_service(**request.form_data)
        except Exception as e:
            print(e)
            return Response.redirect('/signin')

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


