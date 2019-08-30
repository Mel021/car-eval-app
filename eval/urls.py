from django.urls import path
from . import views

#app_name = 'eval'

#urlpatterns = [path('train/',views.Train,name='Train'),path('predict/',views.predict,name='predict'),]
urlpatterns = [path('getclass/',views.get_class,name='get_class'),path('cartrain/',views.Car_Train.as_view(),name='Car_Train'),path('carpredict/',views.Car_Predict.as_view(),name='Car_Predict'),path('',views.home,name='home'),path('index/',views.index,name='index'),]
