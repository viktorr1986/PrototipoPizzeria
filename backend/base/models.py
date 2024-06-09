from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Producto(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Nombre = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='/imagen.jpg')
    #brand = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    # rating = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    # numeroReseña = models.IntegerField(null=True, blank=True, default=0)
    precio = models.PositiveIntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, default=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.Nombre
    
# class Review(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
#     Usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     Nombre = models.CharField(max_length=200, null=True, blank=True)
#     rating = models.IntegerField(null=True, blank=True, default=0)
#     comment = models.TextField(null=True, blank=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.rating)

class Order(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    metodoPago = models.CharField(max_length=200, null=True, blank=True)
    #taxPrice = models.IntegerField(max_digits=8, null=True, blank=True)
    precioEnvio = models.PositiveIntegerField(null=True, blank=True)
    totalPrecio = models.IntegerField(null=True, blank=True)
    pagado = models.BooleanField(default=False)
    pagadoFecha = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    liberado = models.BooleanField(default=False)
    LiberadoFecha = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)
    
class OrderItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    Nombre = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    precio = models.PositiveIntegerField(null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True) 
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.Nombre)
    
# class ShippingAddress(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#     city = models.CharField(max_length=200, null=True, blank=True)
#     postalCode = models.CharField(max_length=200, null=True, blank=True)
#     country = models.CharField(max_length=200, null=True, blank=True)
#     shippingPrice = models.PositiveIntegerField(null=True, blank=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.address)

class Direccion(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.CharField(max_length=200, null=True, blank=True)
    precioEnvio = models.PositiveIntegerField(null=True, blank=True)
    celular = models.PositiveIntegerField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.direccion)



