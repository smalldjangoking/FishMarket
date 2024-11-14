from django.shortcuts import render, get_object_or_404, redirect

from cart.cart import Cart
from mainapp.models import Product
from django.http import JsonResponse


def cart_view(request):
    """Bucket list of all products added to cart."""
    return render(request, 'cart/cart_view.html')

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        weight = request.POST.get('weight')

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity, weight=weight, price=product.price)

        response = JsonResponse({'qty': str(cart.__len__())})
        return response



def cart_del(request):
    ...

def cart_update(request):
    ...