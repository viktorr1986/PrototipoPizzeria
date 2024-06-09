from django.urls import path 
from . import views


urlpatterns = [

    path('users/auth/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('users/auth/', views.login, name="user-login"),

    path('', views.getRoutes, name="routes"),
    path('products/', views.getProducts, name="products"),  
    # path('products/buscar/', views.getProductsBuscar, name="products-buscar"),
    path('products/create/', views.createProduct, name="crear-produto"),   
    path('products/upload/', views.cargarImagen, name="cargar-imagen"),
    path('products/<str:pk>/', views.getProduct, name="product"),
    path('products/delete/<str:pk>/', views.borrarProducto, name="borrar"),
    path('products/update/<str:pk>/', views.updateProduct, name="actualizar-producto"),
    

    path('users/perfil/', views.getUsersPerfil, name="user-perfil"),
    path('users/perfil/update/', views.updateUsersPerfil, name="user-perfil-update"),
    path('users/', views.getUsers, name="user"),

   path('users/registro/', views.registerUser, name="user-registro"),

    #path('users/login/', views.LoginAPIView.as_view(), name="user-login"),
    #path('users/login/', views.loginUser, name="user-login"),
    
    path('login/', views.login, name="login"),
    path('registrarse/', views.registrarse, name="registrarse"),
    path('perfiles/', views.perfiles, name="perfiles"),


    path('orders/adicionar/', views.adicionarItems, name='adicionar-order'),
    path('orders/<str:pk>/', views.obtenerOrdenId, name='obtener-order-id'),
    path('orders/<str:pk>/pagada/', views.actualizarOrdenPagada, name='order-pagada'),
    path('orders/miordenes/', views.obtenerMiOrdenes, name='mi-ordenes'),
    path('orders/ordenes/', views.obtenerOrdenes, name='mi-ordenes'),
    


]