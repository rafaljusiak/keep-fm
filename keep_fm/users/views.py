from django.contrib.auth.views import LoginView


class LoginUserView(LoginView):
    """Base login view"""

    template_name = "auth/login.html"
