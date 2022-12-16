from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from user.forms import CustomUserCreationForm
from .models import *
from .forms import *
from .cart import Cart
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, QueryDict
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
import weasyprint
import requests

now = timezone.now()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/login.html'


def product_list(request, category_name=None):
    cart_product_form = CartAddProductForm()
    currency_symbols = {"ALL": "Lek", "AFN": "؋", "ARS": "$", "AMD": "", "AWG": "ƒ", "AUD": "$", "AZN": "₼", "BSD": "$",
                        "BBD": "$", "BYN": "Br", "BZD": "BZ$", "BMD": "$", "BOB": "$b", "BAM": "KM", "BWP": "P",
                        "BGN": "лв", "BRL": "R$", "BND": "$", "KHR": "៛", "CAD": "$", "KYD": "$", "CLP": "$",
                        "CNY": "¥", "COP": "$", "CRC": "₡", "HRK": "kn", "CUP": "₱", "CZK": "Kč", "DKK": "kr",
                        "DOP": "RD$", "XCD": "$", "EGP": "£", "SVC": "$", "EUR": "€", "FKP": "£", "FJD": "$",
                        "GHS": "¢", "GIP": "£", "GTQ": "Q", "GGP": "£", "GYD": "$", "HNL": "L", "HKD": "$", "HUF": "Ft",
                        "ISK": "kr", "INR": "₹", "IDR": "Rp", "IRR": "﷼", "IMP": "£", "ILS": "₪", "JMD": "J$",
                        "JPY": "¥", "JEP": "£", "KZT": "лв", "KPW": "₩", "KGS": "лв", "LAK": "₭",
                        "LBP": "£", "LRD": "$", "MKD": "ден", "MYR": "RM", "MUR": "₨", "MXN": "$", "MNT": " د.إ",
                        "MZN": "MT", "NAD": "$", "NPR": "₨", "ANG": "ƒ", "NZD": "$", "NIO": "C$",
                        "NGN": "₦", "NOK": "kr", "OMR": "﷼", "PKR": "₨", "PAB": "B/.", "PYG": "Gs", "PEN": "S/.",
                        "PHP": "₱", "PLN": "zł", "QAR": "﷼", "RON": "lei", "RUB": "₽", "SHP": "£", "SAR": "﷼",
                        "RSD": "Дин.", "SCR": "₨", "SGD": "$", "SBD": "$", "SOS": "S", "KRW": "₩", "ZAR": "R",
                        "LKR": "₨", "SEK": "kr", "CHF": "CHF", "SRD": "$", "SYP": "£", "TWD": "NT$", "THB": "฿",
                        "TTD": "TT$", "TRY": "₺", "TVD": "$", "UAH": "₴", "AED": " د.إ", "GBP": "£", "USD": "$",
                        "UYU": "$U", "UZS": "лв", "VEF": "Bs", "VND": "₫", "YER": "﷼", "XOF": "", "ZWD": "Z$",
                        "BDT": "",
                        "CLF": "", "CVE": "", "DJF": "", "GNF": "", "HTG": "", "JOD": "", "KWD": "", "LTL": "",
                        "MGA": "", "MOP": "",
                        "MVR": "", "RWF": "", "AOA": "", "SLL": "", "STD": "", "TOP": "", "WST": "", "XAF": "",
                        "ZMK": "", }

    products = []
    url = 'http://api.currencylayer.com/live?access_key='
    api_key = '31ee563c7d5295a62ed091f48b11955c'
    currency_format = '&format=1'
    USD = '&source=USD'
    desired_currency = '&currencies='
    conversion_rate = ""
    currency_code = ""
    true_symbol = ""
    error_message = ""
    request.session.setdefault('currencies', '')
    request.session.setdefault('conversion_rate', 0)

    if request.session.get('currencies', True):
        CurrencyForm(request.GET)

        currency_code = request.session['currencies']
        conversion_rate = request.session['conversion_rate']

        currency_code = str(currency_code)
        conversion_rate = float(conversion_rate)

        print(currency_code)
        print(conversion_rate)
    if request.method == "GET":
        query = request.GET.get('search')
        # print(query)
        if query == '' or query is None:
            query = 'None'
            products = Product.objects.filter(created_date__lte=timezone.now())
        else:
            products = Product.objects.filter(name__icontains=query)

        currency_form = CurrencyForm(request.GET)
        try:
            if currency_form.is_valid():
                #request.session.flush()
                CurrencyForm(request.GET)
                currency_code = request.GET['currencies']
                convert_url = url + api_key + USD + desired_currency + currency_code + currency_format
                currency_conversion = requests.get(convert_url).json()
                print(convert_url)
                USDtoX = 'USD' + currency_code
                conversion_rate = currency_conversion['quotes'][USDtoX]
                true_symbol = currency_symbols[currency_code]
                print(conversion_rate)
                print(currency_code)

                # if request.session.get('currencies', True):
                request.session['currencies'] = currency_code
                request.session['conversion_rate'] = conversion_rate
                print(request.session['conversion_rate'])
                print(request.session['currencies'])
                return render(request, 'magictea/product_list.html',
                              {'products': products,
                               'cart_product_form': cart_product_form,
                               'conversion_rate': conversion_rate,
                               'currency_code': currency_code,
                               'query': query,
                               'true_symbol': true_symbol, })

        except KeyError:
            error_message = "API Error. Symbol or Conversion May Not Be Displayed."

        return render(request, 'magictea/product_list.html',
                      {'products': products,
                       'cart_product_form': cart_product_form,
                       'conversion_rate': conversion_rate,
                       'currency_code': currency_code,
                       'query': query,
                       'true_symbol': true_symbol,
                       'error_message': error_message, })
    return render(request, 'magictea/product_list.html',
                  {'products': products,
                   'cart_product_form': cart_product_form,
                   'conversion_rate': conversion_rate,
                   'currency_code': currency_code,
                   'true_symbol': true_symbol,
                   'error_message': error_message, })


