import unittest
from sqlalchemy.exc import IntegrityError, DataError
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
        self.db.session.add(models.User(username='vtest', full_name='Volunteer',
                                        email='vtest@test.com', phone='1234',
                                        user_type='Volunteer',
                                        register_date='2017-10-11',
                                        account_status='Active',
                                        passwd=hashed_password))
        self.db.session.add(models.User(username='vtest2', full_name='Volunteer 2',
                                        email='vtest2@test.com', phone='1234',
                                        user_type='Volunteer',
                                        register_date='2017-10-11',
                                        account_status='Pending',
                                        passwd=hashed_password))
        self.db.session.commit()

    def clear_db(self):
        self.db.session.rollback()
        self.User.query.delete()

    @classmethod
    def setUpClass(cls):
        leaderboard.db.session.close()
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

    def test_pending_user_list(self):
        users = sub_process.get_pending_user_list()
        user_usernames = {user.username for user in users}
        non_pending_users = {'test2', 'vtest'}
        pending_users = {'test', 'vtest2'}

        assert user_usernames == pending_users and user_usernames & non_pending_users == set()

    def test_approve_existing_user(self):
        sub_process.approve_user('test')
        user = self.User.query.filter_by(username='test').first()
        assert user.account_status == 'Active'

    def test_approve_nonexistent_user(self):
        with self.assertRaises(exception.EntityNotFoundError):
            sub_process.approve_user('test3')

    def test_reject_nonexistent_user(self):
        """Should result in a no-op when properly implemented"""
        sub_process.reject_user('test3')
        assert True

    def test_reject_existing_user(self):
        sub_process.reject_user('test')
        user = self.User.query.filter_by(username='test').first()
        assert user is None

    def test_active_volunteers(self):
        volunteers = sub_process.get_volunteer_list()
        volunteers_usernames = {volunteer.username for volunteer in volunteers}
        active_volunteers = {'vtest'}
        non_valid_users = {'vtest2', 'test', 'test2'}

        assert volunteers_usernames == active_volunteers and volunteers_usernames & non_valid_users == set()

    def test_new_user_creation(self):
        sub_process.add_user_details_db(
            'Test1', 'test@testtt.com', '1123', 'testttt', 'randompass', 'Administrator')
        new_user = self.User.query.filter_by(username='testttt').first()
        assert new_user is not None and new_user.user_type == 'Administrator' and new_user.account_status == 'Pending'

    def test_conflicting_user_details(self):
        with self.assertRaises(IntegrityError):
            sub_process.add_user_details_db(
                'Test', 'test@test.com', '1234', 'test', 'randompass', 'Administrator')

    def test_invalid_data(self):
        with self.assertRaises(DataError):
            sub_process.add_user_details_db(
                'Test1', 'test@testtt.com', '1123', 'testttt', 'randompass', 'Randomprivilege')