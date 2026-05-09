from django import forms

from hello.models import Product, Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(is_active=True)
        self.fields["product"].required = True

    def save(self, commit=True):
        review = super().save(commit=False)
        if review.product:
            review.fragrance_name = review.product.brand
        if commit:
            review.save()
        return review

    class Meta:
        model = Review
        fields = [
            "reviewer_name",
            "product",
            "title",
            "rating",
            "review_text",
        ]
        labels = {
            "reviewer_name": "Your name",
            "product": "Product",
            "title": "Review title",
            "rating": "Rating",
            "review_text": "Your review",
        }
        widgets = {
            "reviewer_name": forms.TextInput(
                attrs={"placeholder": "e.g. Maya"}
            ),
            "product": forms.Select(
                attrs={"class": "review-select"}
            ),
            "title": forms.TextInput(
                attrs={"placeholder": "Short summary of your experience"}
            ),
            "rating": forms.RadioSelect(
                choices=[(value, str(value)) for value in range(5, 0, -1)]
            ),
            "review_text": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Share your thoughts about the fragrance",
                }
            ),
        }