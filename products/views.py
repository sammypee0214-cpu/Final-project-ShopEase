from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAdminUser




def home(request):
    products = Product.objects.filter(available=True)

    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_id:
        products = products.filter(category_id=category_id)

    from .models import Category
    categories = Category.objects.all()

    return render(request, 'products/home.html', {
        'products': products,
        'search_query': search_query,
        'categories': categories,
        'selected_category': category_id,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart

    return redirect('home')
def view_cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('view_cart')

def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        quantity = int(request.POST.get('quantity', 1))

        if product_id in cart and quantity > 0:
            cart[product_id] = quantity

        request.session['cart'] = cart

    return redirect('view_cart')


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('view_cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not all([full_name, email, address, phone]):
            return render(request, 'products/checkout.html', {
                'error': 'Please complete all the fields.'
            })

        cart_items = []
        total = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(
                Product,
                id=product_id,
                available=True
            )

            if not isinstance(quantity, int) or quantity < 1:
                return redirect('view_cart')

            if quantity > product.stock:
                return render(request, 'products/checkout.html', {
                    'error': f'Not enough stock for {product.name}.'
                })

            subtotal = product.price * quantity
            total += subtotal
            cart_items.append((product, quantity))

        order = Order.objects.create(
            full_name=full_name,
            email=email,
            address=address,
            phone=phone,
            total=total
        )

        for product, quantity in cart_items:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save(update_fields=['stock'])

        request.session['cart'] = {}

        return render(request, 'products/checkout.html', {
            'success': True,
            'full_name': full_name,
            'order_id': order.id,
        })

    return render(request, 'products/checkout.html')


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(request, 'products/product_detail.html', {
        'product': product
    })



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([username, email, password, confirm_password]):
            return render(request, 'products/register.html', {
                'error': 'Please complete all fields.'
            })

        if password != confirm_password:
            return render(request, 'products/register.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'products/register.html', {
                'error': 'This username is already taken.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'products/register.html', {
                'error': 'This email is already registered.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return render(request, 'products/register.html', {
            'success': True,
            'username': user.username
        })

    return render(request, 'products/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'products/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'products/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.filter(available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail_api(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def category_list_api(request):
    categories =  Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail_api(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product_api(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_product_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    serializer = ProductSerializer(
        product,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()

    return Response(
        {"message": "Product deleted successfully."},
        status=200
    )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category_api(request):
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_category_api(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    serializer = CategorySerializer(
        category,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category_api(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()

    return Response(
        {"message": "Category deleted successfully."},
        status=200
    )