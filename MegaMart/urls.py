"""FastDMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import  views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('index/', views.index, name="index"),

    path('submitlogin/', views.submitLogin, name="submitlogin"),

    path('addproduct/', views.addProduct, name="addproduct"),
    path('saveproduct/', views.saveProduct, name="saveproduct"),

    path('showproduct/', views.showProduct, name="showproduct"),
    path('showproductsingle/', views.showProductSingle, name="showproductsingle"),
    path('printqr/', views.printqr, name="printqr"),
    path('printIntoPdf/<int:sid>', views.printIntoPdf, name="printIntoPdf"),
    

    path('additem/', views.addItem, name="additem"),
    path('clearbill/', views.clearBill, name="clearbill"),
    path('qtyplus/<int:sid>', views.qtyPlus, name="qtyplus"),
    path('qtyminus/<int:sid>', views.qtyMinus, name="qtyminus"),
    path('deleteprod/<int:sid>', views.deleteProd, name="deleteprod"),
    path('showscgst/', views.showscgst, name="showscgst"),
    path('showigst/',views.showigst,name='showigst'),
    path('insertInvoiceRecord/',views.insertInvoiceRecord,name='insertInvoiceRecord'),
    
    

    # # path('canclescanne/', views.cancleScanne, name="canclescanne"),
    # path('test/', views.test, name="test"),

]
