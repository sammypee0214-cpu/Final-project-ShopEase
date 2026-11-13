from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Product, Order, OrderItem
from .forms import ProductForm, CategoryForm
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
    categories = Category.objects.all()
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


@login_required
@user_passes_test(lambda user: user.is_staff)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Create Product'
    })

@login_required
@user_passes_test(lambda user: user.is_staff)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('home')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })