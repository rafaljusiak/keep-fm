from django.contrib.auth.views import LoginView


class LoginUserView(LoginView):
    template_name = "auth/login.html"
