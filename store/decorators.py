from django.http import HttpResponse
from django.shortcuts import redirect

# checks if user is logged in before running the original func
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            # execute the original func
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

# check if user is admin
def admin_required(view_func):
    def wrapper_func(request, *args, **kwkargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwkargs)
        else:
            return HttpResponse('You are not authorised to be view this page.')
    return wrapper_func