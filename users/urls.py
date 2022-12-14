from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path

from .views import (cabinet,
                    clean_shopping_cart,
                    favorite_product,
                    ordering,
                    order_detail,
                    order_list,
                    shopping_cart,
                    SignUp)

app_name = 'users'


urlpatterns = [
    path('cabinet/', cabinet, name='cabinet'),
    path('cabinet/favorite_product',
         favorite_product, name='favorite_product'),
    path('cabinet/shopping_cart', shopping_cart, name='shopping_cart'),
    path('cabinet/shopping_cart/clean_shopping_cart',
         clean_shopping_cart, name='clean_shopping_cart'),
    path('cabinet/ordering', ordering, name='ordering'),
    path('cabinet/order_detail/<int:order_id>',
         order_detail, name='order_detail'),
    path('cabinet/order_list', order_list, name='order_list'),

    # аутентификация
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/',
         LogoutView.as_view(),
         name='logout'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html'
         ),
         name='password_change_form'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html'
         ),
         name='password_reset_form'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete')
]
