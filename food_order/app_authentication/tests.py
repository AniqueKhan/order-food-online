from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app_authentication.forms import SignUpForm, EditProfileForm
from app_authentication.models import UserAccount
from django.contrib.auth.models import User
from django.urls import reverse

class SignUpFormTestCase(TestCase):
    def test_valid_signup_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'phone_number': '1234567890',
            'address': '123 Test St',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        # Test when passwords don't match
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'differentpassword',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

class EditProfileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_account = UserAccount.objects.create(user=self.user, phone_number='+12125552368', address='123 Test St')
    
    def test_valid_edit_profile_form(self):
        form_data = {
            'address': '456 New St',
            'phone_number': '+12125552368',
            # You can create a SimpleUploadedFile for testing the image field
            'profile_picture': SimpleUploadedFile("profile.jpg", b"file_content", content_type="image/jpeg"),
        }
        form = EditProfileForm(data=form_data, instance=self.user_account)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_edit_profile_form(self):
        # Test with invalid data
        form_data = {
            'address': 'Too long address' * 50,
            'phone_number': 'invalid_phone_number',
        }
        form = EditProfileForm(data=form_data, instance=self.user_account)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)
        self.assertIn('phone_number', form.errors)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('edit_profile')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_account = UserAccount.objects.create(user=self.user)

    def test_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_authentication/signup.html')

    def test_signup_view_post_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword',
        }
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_authentication/profile.html')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_authentication/edit_profile.html')
