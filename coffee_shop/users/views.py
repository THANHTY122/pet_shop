from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return response
