import unittest
from context import sub_process, leaderboard, models, exception
from werkzeug.security import generate_password_hash, check_password_hash


class TestUser(unittest.TestCase):
    def seed_db(self):
        hashed_password = generate_password_hash('test')
        self.db.session.add(models.User(username='test', full_name='Test',
                                        email='test@test.com', phone='1234',
                                        user_type='Administrator',
                                        register_date='2017-10-11',
                                        account_status='Pending',
                                        passwd=hashed_password))

        self.db.session.add(models.User(username='test2', full_name='Test 2',
                                        email='test2@test.com', phone='1234',
                                        user_type='Administrator',
                                        register_date='2017-10-11',
                                        account_status='Active',
                                        passwd=hashed_password))
        self.db.session.commit()

    def clear_db(self):
        self.User.query.delete()

    @classmethod
    def setUpClass(cls):
        leaderboard.db.drop_all()
        leaderboard.db.create_all()

    def setUp(self):
        self.db = leaderboard.db
        self.User = models.User
        self.clear_db()
        self.seed_db()

    def test_nonexistent_user_auth(self):
        login_status, user_account_type, _ = sub_process.authenticate(
            'test3', 'fail')
        assert login_status is False and user_account_type is None

    def test_inactive_user_auth(self):
        login_status, user_account_type, _ = sub_process.authenticate(
            'test', 'test')
        assert login_status is False and user_account_type is None

    def test_active_user_auth(self):
        login_status, user_account_type, _ = sub_process.authenticate(
            'test2', 'test')
        assert login_status is True and user_account_type == 'Administrator'

    def test_active_user_invalid_auth(self):
        login_status, user_account_type, _ = sub_process.authenticate(
            'test2', 'wrongpass')
        assert login_status is False and user_account_type is None

    def test_approve_user(self):
        sub_process.approve_user('test')
        user = self.User.query.filter_by(username='test').first()
        assert user.account_status == 'Active'

    def test_approve_nonexistent_user(self):
        self.assertRaises(exception.EntityNotFoundError,
                          sub_process.approve_user('test3'))

    def test_reject_nonexistent_user(self):
        """Should result in a no-op when properly implemented"""
        sub_process.reject_user('test3')
        assert True

    def test_reject_user(self):
        sub_process.reject_user('test')
        user = self.User.query.filter_by(username='test').first()
        assert user is None
