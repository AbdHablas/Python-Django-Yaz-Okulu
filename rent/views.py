from json import loads
import stripe
from decouple import config
from win10toast import ToastNotifier
from django.db.models import Q, Avg
from django.utils import timezone
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.html import format_html
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .task import send_pdf_to_email, send_rent_status_to_email
from .models import Car, Rent
from .serializers import RentSerializer


class CheckCouponView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = loads(request.body.decode('utf-8')).get('code')
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon:
                coupon_expired_date = Coupon.objects.get(code=code).expired
                now = timezone.now()
                if now > coupon_expired_date:
                    return Response({'status': 'expired'})
                return Response({'status': 'valid', 'discount': coupon.discount})
        except Coupon.DoesNotExist:
            return Response({'status': 'invalid'})


class CreateRentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RentSerializer

    def perform_create(self, serializer):
        pk = self.request.data.get('pk')
        car = Car.objects.get(pk=pk)
        serializer.save(user=self.request.user, car=car)
        messages.info(self.request,
                      format_html('New rent from {}! <br> Click <a href="{}"> here </a> to view rent.',
                                  self.request.user.get_full_name(), 'http://localhost:8000/admin/rent/rent/' +
                                  str(serializer.data.get('id')) + '/change/'))
        toaster = ToastNotifier()
        toaster.show_toast('New Rent Notification!', f'You rented a new car.', duration=3)


class GetRentsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RentSerializer
    queryset = Rent.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('active') == 'True':
            return self.queryset \
                .filter(Q(approved=True, canceled=False, finished=False, paid=False) |
                        Q(approved=True, canceled=False, finished=False, paid=True))
        if self.request.query_params.get('canceled') == 'True':
            return self.queryset \
                .filter(canceled=True, approved=False, finished=False, paid=False)
        if self.request.query_params.get('finished') == 'True':
            return self.queryset \
                .filter(approved=True, paid=True, finished=True, canceled=False)
        return self.queryset \
            .filter(approved=False, canceled=False, finished=False, paid=False, user=self.request.user)


class CancelRentView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        rent = get_object_or_404(Rent, pk=pk)
        rent.canceled = True
        rent.save()
        messages.info(self.request,
                      format_html('{} cancel the Rent <a href="{}">{}</a>',
                                  self.request.user.get_full_name(),
                                  f'http://localhost:8000/admin/rent/rent/{rent.pk}',
                                  f'#{rent.pk}'))
        send_rent_status_to_email.delay(pk, status='canceled')
        return Response({'canceled': True})




class RateCarView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        rate = loads(request.body.decode('utf-8')).get('rate')
        rent = get_object_or_404(Rent, pk=pk)
        rent.rate = rate
        rent.save()
        car = Car.objects.get(pk=rent.car.pk)
        car.rate = round(car.rents.aggregate(rate=Avg('rate')).get('rate'), 2)
        car.save()
        messages.info(self.request,
                      format_html('{} rated the Car in Rent <a href="{}">{}</a>',
                                  self.request.user.get_full_name(),
                                  f'http://localhost:8000/admin/rent/rent/{rent.pk}',
                                  f'#{rent.pk}'))
        return Response({'rated': True})


@staff_member_required
def admin_send_pdf_rent_detail_to_email(request, pk):
    rent = get_object_or_404(Rent, pk=pk)
    if rent.approved and not rent.paid:
        send_pdf_to_email.delay(pk)
        return HttpResponse(f'<i>Email has been sent successfully to {rent.user.get_full_name()}!</i>')
    return HttpResponseBadRequest('<i>Oops! The rent is not approved yet or it has already been paid.</i>')
