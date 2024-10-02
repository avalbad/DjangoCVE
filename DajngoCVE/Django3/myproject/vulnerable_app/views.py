# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView
# from .forms import PasswordResetForm
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from django.core import mail
# from django.contrib.auth.models import User

# 2.2
# # -----------------------
# class PasswordResetViewTest(TestCase):
#     def _create_user(self, username, email, password=None):
#         return User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#         )

#     def test_send_reset_mail(self):
#         # Create a user with a valid email
#         email = 'taro@example.com'
#         self._create_user(username='taro', email=email, password='testpassword')

#         # Send a POST request to the password reset view with the user's email
#         data = {'email': email}
#         response = self.client.post(reverse('accounts:password_reset'), data)

#         # Assert that the response is a redirect to the password reset done page
#         self.assertRedirects(response, reverse('accounts:password_reset_done'))

#         # Assert that an email was sent to the user's email
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertListEqual(mail.outbox[0].to, [email])

#         # Assert that the email contains a link to reset the password
#         self.assertIn('http://example.com/accounts/reset/', mail.outbox[0].body)


# 1.1
## -----------------------

# def password_reset(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             # کد مربوط به بازنشانی رمز عبور
#             pass
#     else:
#         form = PasswordResetForm()
#     return render(request, 'password_reset0.html', {'form': form})



# def vulnerable_view(request):
#     user_input = request.GET.get('user_input')
#     return HttpResponse(f"Hello, {user_input}!")

# class BaseView(TemplateView):
#     template_name = 'base.html'


# class ProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'profile.html'

# class PasswordResetView(auth_views.PasswordResetView):
#     form_class = PasswordResetForm
#     subject_template_name = 'mails/password_reset/subject.txt'
#     email_template_name = 'mails/password_reset/body.txt'
#     template_name = 'password_reset_complete.html'
#     success_url = reverse_lazy('accounts:password_reset_done')


# class PasswordResetDoneView(auth_views.PasswordResetDoneView):
#     template_name = 'password_reset_done.html'


# class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     success_url = reverse_lazy('accounts:password_reset_complete')
#     template_name = 'password_reset_confirm.html'


# class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
#     template_name = 'password_reset_complete.html'



# 3.3
# -----------------------------------------------------

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'vulnerable_app/mails/password_reset_form.html'
    email_template_name = 'vulnerable_app/mails/password_reset_email.html'
    subject_template_name = 'vulnerable_app/mails/password_reset/subject.txt'
    success_url = reverse_lazy('vulnerable_app:password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'vulnerable_app/mails/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'vulnerable_app/mails/password_reset_confirm.html'
    success_url = reverse_lazy('vulnerable_app:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'vulnerable_app/mails/password_reset_complete.html'
