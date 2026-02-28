import unittest
from unittest.mock import patch, MagicMock

class TestUserRoute(unittest.TestCase):
    def setUp(self):
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('route.user_route.add_user')
    def test_create_user_success(self, mock_add_user):
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {'username': 'testuser', 'email': 'test@example.com'}
        mock_add_user.return_value = (mock_user, None)
        response = self.client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')

    @patch('route.user_route.add_user')
    def test_create_user_missing_username(self, mock_add_user):
        response = self.client.post('/users', json={'email': 'test@example.com'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'message': 'Field username is required'})

    @patch('route.user_route.add_user')
    def test_create_user_missing_email(self, mock_add_user):
        response = self.client.post('/users', json={'username': 'testuser'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'message': 'Field email is required'})

    @patch('route.user_route.add_user')
    def test_create_user_duplicate_email(self, mock_add_user):
        mock_add_user.return_value = (None, 'Email already exists.')
        response = self.client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json(), {'message': 'Email already exists.'})

    @patch('route.user_route.get_all_users')
    def test_list_users(self, mock_get_all_users):
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {'username': 'testuser', 'email': 'test@example.com'}
        mock_get_all_users.return_value = [mock_user]
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'testuser')
        self.assertEqual(data[0]['email'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()
