from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from mainapp.models import Product, SeaCategory, ProductImage
from django.db.models import Q


class MainPageView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    context_object_name = 'products'
    queryset = Product.objects.order_by('-time_create')[:6]

class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product_item.html'
    context_object_name = 'product'
    slug_field = 'slug'  # поле модели для поиска
    slug_url_kwarg = 'slug'  # название параметра URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пример дополнительного контекста
        context['related_products'] = ProductImage.objects.filter(product_id=self.object.id)
        context['amount_of_photos'] = range(len(context['related_products']) +1)
        print(context['amount_of_photos'])
        return context

class CategoryListView(ListView):
    model = SeaCategory
    template_name = 'mainapp/category.html'
    context_object_name = 'categories'

class CategorySelectView(ListView):
    model = Product
    template_name = 'mainapp/categoryselect.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = get_object_or_404(SeaCategory, slug=self.kwargs['slug'])
        return Product.objects.filter(product_category=category.id)

class AllProductsOrSpecificView(ListView):
    model = Product
    template_name = 'mainapp/categoryselect.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get('search')

        if name:
            return Product.objects.filter(name__icontains=name.upper())
        else:
            return Product.objects.all()


def delivery(request):
    return render(request, 'mainapp/delivery.html')

def about(request):
    return render(request, 'mainapp/about.html')