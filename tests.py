from app import app
import unittest


class MaestroTestCase(unittest.TestCase):


	def test_create_album(self):

		''' test correct response, it's 302 in this case because of redirect
		and user not authenticated '''

		tester = app.test_client(self)
		response = tester.get('/create_album/', content_type='text/html')
		self.assertEqual(response.status_code, 302)


	def test_login_view_response(self):

		''' if user is redirected to 'login' page, then "Please login" text
		is rendered by view function. This test checks whether correct data (
		so form) is passed to template or not '''

		tester = app.test_client(self)
		response = tester.get('/login/', content_type='text/html')
		self.assertTrue(b'Please login' in response.data)

	def test_register_view_response(self):

		''' similar test to this above, just checking with the register view.
		Both views operate on the same template, theat's why test is crucial '''

		tester = app.test_client(self)
		response = tester.get('/register/', content_type='text/html')
		self.assertTrue(b'Please register' in response.data)


if __name__ == '__main__':
	unittest.main()
