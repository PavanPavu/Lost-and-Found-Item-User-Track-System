from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('user_dashboard')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            if user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def user_dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return render(request, 'accounts/user_dashboard.html')

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')
