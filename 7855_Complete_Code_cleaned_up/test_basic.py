import unittest
import sys
import os

from main import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_main_page_redirect(self):
        """Test if the main page redirects to login when not authenticated"""
        response = self.app.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # 302 is redirect
        self.assertTrue('/login' in response.location)
    
    def test_login_page_loads(self):
        """Test if the login page loads correctly"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Login' in response.data)
    
    def test_signup_page_loads(self):
        """Test if the signup page loads correctly"""
        response = self.app.get('/signUp')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Sign Up' in response.data)

if __name__ == "__main__":
    unittest.main()