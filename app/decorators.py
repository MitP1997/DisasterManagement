from django.core.exceptions import PermissionDenied

def user_is_operator(function):
    def wrap(request, *args, **kwargs):
        user_role = request.user.user_role
        if user_role == 'o':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        user_role = request.user.user_role
        if user_role == 'a':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_supplier(function):
    def wrap(request, *args, **kwargs):
        user_role = request.user.user_role
        if user_role == 's':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