@login_required
def product_detail(request):
    product = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'magictea/product_detail.html',
                  {'products': product})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        # update
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_date = timezone.now()
            product.save()
            return redirect('magictea:product_detail')
    else:
        # edit
        form = ProductForm(instance=product)
    return render(request, 'magictea/product_edit.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('magictea:product_detail')


@login_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('magictea:product_list')
    else:
        form = ProductForm()
        # print("Else")
    return render(request, 'magictea/product_new.html', {'form': form})


def unit_list(request):
    unit = Unit.objects.filter(created_date__lte=timezone.now())
    return render(request, 'magictea/unit_list.html',
                  {'units': unit})


@login_required
def unit_new(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.created_date = timezone.now()
            unit.save()
            return redirect('magictea:unit_list')
    else:
        form = UnitForm()
        # print("Else")
    return render(request, 'magictea/unit_new.html', {'form': form})


@login_required
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == "POST":
        # update
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.updated_date = timezone.now()
            unit.save()
            return redirect('magictea:unit_list')
    else:
        # edit
        form = UnitForm(instance=unit)
    return render(request, 'magictea/unit_edit.html', {'form': form})


@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect('magictea:unit_list')


def category_list(request):
    category = Category.objects.filter(created_date__lte=timezone.now())
    return render(request, 'magictea/category_list.html',
                  {'categorys': category})


@login_required
def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_date = timezone.now()
            category.save()
            return redirect('magictea:category_list')
    else:
        form = CategoryForm()
    return render(request, 'magictea/category_new.html', {'form': form})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        # update
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.updated_date = timezone.now()
            category.save()
            return redirect('magictea:category_list')
    else:
        # edit
        form = CategoryForm(instance=category)
    return render(request, 'magictea/category_edit.html', {'form': form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('magictea:category_list')


def order_list(request):
    order = Order.objects.filter(created_date__lte=timezone.now())
    return render(request, 'magictea/order_list.html',
                  {'orders': order})


def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_MAGIC,
                          [order.email])
    return mail_sent


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        # update
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.updated_date = timezone.now()
            order.save()
            return redirect('magictea:order_list')
    else:
        # edit
        form = OrderForm(instance=order)
    return render(request, 'magictea/order_edit.html', {'form': form})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('magictea:order_list')


@staff_member_required
# @login_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart.add(product=product,
             quantity=cd['quantity'],
             override_quantity=cd['override'])
    return redirect('magictea:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('magictea:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})

    error_message = ""
    try:
        CurrencyForm(request.GET)

        currency_code = request.session['currencies']
        conversion_rate = request.session['conversion_rate']

        currency_code = str(currency_code)
        conversion_rate = float(conversion_rate)

    except KeyError or ValueError or LookupError or UnboundLocalError or TypeError or Exception:
        conversion_rate = 0
        currency_code = ""
        request.session['conversion_rate'] = conversion_rate
        request.session['currencies'] = currency_code
        error_message = "API Error. Symbol or Conversion May Not Be Displayed."
        return render(request, 'cart/detail.html', {'cart': cart,
                                                    'currency_code': currency_code,
                                                    'conversion_rate': conversion_rate,
                                                    'error_message': error_message})
    return render(request, 'cart/detail.html',
                  {'cart': cart, 'error_message': error_message, 'currency_code': currency_code,
                   'conversion_rate': conversion_rate, })


def get_recipes(request):
    recipes = getRecipeByIngredients("tea")
    return render(request, 'magictea/get_recipe.html',
                  {'recipes': recipes})


# Reference https://stackoverflow.com/questions/47627030/spoonacular-api-integration-with-python
def getRecipeByIngredients(ingredients):
    api_key = settings.SPOONACULAR_API_KEY
    searchRecipesURL = "https://api.spoonacular.com//recipes/findByIngredients?ingredients=tea&number=8&limitLicense=true&ranking=1&ignorePantry=false"
    results = requests.get(url=searchRecipesURL, params={"apiKey": api_key}).json()

    recipeURL = "https://api.spoonacular.com//recipes/<id>/information?includeNutrition=false"
    recipes = []
    for result in results:
        temp = requests.get(url=recipeURL.replace("<id>", str(result['id'])), params={"apiKey": api_key}).json()
        recipes.append(recipe(temp['title'], temp['sourceUrl'], temp['image'], temp['summary'], temp['sourceName'], temp['id']))

    return recipes


class recipe:
    def __init__(self, title, url, image, summary, sourceName, id):
        self.title = title
        self.url = url
        self.image = image
        self.summary = summary
        self.sourceName = sourceName
        self.id = id


@csrf_exempt
@api_view(['GET', 'POST'])
def order_details(request):
    permission_classes = (IsAuthenticatedOrReadOnly)
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getOrder(request, pk):
    """
    Retrieve, update or delete a order instance.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
