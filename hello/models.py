from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Product(models.Model):
	class Category(models.TextChoices):
		MEN = "men", "Men"
		WOMEN = "women", "Women"

	category = models.CharField(max_length=10, choices=Category.choices, db_index=True)
	brand = models.CharField(max_length=120)
	size = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	badge = models.CharField(max_length=12, blank=True)
	image = models.CharField(max_length=255, blank=True)
	image_file = models.ImageField(upload_to="products/", blank=True)
	notes_title = models.CharField(max_length=80, default="Notes")
	notes_text = models.TextField(help_text="Enter one note per line.")
	sort_order = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["category", "sort_order", "brand"]

	def __str__(self):
		return self.brand

	@property
	def notes(self):
		return [line.strip() for line in self.notes_text.splitlines() if line.strip()]


class Review(models.Model):
	reviewer_name = models.CharField(max_length=80)
	product = models.ForeignKey(
		Product,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="reviews",
	)
	fragrance_name = models.CharField(max_length=120, blank=True)
	title = models.CharField(max_length=120)
	rating = models.PositiveSmallIntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)]
	)
	review_text = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.display_product_name} review by {self.reviewer_name}"

	@property
	def display_product_name(self):
		if self.product:
			return self.product.brand
		return self.fragrance_name
