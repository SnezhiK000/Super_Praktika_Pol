from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, EmailValidator


class ProductType(models.Model): #Модель продукта
    id = models.AutoField(primary_key=True)
    product_type = models.CharField(max_length=100, verbose_name='Тип продукции')
    product_type_coefficient = models.FloatField(verbose_name='Коэффициент типа продукции')

    def __str__(self):
        return self.product_type


class PartnerType(models.Model): #Модель для типа партнера
    id_partner_type = models.AutoField(primary_key=True)
    partner_type = models.CharField(max_length=50, verbose_name='Тип партнера')

    def __str__(self):
        return self.partner_type

class MaterialType(models.Model): #Материалы (пока не поняла для чего они, но они тоже есть. В описании вроде нигде пока не используются)
    material_type = models.CharField(primary_key=True, max_length=50, verbose_name='Тип материала')
    defect_percentage = models.FloatField(verbose_name='Процент брака материала')

    def __str__(self):
        return self.material_type

class Product(models.Model): #Продукт
    article = models.CharField(primary_key=True, max_length=50, verbose_name='Артикул')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name='Тип продукции')
    material = models.ManyToManyField(MaterialType, verbose_name='Тип материала')
    product_name = models.CharField(max_length=255, verbose_name='Наименование продукции')
    min_partner_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная стоимость для партнера')


    def __str__(self):
        return f"{self.article} - {self.product_name}"


class PostalCode(models.Model): #Индекс
    postal_code = models.CharField(primary_key=True, max_length=6, verbose_name='Почтовый индекс')

    def __str__(self):
        return self.postal_code


class Region(models.Model): #Регион с индексом
    region_code = models.CharField(primary_key=True, max_length=10, verbose_name='Код региона')
    region = models.CharField(max_length=100, verbose_name='Регион')
    postal_code = models.ForeignKey(PostalCode, on_delete=models.CASCADE, verbose_name='Почтовый индекс')

    def __str__(self):
        return self.region


class Settlement(models.Model):
    id = models.AutoField(primary_key=True)
    settlement = models.CharField(max_length=100, verbose_name='Населенный пункт')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')

    def __str__(self):
        return self.settlement


class Street(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100, verbose_name='Улица')
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE, verbose_name='Населенный пункт')

    def __str__(self):
        return f"{self.street}, {self.settlement.settlement}"


class House(models.Model):
    id = models.AutoField(primary_key=True)
    house = models.CharField(max_length=10, verbose_name='Дом')
    street = models.ForeignKey(Street, on_delete=models.CASCADE, verbose_name='Улица')

    def __str__(self):
        return f"{self.street.street}, {self.house}"


# Валидация (шаблон) по которому должен быть заполнен телефон и почта
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Телефон должен быть в формате: '+999999999'. Допускается до 15 цифр."
)

email_validator =(EmailValidator
    (
    message="Введите корректный email адрес."
    )
)


class Partner(models.Model): #Партнер
    inn = models.CharField(primary_key=True, max_length=12, verbose_name='ИНН')
    partner_type = models.ForeignKey(PartnerType, on_delete=models.CASCADE, verbose_name='Тип партнера')
    partner_name = models.CharField(max_length=255, verbose_name='Наименование партнера')
    director = models.CharField(max_length=255, verbose_name='Директор')
    email = models.EmailField( #поле почты для валидации
        verbose_name='Электронная почта партнера',
        validators=[email_validator] #валидация
    )
    phone = models.CharField( #поле телефона с валидацией
        max_length=20,
        verbose_name='Телефон партнера',
        validators=[phone_validator] #валидация
    )
    legal_address = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='Юридический адрес партнера')
    rating = models.IntegerField(verbose_name='Рейтинг')

    def procent(self): #функция расчета процентной скидки, суммирая всё что есть у каждого партнера по продажам

        total_quantity = PartnerProduct.objects.filter(partner=self).aggregate(total=models.Sum('quantity', default=0))['total']

        if total_quantity > 0 and total_quantity <= 10000: #просто сравниваю колличество всей продукции партнера с значениями для скидки
            skid = 0
        elif total_quantity > 10000 and total_quantity <= 50000:
            skid = 5
        elif total_quantity > 50000 and total_quantity <= 300000:
            skid = 10
        else:
            skid = 15
        return skid

    def __str__(self):
        return self.partner_name



class PartnerProduct(models.Model): #Продукция-партенеры. Связывающая таблица
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Наименование партнера')
    quantity = models.IntegerField(verbose_name='Количество продукции')
    sale_date = models.DateTimeField(verbose_name='Дата продажи')

    def __str__(self):
        return f"{self.partner.partner_name} - {self.product.product_name}"
