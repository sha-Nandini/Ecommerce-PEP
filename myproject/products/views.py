from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Review, Category

def home(request):

    from django.db.models import Avg, Count, Q
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(parent=None)

    # Filters
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    search = request.GET.get('search')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    if category_id:
        main_category = Category.objects.get(id=category_id)
        subcategories = Category.objects.filter(parent=main_category)
        products = products.filter(Q(category=main_category) | Q(category__parent=main_category))
    else:
        subcategories = []

    if subcategory_id:
        products = products.filter(category_id=subcategory_id)

    if search:
        products = products.filter(name__icontains=search)

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    if rating:
        products = products.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=rating)

    # Sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'rating':
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')

    # Annotate products with avg rating and review count
    products = products.annotate(avg_rating=Avg('review__rating'), review_count=Count('review'))

    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'home.html', context)



def product_detail(request, id):

    from .models import ProductImage, Review
    from django.db.models import Avg, Count
    product = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=product)
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'similar_products': similar_products,
    }
    return render(request, 'product_detail.html', context)

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', id=pk)