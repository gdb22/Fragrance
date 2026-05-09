from django.contrib import messages
from django.shortcuts import redirect, render

from hello.forms import ReviewForm
from hello.models import Product, Review

# Static page views.
def home(request):
    return render(request, "hello/Home.html")

def about(request):
    return render(request, "hello/About.html")

def contact(request):
    return render(request, "hello/Contact.html")


def review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            saved_review = form.save()
            request.session["highlight_review_id"] = saved_review.id
            messages.success(request, "Thanks for sharing your fragrance review.")
            return redirect("review")
    else:
        form = ReviewForm()

    highlighted_review_id = request.session.pop("highlight_review_id", None)

    return render(
        request,
        "hello/Review.html",
        {
            "form": form,
            "reviews": Review.objects.all()[:6],
            "highlighted_review_id": highlighted_review_id,
        },
    )

# Product catalog view with both collections passed to the template.
def product(request):
    men_products = Product.objects.filter(
        category=Product.Category.MEN,
        is_active=True,
    )
    women_products = Product.objects.filter(
        category=Product.Category.WOMEN,
        is_active=True,
    )

    return render(
        request,
        "hello/Product.html",
        {
            "men_products": men_products,
            "women_products": women_products,
        },
    )
