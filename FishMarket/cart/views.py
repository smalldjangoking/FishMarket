from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from mainapp.models import Product
from django.http import JsonResponse
from django.core import exceptions


def cart_view(request):
    return render(request, 'cart/bucket_view.html')

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        if int(quantity) < 1:
            return JsonResponse({'status': 'error', 'message': 'Кількість товару не може бути меншою за 1'}, status=400)
        weight = request.POST.get('weight')

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, price=product.price, quantity=quantity, weight=weight)

        response = JsonResponse({'qty': str(cart.__len__())})
        return response



def cart_del(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST':
        product_id = request.POST.get('product_id')
        product_weight = request.POST.get('product_weight')


        cart.delete_product(product_id=product_id, product_weight=product_weight)
        response = JsonResponse({'qty': str(cart.__len__()), 'total_price': cart.get_full_price()})
        return response


def cart_update(request):
    ...