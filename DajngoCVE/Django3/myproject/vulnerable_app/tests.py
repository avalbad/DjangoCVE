# from django.conf import settings
# from django.core import mail
# from django.contrib.auth import get_user_model
# from django.test import TestCase



# 1.1
# -----------------------------------------
# class LoginViewTest(TestCase):
#     def _create_user(self, username, email, password=None):
#         return User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#         )

#     def test_show_page(self):
#         r = self.client.get(reverse('accounts:login'))
#         self.assertEqual(r.status_code, 200)

#     def test_redirect_to_index_after_login(self):
#         username = 'taro'
#         email = 'taro@example.com'
#         password = 'testpassword'
#         self._create_user(
#             username=username,
#             email=email,
#             password=password,
#         )
#         data = {
#             'username': username,
#             'password': password,
#         }
#         r = self.client.post(reverse('accounts:login'), data)
#         self.assertRedirects(
#             r,
#             settings.LOGIN_REDIRECT_URL,
#             fetch_redirect_response=False,
#         )


# class ProfileViewTest(TestCase):
#     def _create_user(self, username, email, password=None):
#         return User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#         )

#     def test_show_page(self):
#         user = self._create_user(
#             username='taro',
#             email='taro@example.com',
#             password='testpassword',
#         )
#         self.client.force_login(user)
#         r = self.client.get(reverse('accounts:profile'))
#         self.assertEqual(r.status_code, 200)


# class PasswordResetViewTest(TestCase):
#     def _create_user(self, username, email, password=None):
#         return User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#         )

#     def test_show_page(self):
#         r = self.client.get(reverse('accounts:password_reset'))
#         self.assertEqual(r.status_code, 200)

#     def test_send_reset_mail(self):
#         email = 'taro@example.com'
#         self._create_user(
#             username='taro',
#             email=email,
#             password='testpassword',
#         )

#         data = {'email': email}
#         r = self.client.post(reverse('accounts:password_reset'), data)
#         self.assertRedirects(r, reverse('accounts:password_reset_done'))

#         self.assertEqual(len(mail.outbox), 1)
#         self.assertListEqual(mail.outbox[0].to, [email])
# ------------------------------------------



# 2.2
# --------------------------------------
# from urllib.parse import urlparse
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_encode
# class PasswordResetVulnerabilityTest(TestCase):
    # def test_password_reset_vulnerability(self):
    #     # Create two users
    #     user1 = User.objects.create_user('user1', 'user1@example.com', 'password')
    #     user2 = User.objects.create_user('user2', 'user2@example.com', 'password')

    #     # Submit the password reset form for user1
    #     response = self.client.post(reverse('password_reset'), {'email': user1.email})

    #     # Get the password reset token from the email
    #     email = mail.outbox[0]
    #     email_body = email.body
    #     print(email_body)  # or log it
    #     url_start = "http://testserver/reset/"
    #     url_end = "/"
    #     token_start = email_body.find(url_start) + len(url_start)
    #     token_end = email_body.find(url_end, token_start)
    #     token = email_body[token_start:token_end]

    #     if not token:
    #        self.fail("Email body format is not as expected")
        

    #     # Tamper with the token to reset user2's password
    #     # tampered_token = token.replace(user1.pk, user2.pk)
    #     tampered_token = token.replace(str(user1.pk), str(user2.pk))
    #     uidb64 = urlsafe_base64_encode(force_text(user2.pk))
    #     # response = self.client.get(reverse('password_reset_confirm'), {'token': tampered_token})
    #     response = self.client.get(reverse('password_reset_confirm', args=[uidb64, tampered_token]))

    #     # Check that the password reset form is displayed for user2
    #     self.assertContains(response, 'Enter new password')

    #     # Submit the new password for user2
    #     new_password = 'new_password'
    #     response = self.client.post(reverse('password_reset_confirm'), {'token': tampered_token, 'new_password1': new_password, 'new_password2': new_password})

    #     # Check that the password was successfully reset for user2
    #     self.assertTrue(self.client.login(username=user2.username, password=new_password))
# ---------------------------------------





# 3.3
# ----------------------------------------
from django.contrib.auth.models import User
import re
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

def test_password_reset_vulnerability(self):
    user2 = User.objects.create_user(user2, 'user2@example.com', 'password123')
 
        # Send password reset email
    response = self.client.post(reverse('password_reset'), {'email': 'user2@example.com'})
    self.assertEqual(response.status_code, 302)

    # Extract token from email
    email_content = response.wsgi_request._email_messages[0].body
    token_pattern = r'http://testserver/reset/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$'
    match = re.search(token_pattern, email_content)
    uidb64 = match.group(1)
    original_token = match.group(2)

    # Tamper with the token
    hacked_token = original_token + 'tampered'

    # Try to reset password with tampered token
    response = self.client.get(reverse('password_reset_confirm', args=[uidb64, hacked_token]))
    self.assertEqual(response.status_code, 200)

    # Check that the password reset form is displayed
    self.assertContains(response, 'New password')

    # Try to reset password with tampered token
    response = self.client.post(reverse('password_reset_confirm', args=[uidb64, hacked_token]), {
        'new_password1': 'newpassword123',
        'new_password2': 'newpassword123'
    })
    self.assertEqual(response.status_code, 302)

    # Check that the password has been reset successfully
    self.assertTrue(self.client.login(username='user2', password='newpassword123'))