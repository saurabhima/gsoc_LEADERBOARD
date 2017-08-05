import unittest
from sqlalchemy.exc import IntegrityError, DataError
from werkzeug.security import generate_password_hash

from context import sub_process, leaderboard, models, exception


class TestDonor(unittest.TestCase):
    def seed_db(self):
        hashed_password = generate_password_hash('test')
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
        self.db.session.add(models.Donor(title="Mr", name="Donor", email="donor@test.com",
                                         phone="1234", donor_status="New", org="Some Org",
                                         contact_person="some person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name=None))
        self.db.session.add(models.Donor(title="Mrs", name="Donor2", email="donor2@test.com",
                                         phone="12345", donor_status="Committed", org="Some Org",
                                         contact_person="some other person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name="Volunteer"))
        self.db.session.add(models.Donor(title="Miss", name="Donor3", email="donor3@test.com",
                                         phone="12346", donor_status="Allotted", org="Some Org",
                                         contact_person="some other person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name="Volunteer"))
        self.db.session.commit()

    def setUp(self):
        self.db = leaderboard.db
        self.User = models.User
        self.Donor = models.Donor

        self.db.session.close()
        self.db.drop_all()
        self.db.create_all()
        self.seed_db()

    def test_get_donor_list(self):
        donors = sub_process.get_donor_list()
        assert donors[1].email == "donor2@test.com" and donors[1].id == 2

    def test_donor_detailsbyid(self):
        donor = sub_process.donor_details_byid(1)
        assert donor.email == "donor@test.com"

    def test_update_nonexistent_donor(self):
        """Updating a nonexistent donor should throw an EntityNotFoundError"""

        with self.assertRaises(exception.EntityNotFoundError):
            sub_process.update_donor_contact(
                99, "1234", "test@test2.com", "Random org")

    def test_update_existing_donor(self):
        sub_process.update_donor_contact(
            1, "1345", "test@test123.com", "someorg")
        donor = self.Donor.query.get(1)
        assert donor.phone == "1345" and donor.email == "test@test123.com" and donor.org == "someorg"

    def test_get_new_donor_list(self):
        new_donors = sub_process.get_new_donor_list()
        assert new_donors[0].id == 1

    def test_allotted_donors(self):
        alloted_donors = sub_process.alotted_donors_byid('Volunteer')
        assert alloted_donors[0].name == 'Donor2'

    def test_register_new_donor(self):
        sub_process.register_new_donor(
            "Sir", "Donorus", "Orgus", "donorus@test.com", "1234", "Contactus", "2017-10-10", "Yes")
        new_donor = self.Donor.query.filter_by(
            email="donorus@test.com").first()
        assert new_donor.name == "Donorus" and new_donor.donor_status == "New" and new_donor.volunteer_name is None

    def test_register_new_donor_with_existing_details(self):
        """Should raise an integrity error for colliding details"""
        with self.assertRaises(IntegrityError):
            sub_process.register_new_donor(
                "Sir", "Donorus", "Orgus", "donor@test.com", "1234", "contactus", "2017-10-10", "No")


class TestDonorLog(unittest.TestCase):
    def seed_db(self):
        self.db.session.add(models.Donor(title="Mr", name="Donor", email="donor@test.com",
                                         phone="1234", donor_status="New", org="Some Org",
                                         contact_person="some person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name=None))
        self.db.session.add(models.Donor(title="Mrs", name="Donor2", email="donor2@test.com",
                                         phone="12345", donor_status="Committed", org="Some Org",
                                         contact_person="some other person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name="Volunteer"))
        self.db.session.add(models.Donor(title="Miss", name="Donor3", email="donor3@test.com",
                                         phone="12346", donor_status="Allotted", org="Some Org",
                                         contact_person="some other person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name="Volunteer"))
        self.db.session.add(models.DonorPhoneLog(contact_date="2017-09-09", contact_time="11:30",
                                                 contact_person="Contact", donor_id=1, remarks="Remark",
                                                 details_shared="Shared details"))
        self.db.session.add(models.DonorPhoneLog(contact_date="2017-09-10", contact_time="11:30",
                                                 contact_person="Contact2", donor_id=2, remarks="Remarks2",
                                                 details_shared="Shared details2"))

        self.db.session.add(models.DonorEmailLog(
            "2017-10-10", "11:30", "Dude", 1, "Some body", "some email", "code"))
        self.db.session.add(models.DonorEmailLog(
            "2017-10-12", "11:31", "Dude2", 2, "Some body3", "some email4", "code5"))
        self.db.session.commit()

    def setUp(self):
        self.db = leaderboard.db
        self.Donor = models.Donor
        self.DonorPhoneLog = models.DonorPhoneLog
        self.DonorEmailLog = models.DonorEmailLog
        self.db.session.close()
        self.db.drop_all()
        self.db.create_all()
        self.seed_db()

    def test_phone_log_lookup(self):
        logs = sub_process.donor_phone_logs_byid(1)

        assert len(logs) == 1 and logs[0].remarks == "Remark"

    def test_nonexistent_donor_phone_lookup(self):
        logs = sub_process.donor_phone_logs_byid(99)

        assert len(logs) == 0

    def test_add_phone_log(self):
        sub_process.add_donor_phone_log(
            1, "Person", "2017-10-10", "11:30", "Something", "Silly")

        logs = self.DonorPhoneLog.query.filter_by(donor_id=1).all()

        assert len(logs) == 2 and logs[1].remarks == "Silly"

    def test_add_nonexistent_donor_log(self):

        with self.assertRaises(exception.EntityNotFoundError):
            sub_process.add_donor_phone_log(
                1, "Person", "2017-10-10", "11:30", "Something", "Silly")

    def test_email_log_lookup(self):
        logs = sub_process.donor_email_logs_byid(2)

        assert len(logs) == 1 and logs[0].contact_person == "Dude2"

    def test_nonexistent_donor_email_lookup(self):
        logs = sub_process.donor_email_logs_byid(99)

        assert len(logs) == 0
