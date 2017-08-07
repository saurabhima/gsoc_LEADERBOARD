import unittest

from context import sub_process, models, leaderboard


class TestEmail(unittest.TestCase):

    def seed_db(self):
        self.db.session.add(models.Donor(title="Mrs", name="Donor2", email="donor2@test.com",
                                         phone="12345", donor_status="Committed", org="Some Org",
                                         contact_person="some other person", contact_date="2017-10-10",
                                         anonymous_select="No", volunteer_name="Volunteer"))
        self.db.session.add(models.EmailTemplate(
            "generic", "Dear", "Body", "Closing", "Signature"))
        self.db.session.commit()

    def setUp(self):
        self.db = leaderboard.db
        self.User = models.User
        self.Donor = models.Donor
        self.EmailTemplate = models.EmailTemplate
        self.db.session.close()
        self.db.drop_all()
        self.db.create_all()
        self.seed_db()

    def test_get_email_template_list(self):
        templates = sub_process.get_email_template_list()
        assert templates[0].template_name == "generic"

    def test_manual_composition(self):
        donor = self.Donor.query.get(1)
        template_package = sub_process.get_email_template_obj(
            "Manual Composition", donor, 'Sender')
        assert template_package.template_name == 'Manual Composition' and \
            template_package.closing == '' and template_package.main_body == '' and \
            template_package.salutation == '' and template_package.signature_block == ''

    def test_template_composition(self):
        donor = self.Donor.query.get(1)
        template_package = sub_process.get_email_template_obj(
            "generic", donor, "Sender")

        assert template_package.template_name == 'generic' and template_package.salutation == 'Dear Mrs Donor2'