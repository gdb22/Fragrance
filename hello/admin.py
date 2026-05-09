from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Avg, Count, Q
from django.templatetags.static import static
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path, reverse

from hello.models import Product, Review


admin.site.site_header = "Fragrance admin"
admin.site.site_title = "Fragrance admin"
admin.site.index_title = "Store management"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
		"admin_image_preview",
		"brand",
		"category",
		"size",
		"price",
		"is_active",
		"sort_order",
		"updated_at",
	)
	list_filter = ("category", "is_active", "created_at", "updated_at")
	search_fields = ("brand", "badge", "notes_title", "notes_text")
	list_editable = ("is_active", "sort_order")
	ordering = ("category", "sort_order", "brand")
	readonly_fields = ("admin_large_image_preview",)
	fieldsets = (
		("Product", {"fields": ("category", "brand", "size", "price", "badge", "is_active")}),
		("Display", {"fields": ("image", "image_file", "admin_large_image_preview", "sort_order")}),
		("Scent notes", {"fields": ("notes_title", "notes_text")}),
	)

	@admin.display(description="Preview")
	def admin_image_preview(self, obj):
		image_url = self._product_image_url(obj)
		if not image_url:
			return "—"
		return format_html(
			'<img src="{}" alt="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 10px; border: 1px solid rgba(139, 139, 130, 0.24);" />',
			image_url,
			obj.brand,
		)

	@admin.display(description="Current image")
	def admin_large_image_preview(self, obj):
		if not obj.pk:
			return "Save the product to preview its image."

		image_url = self._product_image_url(obj)
		if not image_url:
			return "No image selected."

		return format_html(
			'<div style="display:grid;gap:10px;max-width:280px;"><img src="{}" alt="{}" style="width: 100%; max-width: 280px; height: auto; object-fit: cover; border-radius: 16px; border: 1px solid rgba(139, 139, 130, 0.24); box-shadow: 0 12px 24px rgba(78, 68, 55, 0.08);" /><a href="{}" target="_blank" rel="noreferrer">Open full image</a></div>',
			image_url,
			obj.brand,
			image_url,
		)

	def _product_image_url(self, obj):
		if obj.image_file:
			return obj.image_file.url
		if obj.image:
			return static(obj.image)
		return None


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("display_product_name", "reviewer_name", "rating", "created_at")
	search_fields = ("fragrance_name", "reviewer_name", "title", "review_text")
	list_filter = ("rating", "created_at", "product")
	date_hierarchy = "created_at"


def admin_report_view(request):
	User = get_user_model()
	products = Product.objects.all()
	reviews = Review.objects.all()
	users = User.objects.all()
	groups = Group.objects.all()

	context = {
		**admin.site.each_context(request),
		"title": "Store report",
		"report_links": {
			"products": reverse("admin:hello_product_changelist"),
			"reviews": reverse("admin:hello_review_changelist"),
			"users": reverse("admin:auth_user_changelist"),
			"groups": reverse("admin:auth_group_changelist"),
		},
		"stats": {
			"product_count": products.count(),
			"active_product_count": products.filter(is_active=True).count(),
			"review_count": reviews.count(),
			"average_rating": reviews.aggregate(avg=Avg("rating"))["avg"],
			"user_count": users.count(),
			"staff_count": users.filter(is_staff=True).count(),
			"superuser_count": users.filter(is_superuser=True).count(),
			"group_count": groups.count(),
			"users_without_groups": users.annotate(group_total=Count("groups")).filter(group_total=0).count(),
		},
		"recent_products": products.order_by("-updated_at")[:5],
		"recent_reviews": reviews.order_by("-created_at")[:5],
		"recent_users": users.order_by("-date_joined")[:5],
		"security_groups": groups.annotate(member_count=Count("user")).order_by("name"),
		"security_snapshot": users.aggregate(
			active_users=Count("id", filter=Q(is_active=True)),
			inactive_users=Count("id", filter=Q(is_active=False)),
			staff_users=Count("id", filter=Q(is_staff=True)),
		),
	}
	return TemplateResponse(request, "admin/report.html", context)


_original_get_urls = admin.site.get_urls


def _get_admin_urls():
	custom_urls = [
		path(
			"report/",
			admin.site.admin_view(admin_report_view),
			name="hello_admin_report",
		),
	]
	return custom_urls + _original_get_urls()


admin.site.get_urls = _get_admin_urls
