import unittest
from unittest.mock import patch, MagicMock

class MockUser:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    def to_dict(self):
        return {'username': self.username, 'email': self.email}

class TestUserService(unittest.TestCase):
    def setUp(self):
        from app import app
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('service.user_service.find_user_by_email')
    @patch('service.user_service.db')
    @patch('service.user_service.User', new=MockUser)
    def test_add_user_success(self, mock_db, mock_find):
        mock_find.return_value = None
        mock_session = MagicMock()
        mock_db.session = mock_session
        from service.user_service import add_user
        user, error = add_user('testuser', 'test@example.com')
        self.assertIsNotNone(user)
        self.assertIsNone(error)

    @patch('service.user_service.find_user_by_email')
    @patch('service.user_service.User', new=MockUser)
    def test_add_user_duplicate_email(self, mock_find):
        mock_find.return_value = MockUser(username='testuser', email='test@example.com')
        from service.user_service import add_user
        user, error = add_user('testuser', 'test@example.com')
        self.assertIsNone(user)
        self.assertEqual(error, 'Email already exists.')

    @patch('service.user_service.User')
    def test_get_all_users(self, mock_user):
        mock_instance = MockUser(username='testuser', email='test@example.com')
        mock_query = MagicMock()
        mock_query.filter_by.return_value.all.return_value = [mock_instance]
        mock_user.query = mock_query
        from service.user_service import get_all_users
        users = get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'testuser')

    @patch('service.user_service.User')
    def test_find_user_by_email(self, mock_user):
        mock_instance = MockUser(username='testuser', email='test@example.com')
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_instance
        mock_user.query = mock_query
        from service.user_service import find_user_by_email
        user = find_user_by_email('test@example.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
