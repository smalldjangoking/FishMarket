from functools import wraps
from django.shortcuts import redirect
from cart.cart import Cart


def check_user_cart(view_func):
    """Makes a return to allproducts if the Cart is empty"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cart = Cart(request)
        if cart.__len__() == 0:
            return redirect('mainapp:AllProducts')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def user_not_authenticated(function):
    """decorator to check if user is not logged in"""
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        else:
            return function(request, *args, **kwargs)
    return wrapper