from django.db import models

# Create your models here.
# sozdat tablicu kategoriy
class Category(models.Model):

#     sozdat kolonki dlya tablici
    category_name = models.CharField(max_length=75)
    reg_date = models.DateTimeField(auto_now_add=True)

# vivod informacii v normalnom vide
    def __str__(self):
        return self.category_name

# sozdat tablicu dlya productov
class Product(models.Model):

#   sozdaem kolonki dly tablici productov
    product_name = models.CharField(max_length=125)
    product_count = models.IntegerField()
    product_price = models.FloatField()
    product_photo = models.ImageField(upload_to='media')
    product_des = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    reg_date = models.DateTimeField(auto_now_add=True)

# vivod v нормальном виде

def __str__(self):
    return self.product_name

# esli est image field ispolzuem pip install pillow
class UserCart(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_for_product = models.FloatField()

    # def __str__(self):
    #     return f"{self.quantity} x {self.product.name} = {self.total_for_product}"
    def __str__(self):
        return str(self.product)








