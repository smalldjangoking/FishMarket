from django.shortcuts import render, redirect

from FishMarket.helpers import check_user_cart
from checkout.forms import CheckoutUserForm
from checkout.order import create_order

@check_user_cart
def checkout(request):
    """
    View for creating an order to db
    Also, update user information while creating an order.
    """

    if request.method == 'GET':
        if request.user.is_authenticated:
            data = {
                'name': request.user.name,
                'last_name': request.user.last_name,
                'phone': request.user.phone_number,
            }
            form = CheckoutUserForm(initial=data)
        else:
            form = CheckoutUserForm()

    if request.method == 'POST':
        form = CheckoutUserForm(request.POST)

        if request.user.is_authenticated:
            user = request.user
            if not all([user.name, user.last_name, user.phone_number]):
                user.name = request.POST.get('name')
                user.last_name = request.POST.get('last_name')
                user.phone_number = request.POST.get('phone')
                user.save()


        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['request'] = request
            order_creating = create_order(cleaned_data)

            if order_creating:
                return redirect('checkout:checkout_success')



    return render(request, 'checkout/checkout.html', context={'form': form})

def checkout_success(request):
    """Success page for checkout"""
    return render(request, 'checkout/successful.html')
