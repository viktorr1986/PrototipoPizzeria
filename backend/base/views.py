from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from .models import Producto, Order, OrderItem, Direccion
from .products import products
from .serializer import ProductSerializer, OrderSerializer, UserSerializer, UserSerializerWithToken, LoginSerializers, UserSerializerFazt

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        #token['username'] = self.user.username
        #token['email'] = self.user.email
        # ...
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products',
        '/api/products/create/',

        '/api/products/upload/',

        '/api/products/<id>/reviews/',

        '/api/products/top/',
        '/api/products/<id>/',

        '/api/products/delete/<id>/',
        '/api/products/<update>/<id>/',

    ]
    return Response(routes)

@api_view(['GET'])
def getUsersPerfil(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUsersPerfil(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
     
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    
    user.save()

    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):

    data = request.data
    print(data)
    try:
        user = User.objects.create(
            first_name = data['name'], 
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
            # serializer = UserSerializer(user, many=False)
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except: 
        mensaje = {'detail':'Usuario con este email ya existe...'}
        return Response(mensaje, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    print('query: ', query)
    if query == None:
        query = ''
    # products = Producto.objects.all()
    products = Producto.objects.filter(Nombre__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def getProductsBuscar(request):
#     query = request.query_params.get('keyword')
#     print('query: ', query)
#     if query == None:
#         query = ''
#     products = Producto.objects.filter(name__icontains=query)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Producto.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def borrarProducto(request, pk):
    product = Producto.objects.get(_id=pk)
    product.delete()
    return Response({'detail':'Producto borrado'})


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Producto.objects.create(
        Usuario = user ,
        Nombre='Producto Nuevo',
        precio=0,
        stock=0,
        categoria='Categoria',
        descripcion='Descripcion'
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Producto.objects.get(_id=pk)

    product.Nombre = data['Nombre']
    product.precio = data['precio']
    product.stock = data['stock']
    product.categoria = data['categoria']
    product.descripcion = data['descripcion']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def cargarImagen(request):
    data = request.data
    product_id = data['product_id']
    product = Producto.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response({'detail':'Imagen cargada'})

# class LoginAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = LoginSerializers(data=data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # user = serializer.validated_data['user']
#         # update_last_login(None, user)
#         # token, created = Token.objects.get_or_create(user=user)
#         # return Response({"status": status.HTTP_200_OK, "Token": token.key})
#         # return Response(serializer.data, {"status": status.HTTP_200_OK})
#         return Response(serializer.data)


@api_view(['POST'])
def login(request): 
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error":"Invalido la contraseña"}, status=status.HTTP_400_BAD_REQUEST)
    token, created =Token.objects.get_or_create(user=user)
    serializer =UserSerializerFazt(instance=user)    
    return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_200_OK)  


@api_view(['POST'])
def registrarse(request): 

    serializer  = UserSerializerFazt(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)
    print(request.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfiles(request): 
    print(request.user)
    serializer = UserSerializerFazt(instance=request.user)
    # return Response("Perfil {}".format(request.user.username), status=status.HTTP_200_OK)  
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adicionarItems(request): 
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({"detail":"No hay productos"}, status=status.HTTP_400_BAD_REQUEST)
    
    else: 
        order = Order.objects.create(
            Usuario = user,
            metodoPago = data['metodoPago'],
            precioEnvio = data['precioEnvio'],
            totalPrecio = data['totalPrecio']

        )

        direccion = Direccion.objects.create(
            order = order,
            direccion=data['direccionCompra']['direccion'],
            ciudad=data['direccionCompra']['ciudad'],
            celular=data['direccionCompra']['celular']
        )


        for i in orderItems:
            # if 'producto' not in i:
            #     print('producto')
            #     return Response({"Error": "Falta la clave 'producto'"}, status=status.HTTP_400_BAD_REQUEST)
            # producto = Producto.objects.get(_id=i['producto'])
            producto = Producto.objects.get(_id=i['_id'])
            # producto = Producto.objects.get(_id=2)   #productos ewwe
            # producto = Producto.objects.filter(_id = i['producto'])
  

            item = OrderItem.objects.create(
                producto= producto,
                order= order,
                Nombre= producto.Nombre,
                qty= i['qty'],
                precio= i['precio'],
                image= producto.image.url

            )

            # producto.stock -= item.qty
            producto.save()
        
        serializer = OrderSerializer(order, many=False)

        return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def obtenerOrdenId(request, pk):
#     user = request.user
#     try: 
#         order = Order.objects.get(_id=pk)
#         serializer = OrderSerializer(order, many=False)
#         return Response(serializer.data)
#         # if user.Administrador or order.user == user:           # Administrador  # is_staff
#         #     serializer = OrderSerializer(order, many=False)
#         #     return Response(serializer.data)
#         # else:
#         #     Response({'detail': 'No estas autorizado'}, status=status.HTTP_400_BAD_REQUEST)
#     except: 
#         return Response({'detail': 'La orden no existe...'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerOrdenId(request, pk):
    Usuario = request.user
    try: 
        order = Order.objects.get(_id=pk)

        if Usuario.is_staff or order.Usuario == Usuario:           # Administrador  # is_staff
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'No estas autorizado'}, status=status.HTTP_400_BAD_REQUEST)
    except: 
        return Response({'detail': 'La orden no existe...'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizarOrdenPagada(request, pk):
    order = Order.objects.get(_id=pk)
    order.pagado = True
    order.pagadoFecha = datetime.now()
    order.save()
    return Response({'detail':'Orden pagada'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerMiOrdenes(request):
    user = request.user   
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenerOrdenes(request): 
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)