from django.shortcuts import render

from checkout.forms import CheckoutUserForm


def checkout(request):
    if request.method == 'POST':
        form = CheckoutUserForm(request.POST)

    if request.user.is_authenticated:
        data = {
            'name': request.user.name,
            'last_name': request.user.last_name,
            'phone': request.user.phone_number
        }

        form = CheckoutUserForm(initial=data)
    else:
        form = CheckoutUserForm()

    context = {
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context=context)