from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from product.models import Variant, Product
from forms import ProductFilterForm

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10  # Set the number of items per page
    form_class = ProductFilterForm

    def get_queryset(self):
        queryset = Product.objects.all()
        form = self.form_class(self.request.GET)
        
        if form.is_valid():
            title = form.cleaned_data.get('title')
            variant = form.cleaned_data.get('variant')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            created_at = form.cleaned_data.get('created_at')

            if title:
                queryset = queryset.filter(title__icontains=title)
            if variant:
                queryset = queryset.filter(productvariant__variant_title__icontains=variant)
            if min_price:
                queryset = queryset.filter(productvariantprice__price__gte=min_price)
            if max_price:
                queryset = queryset.filter(productvariantprice__price__lte=max_price)
            if created_at:
                queryset = queryset.filter(created_at__date=created_at)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.GET)
        context['form'] = form

        # Customize the response with the range summary
        paginator = Paginator(context['products'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        context['products'] = paginated_products
        context['start_index'] = paginated_products.start_index()
        context['end_index'] = paginated_products.end_index()
        context['total_count'] = paginator.count

        return context