from django.shortcuts import render, redirect
from django.template.context_processors import request
from .models import Partner, PartnerProduct, PartnerType, Region, Settlement, Street, House
from django.db.models import Q

def show_partners(request):
    partners = Partner.objects.all()

    context = {
       'partners': partners
    }
    return render(request, 'partner_list.html', context)

#добавление партнера
def add(request):
    if request.method == 'POST': #Получение всех данных
        inn = request.POST.get('inn')
        partner_type_id = request.POST.get('partner_type')
        partner_name = request.POST.get('partner_name')
        director = request.POST.get('director')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        rating = request.POST.get('rating')
        house_id = request.POST.get('house')
        #получение через всязь
        partner_type = PartnerType.objects.get(id_partner_type=partner_type_id)
        house = House.objects.get(id=house_id)
        #Создание партнера через то что приняли и присвоили
        Partner.objects.create(
            inn=inn,
            partner_type=partner_type,
            partner_name=partner_name,
            director=director,
            email=email,
            phone=phone,
            legal_address=house,
            rating=rating,
        )
    #получение весех данных для формы
    partner_types = PartnerType.objects.all()
    regions = Region.objects.all()
    settlements = Settlement.objects.all()
    streets = Street.objects.all()
    houses = House.objects.all()

    context = {
        'partner_types': partner_types,
        'regions': regions,
        'settlements': settlements,
        'streets': streets,
        'houses': houses,
    }
    return render(request, 'add_partner.html', context) #вывод всего на страницу добавления партнеров

#Для редактирования существующих партнеров
def edit_partner(request):
    partners = Partner.objects.all()
    selected_partner = None

    partner_id = request.GET.get('partner_id') #получение айди партнера

    if partner_id: #проверка на существование
        try:
            selected_partner = Partner.objects.get(inn=partner_id)
        except Partner.DoesNotExist:
            selected_partner = None

    #метод редактирования партнера по его id
    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        try:
            partner = Partner.objects.get(inn=partner_id)
            partner.partner_name = request.POST.get('partner_name')
            partner.director = request.POST.get('director')
            partner.email = request.POST.get('email')
            partner.phone = request.POST.get('phone')
            partner.rating = request.POST.get('rating')
            partner.save()
        except Partner.DoesNotExist:
            pass

    context = {
        'partners': partners,
        'selected_partner': selected_partner,
    }
    return render(request, 'edit_partner.html', context)#вывод на страничку редактированяи партнера

#История партнера
def history(request):
    partners = Partner.objects.all()
    selected_partner = None
    products = [] #для хранения всех продуктов партнера
    #Получаем партнера
    partner_id = request.GET.get('partner_id')
    if partner_id:
        try:
            selected_partner = Partner.objects.get(inn=partner_id)
            products = PartnerProduct.objects.filter(partner=selected_partner).select_related(
                'product__product_type'
            )
        except Partner.DoesNotExist:
            selected_partner = None

    context = {
        'partners': partners,
        'selected_partner': selected_partner,
        'products': products,
    }
    return render(request, 'history_partner.html', context) #возврат содержимого на историю партнера


def login(request): #сделано для красивого вида, просто как страничка подрозумевающая вход
    logins = Partner.objects.all()
    context = {
        'logins': logins
    }
    return render(request, 'login.html', context)