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
