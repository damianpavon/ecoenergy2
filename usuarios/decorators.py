from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_required(allowed_roles):
    """
    Decorator to check if user has one of the allowed roles.
    allowed_roles: list of role names (e.g., ['Admin', 'Manager'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(role in allowed_roles for role in user_groups):
                return HttpResponseForbidden("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return role_required(['Admin'])(view_func)

def manager_required(view_func):
    return role_required(['Admin', 'Manager'])(view_func)

def editor_required(view_func):
    return role_required(['Admin', 'Manager', 'Editor'])(view_func)

def reader_required(view_func):
    return role_required(['Admin', 'Manager', 'Editor', 'Reader'])(view_func)
