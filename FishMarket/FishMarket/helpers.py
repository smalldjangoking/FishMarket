from functools import wraps
from django.shortcuts import redirect
from cart.cart import Cart


def check_user_cart(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cart = Cart(request)
        if cart.__len__() == 0:
            return redirect('mainapp:AllProducts')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper