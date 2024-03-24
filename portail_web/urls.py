from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='Home'),
    path('Apropos', views.about , name='about'),
    path('Services', views.service , name='service'),
    path('Expertises', views.expertise , name='expertise'),
    path('Carriere', views.carriere , name='carriere'),
    path('detail-expertise/<detail>', views.detailSecteur , name='detail_secteur'),
    path('Contact', views.contact , name='contact'),
    path('Detail/<int:id_post>', views.getDetail , name='detail'),
    path('Postuler/<int:id_post>', views.postuler , name='postuler'),
    path('Postuler-offre',views.postulerOffres, name='offre'),
    path('Spontaner/',views.postulerSpontaner,name='spontaner'),
]