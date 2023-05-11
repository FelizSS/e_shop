from django.shortcuts import render, redirect
from . models import Category, Product, UserCart
from . import models
from .forms import SearchForm
from telebot import TeleBot

bot = TeleBot('6082800610:AAEd4pHylIN6TPt8BrRRlA6RlzKjierowhc', parse_mode="HTML")



# Create your views here.

def index(request):
    # berem vse kategorii s bazi dannih

    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()
    search_bar = SearchForm ()

    context = {'all_categories': all_categories,
               'products': all_products,
               'form': search_bar}

    if request.method == 'POST':
        product_find = request.POST.get('search_product')
        try:
            search_result = models.Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')

    # peredaem na front
    return render(request, 'index.html', context)

# poluchit opredelenniy product

def get_exact_product(request,pk):
    product = models.Product.objects.get(id=pk)
    context = {'product': product}

    if request.method == 'POST':

        models.UserCart.objects.create(user_id=request.user.id,
                                       product=product,
                                       quantity=request.POST.get('quantity'),
                                       total_for_product = product.product_price*int(request.POST.get('quantity')))
        return redirect('/cart')

    return render(request, 'about_product.html', context)


def current_category(request, pk):
    category = models.Category.objects.get(id=pk)

    context = {'product': category}
    return render(request, 'current_category.html', context)

def get_exact_category(request, pk):
    # poluchaem categorii
    exact_category = models.Category.objects.get(id=pk)
    categories = models.Category.objects.all()
    # vivodim product iz etoy categorii
    category_products = models.Product.objects.filter(product_category=exact_category)

    return render(request, 'categrory_products.html', {'category_products': category_products,
                                                      'categories': categories})

def get_user_cart(request):

    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    total = [i.total_for_product for i in user_cart]
    context = {'cart': user_cart, 'total': total}

    return render(request, 'user_cart.html', {'cart': user_cart}, context)

# oformlenie zakazov

def complete_order(request):

    # poluchaem korzinu polzovatelya
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)

    #formiruem soobsheniya dlya tg admina
    result_message = 'Новый заказ(Сайт)\n\n'
    total_for_all_cart = 0
    for cart in user_cart:
        result_message += f'<b>{cart.product}</b> x {cart.quantity} = {cart.total_for_product} сум\n'

        total_for_all_cart += cart.total_for_product
    result_message += f'\n---------\n<b>Итого: {total_for_all_cart} сум</b>'

    # otpravlyaem adminu soobshenie v tg
    bot.send_message(140566, result_message)

    return redirect('/')