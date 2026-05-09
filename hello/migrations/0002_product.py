from django.db import migrations, models


def seed_products(apps, schema_editor):
	Product = apps.get_model("hello", "Product")
	products = [
		{
			"category": "men",
			"brand": "YSL MYSLF",
			"size": "100ML",
			"price": "165.00",
			"badge": "YSL",
			"image": "hello/images/ysl-myslf.png",
			"notes_title": "Top Notes",
			"notes_text": "Fresh Accord\nOrange Blossom Absolute Heart\nWoods Accord",
			"sort_order": 1,
		},
		{
			"category": "men",
			"brand": "ACQUA DI GIO PROFONDO PARFUM",
			"size": "100ML",
			"price": "182.00",
			"badge": "ADG",
			"image": "hello/images/acqua-di-gio-profondo-parfum.png",
			"notes_title": "Scent Type",
			"notes_text": "Fresh Aquatic\nCardamom Essence\nGreen Mandarin, Lavender, Cypress",
			"sort_order": 2,
		},
		{
			"category": "men",
			"brand": "Eros Najim Parfum",
			"size": "200ML",
			"price": "220.00",
			"badge": "EN",
			"image": "hello/images/eros-najim-parfum.png",
			"notes_title": "Top Notes",
			"notes_text": "Yellow Mandarin Orpur™ (Italy)\nClary Sage\nSaffron, Cardamom Orpur™ (India)",
			"sort_order": 3,
		},
		{
			"category": "men",
			"brand": "Le Male Le Parfum Eau De Parfum",
			"size": "200ML",
			"price": "194.00",
			"badge": "JPG",
			"image": "hello/images/le-male-le-parfum.png",
			"notes_title": "Key Notes",
			"notes_text": "Cardamom\nLavender\nIris",
			"sort_order": 4,
		},
		{
			"category": "women",
			"brand": "Burberry Her Elixer",
			"size": "100ML",
			"price": "190.00",
			"badge": "BH",
			"image": "hello/images/burberry-her-elixer.png",
			"notes_title": "Key Notes",
			"notes_text": "Strawberry and Blackberry Accord\nJasmine Accord\nVanilla, Amber, Sandalwood",
			"sort_order": 1,
		},
		{
			"category": "women",
			"brand": "Parfumes De Marly Valaya Exclusif",
			"size": "75ML",
			"price": "410.00",
			"badge": "PM",
			"image": "hello/images/parfumes-de-marly-valaya-exclusif.png",
			"notes_title": "Top / Heart / Base",
			"notes_text": "Top: Almond, Bergamot, Mandarin\nHeart: Orange Blossom, White Flowers\nBase: White Musks, Akigalawood, Sandalwood, Vanilla",
			"sort_order": 2,
		},
		{
			"category": "women",
			"brand": "Valentino Donna Born In Roma",
			"size": "100ML",
			"price": "180.00",
			"badge": "VR",
			"image": "hello/images/valentino-donna-born-in-roma.png",
			"notes_title": "Key Notes",
			"notes_text": "Sambac Jasmine\nCashmeran\nVanilla",
			"sort_order": 3,
		},
		{
			"category": "women",
			"brand": "YUM BOUJEE MARSHMALLOW",
			"size": "100ML",
			"price": "150.00",
			"badge": "YB",
			"image": "hello/images/yum-boujee-marshmallow.png",
			"notes_title": "Key Notes",
			"notes_text": "Strawberry\nPink Marshmallow\nWhipped Vanilla",
			"sort_order": 4,
		},
	]

	for product in products:
		Product.objects.update_or_create(
			brand=product["brand"],
			defaults=product,
		)


def unseed_products(apps, schema_editor):
	Product = apps.get_model("hello", "Product")
	Product.objects.all().delete()


class Migration(migrations.Migration):

	dependencies = [
		("hello", "0001_review"),
	]

	operations = [
		migrations.CreateModel(
			name="Product",
			fields=[
				("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
				("category", models.CharField(choices=[("men", "Men"), ("women", "Women")], db_index=True, max_length=10)),
				("brand", models.CharField(max_length=120)),
				("size", models.CharField(max_length=30)),
				("price", models.DecimalField(decimal_places=2, max_digits=7)),
				("badge", models.CharField(blank=True, max_length=12)),
				("image", models.CharField(blank=True, max_length=255)),
				("notes_title", models.CharField(default="Notes", max_length=80)),
				("notes_text", models.TextField(help_text="Enter one note per line.")),
				("sort_order", models.PositiveIntegerField(default=0)),
				("is_active", models.BooleanField(default=True)),
				("created_at", models.DateTimeField(auto_now_add=True)),
				("updated_at", models.DateTimeField(auto_now=True)),
			],
			options={"ordering": ["category", "sort_order", "brand"]},
		),
		migrations.RunPython(seed_products, unseed_products),
	]