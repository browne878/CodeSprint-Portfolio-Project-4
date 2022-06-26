from django.test import TestCase

class TestViews(TestCase):
    """
    Test rendering of website views
    """

    def test_login_page(self):
        """
        Checks if the login page is displayed
        """
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_signup_page(self):
        """
        Checks if the signup page is displayed
        """
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
