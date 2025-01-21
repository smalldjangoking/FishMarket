from django.shortcuts import render

from checkout.forms import CheckoutUserForm


def checkout(request):
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


        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['user_id'] = request.user.id if request.user.is_authenticated else None



    return render(request, 'checkout/checkout.html', context={'form': form})
