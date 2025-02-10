from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from checkout.models import Order
from .forms import SignUpForm
from .models import User, NovaAddresses
from .forms import UserChangeForm


class UserView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def user_addresses(request):
    user_addresses = NovaAddresses.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if address_id:
            NovaAddresses.objects.get(user=request.user, id=address_id).delete()

    return render(request, 'users/user_addresses.html', context={'user_addresses': user_addresses})


def user_order_history(request):
    history = Order.objects.filter(user=request.user)

    return render(request, 'users/user_history.html', context={'history': history})