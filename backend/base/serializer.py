from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Producto, Direccion, Order, OrderItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class ProductSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Producto
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Direccion
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    direccion = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    class Meta: 
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
        
    def get_direccion(self, obj):
        try: 
            direccion = DireccionSerializer(obj.direccion, many=False).data
        except: 
            direccion = False
        return direccion
        
    def get_user(self, obj):
        user = obj.Usuario
        serializer = UserSerializer(user, many=False)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    Administrador = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = User
        fields = ['id', '_id', 'username', 'email', 'nombre', 'Administrador']

    def get_nombre(self, obj):
        nombre = obj.first_name
        if nombre == '':
            nombre = obj.email
        return nombre
    
    def get__id(self, obj):
        return obj.id
    
    def get_Administrador(self, obj):
        return obj.is_staff
    

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = User
        fields = ['id', '_id', 'username', 'email', 'nombre', 'Administrador', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

    # def get_tokens(self, obj):   
    #     refresh = RefreshToken.for_user(obj)

    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise 'Usuario no encontrado'
        return user
    

class UserSerializerWeb(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ['id', 'username', 'password', 'email']



class LoginSerializers(serializers.Serializer):
    class Meta:
        model = User

        email = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email and password:

            user = authenticate(username=email, password=password)
            if user:
                data['user'] = user

            data['user'] = user
        return data
    
class UserSerializerFazt(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'password']