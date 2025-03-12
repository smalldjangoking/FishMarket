from django.db.models import Max, Min
from django.views.generic import ListView, DetailView

from mainapp.forms import PriceFilterForm
from mainapp.models import Product, ProductImage, ProductWeight, MoreInformation


class MainPageView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    context_object_name = 'products'
    queryset = Product.objects.order_by('-time_create')[:4]


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product_item.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = ProductImage.objects.filter(product_id=self.object.id)
        context['product_weights'] = ProductWeight.objects.filter(product_id=self.object.id).order_by('-weight')
        context['more_information'] = MoreInformation.objects.filter(product_id=self.object.id).first()
        context['category_related'] = Product.objects.filter(
            product_category_id=self.object.product_category_id).exclude(id=self.object.id)
        return context


class AllProductsOrSpecificView(ListView):
    model = Product
    template_name = 'mainapp/AllProductsOrSearch.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        """
        Receiving and returning quary of products with filters for [search, price-range]
        """
        queryset = super().get_queryset()

        if self.request.GET.get('category'):
            category = self.request.GET.get('category')
            queryset = queryset.filter(product_category__slug=category)

        if self.request.GET.get('search'):
            search_products = self.request.GET.get('search')

            queryset = queryset.filter(name__icontains=search_products.upper())

        if self.request.GET.get('sort'):
            sort_products = self.request.GET.get('sort')

            if sort_products == 'DESC':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')

        price_aggregate = queryset.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )

        if len(price_aggregate) == 2:
            min_product_price = price_aggregate['min_price']
            max_product_price = price_aggregate['max_price']

            if self.request.GET.get('min_price') or self.request.GET.get('max_price'):
                self.requests = {'min_price': self.request.GET.get('min_price'),
                                 'max_price': self.request.GET.get('max_price')}
                self.form = PriceFilterForm(
                    self.requests,
                    min_price=min_product_price,
                    max_price=max_product_price,
                    initial={
                        'min_price': min_product_price,
                        'max_price': max_product_price,
                    }
                )
            else:
                self.form = PriceFilterForm(
                    None,
                    min_price=min_product_price,
                    max_price=max_product_price,
                    initial={
                        'min_price': min_product_price,
                        'max_price': max_product_price,
                    }
                )

            if self.form.is_valid():
                min_price = self.form.cleaned_data['min_price']
                max_price = self.form.cleaned_data['max_price']
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form or None
        return context