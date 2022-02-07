from unittest import TestCase, main
from server import app
from model import connect_to_db, db, create_test_data

class TripsterTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_redirect_to_login(self):
        result = self.client.get("/", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Welcome back</h2>', result.data)
        self.assertNotIn(b'<h2>Trips</h2>', result.data)


class TripsterTestsLoggedIn(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        create_test_data()

        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = 1


    def tearDown(self):

        db.session.remove()
        db.drop_all()


    def test_trips(self):
        result = self.client.get("/", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Trips</h2>', result.data)
        self.assertNotIn(b'<h2>Welcome back</h2>', result.data)


    def test_categories(self):
        result = self.client.get("/categories")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Categories</h2>', result.data)
        self.assertNotIn(b'<h2>Welcome back</h2>', result.data)


    def test_templates(self):
        result = self.client.get("/templates")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Templates</h2>', result.data)
        self.assertNotIn(b'<h2>Welcome back</h2>', result.data)


if __name__ == "__main__":
    main()
