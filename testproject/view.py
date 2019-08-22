from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from user.views import AdminUserRequiredMixin


class HomeView(AdminUserRequiredMixin, TemplateView):
    template_name = "base.html"

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(self.request)
        if not user:
            return redirect(reverse('login'))
        return redirect(reverse("home"))
