from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import SignUpForm
from .models import User
from .forms import UserChangeForm


class UserView(UpdateView):
    model = User
    template_name = 'usersapp/profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('usersapp:profile')

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
            return redirect('usersapp:profile')
    else:
        form = SignUpForm()
    return render(request, 'usersapp/signup.html', {'form': form})
