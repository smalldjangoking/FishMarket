from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from FishMarket.helpers import user_not_authenticated
from checkout.models import Order, OrderItem
from .forms import SignUpForm
from .helpers import email_sender, user_email_activator
from .models import User, NovaAddresses
from .forms import UserChangeForm


class UserView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

@user_not_authenticated
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)

            if user is not None:
                login(request, user)
                if not user.is_email_confirmed:
                    email_sender(request, user)
                    return redirect('users:email_confirm')

                return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def email_confirmation(request):
    return render(request, 'users/email_sent.html')


def email_confirmed(request, token):
    tk_confirm = user_email_activator(token)

    if tk_confirm:
        return render(request, 'users/email_confirmed.html')
    else:
        return redirect('mainapp:main')

def user_addresses(request):
    user_addresses = NovaAddresses.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if address_id:
            NovaAddresses.objects.get(user=request.user, id=address_id).delete()

    return render(request, 'users/user_addresses.html', context={'user_addresses': user_addresses})


def user_order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))

    paginator = Paginator(orders, 3)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'users/user_history.html', context={'orders': page_obj, 'page_obj': page_obj})
