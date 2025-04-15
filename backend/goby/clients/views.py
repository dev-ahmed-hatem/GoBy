from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from django.db.models import Q, F

from .serializers import *
from .models import *
import os


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientWriteSerializer
        return ClientReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        client = self.request.query_params.get('client', None)

        if client is not None:
            if client.isdigit():
                queryset = queryset.filter(id=client)
                if queryset.exists():
                    return queryset
                else:
                    return queryset.none()
            else:
                search = client

        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) |
                Q(name__icontains=search) |
                Q(national_id__icontains=search) |
                Q(phone__icontains=search) |
                Q(phone2__icontains=search))
        return queryset

    @action(detail=True, methods=['PATCH'])
    def change_id(self, request, pk=None):
        client = self.get_object()
        new_id = request.data.get('new_id')
        try:
            c = Client.objects.get(id=new_id)
            if c:
                return Response({"new_id": "كود غير متاح"}, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            client.id = new_id
            if client.qr_code:
                if os.path.isfile(client.qr_code.path):
                    os.remove(client.qr_code.path)
            if client.barcode:
                if os.path.isfile(client.barcode.path):
                    os.remove(client.barcode.path)
            # client.generate_barcode()
            # client.generate_qr_code()
            client.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def requested_photo(self, request, pk=None):
        client = self.get_object()
        action_ = request.data.get('action')
        if action_ == 'accept':
            client.accept_requested_photo()
        else:
            client.delete_requested_photo()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientLogin(APIView):
    def post(self, request):
        id = request.data.get('id')
        password = request.data.get('password')

        if not id or not password:
            return Response({"error": "ID and Password must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(id=id)
            if client.check_password(password):
                return Response(ClientMobileSerializer(client, context={"request": request}).data,
                                status=status.HTTP_200_OK)
            return Response({"error": "incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        except Client.DoesNotExist:
            return Response({"error": "ID is not found!"}, status=status.HTTP_404_NOT_FOUND)


class GetClientData(APIView):
    def post(self, request):
        id = request.data.get('id')
        try:
            client = Client.objects.get(id=id)
            return Response(ClientMobileSerializer(client, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"error": "ID is not found!"}, status=status.HTTP_404_NOT_FOUND)


class ChangeClientPassword(APIView):
    def post(self, request):
        id = request.data.get('id')
        try:
            client = Client.objects.get(id=id)
            serializer = ClientPasswordSerializer(data=request.data, context={"request": request, "id": id})

            if serializer.is_valid(raise_exception=True):
                client.set_password(serializer.validated_data['new_password'])
                client.save()
                return Response({}, status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"error": "ID is not found!"}, status=status.HTTP_404_NOT_FOUND)
