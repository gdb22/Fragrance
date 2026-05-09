from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from hello.models import Product, Review


class ReviewPageTests(TestCase):
	def test_review_page_renders(self):
		response = self.client.get(reverse("review"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Share your fragrance review")

	def test_product_page_uses_database_products(self):
		response = self.client.get(reverse("product"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Product.objects.count(), 8)
		self.assertContains(response, "YSL MYSLF")

	def test_post_creates_review(self):
		product = Product.objects.get(brand="YSL MYSLF")

		response = self.client.post(
			reverse("review"),
			{
				"reviewer_name": "Ava",
				"product": product.id,
				"title": "Clean everyday scent",
				"rating": 5,
				"review_text": "Fresh opening and smooth dry down. Easy to wear daily.",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Review.objects.count(), 1)
		self.assertEqual(Review.objects.first().product, product)
		self.assertContains(response, "Thanks for sharing your fragrance review.")
		self.assertContains(response, 'data-review-new-card="true"')


class AdminReportTests(TestCase):
	def setUp(self):
		self.superuser = get_user_model().objects.create_superuser(
			username="admin",
			email="admin@example.com",
			password="pass12345",
		)

	def test_admin_report_page_renders_for_staff(self):
		self.client.force_login(self.superuser)

		response = self.client.get(reverse("admin:hello_admin_report"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Store report")
		self.assertContains(response, "Security & access")
