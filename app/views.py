from django.shortcuts import redirect, render, get_object_or_404

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


# class ReviewFor

def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    review_list = request.session.get('user_reviews') or list()
    is_review_exist = False
    if pk in review_list:
        is_review_exist = True
    reviews = Review.objects.filter(product_id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if not is_review_exist:
            if form.is_valid():
                review_list.append(pk)
                request.session['user_reviews'] = review_list
                text = form.cleaned_data['text']
                new_review = Review(product=product, text=text)
                new_review.save()
                request.session.modified = True
                is_review_exist = True
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist,
    }
    return render(request, template, context)
