
from django.urls import path
from rent.views import CreateRentView,  admin_send_pdf_rent_detail_to_email, GetRentsView, CancelRentView, RateCarView

app_name = 'rent'

urlpatterns = [
    path('create/', CreateRentView.as_view(), name='create'),
    path('admin/rent/<int:pk>/send-pdf/', admin_send_pdf_rent_detail_to_email, name='send_pdf_to_email'),
    path('get-rents/', GetRentsView.as_view(), name='get_rents'),
    path('<int:pk>/cancel/', CancelRentView.as_view(), name='cancel_rent'),
    path('<int:pk>/rate-car/', RateCarView.as_view(), name='rate_car'),
]
