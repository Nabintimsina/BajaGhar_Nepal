from datetime import timedelta

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Category, Instrument, Expert, LearningContent, Contact, Tutorial, TunerConfiguration, Branding
from .serializers import (
    CategorySerializer,
    InstrumentListSerializer,
    InstrumentDetailSerializer,
    ExpertListSerializer,
    ExpertDetailSerializer,
    LearningContentSerializer,
    ContactSerializer,
    TutorialSerializer,
    TunerConfigurationSerializer,
    BrandingSerializer,
)
from .permissions import IsAdminOrReadOnly
from .filters import InstrumentFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'description']


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.select_related('category').prefetch_related('experts')
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = InstrumentFilter
    search_fields = ['name', 'description', 'history', 'materials', 'cultural_significance']
    ordering_fields = ['name', 'region', 'created_at']

    def get_serializer_class(self):
        # Use the detailed serializer for retrieve and write operations
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return InstrumentDetailSerializer
        return InstrumentListSerializer

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def tutorials(self, request, pk=None):
        instrument = self.get_object()
        tutorials = instrument.tutorials.all()
        serializer = TutorialSerializer(tutorials, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def tuner_config(self, request, pk=None):
        instrument = self.get_object()
        try:
            config = instrument.tuner_config
            serializer = TunerConfigurationSerializer(config, context={'request': request})
            return Response(serializer.data)
        except TunerConfiguration.DoesNotExist:
            return Response(None)


class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.prefetch_related('instruments')
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'expertise']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExpertDetailSerializer
        return ExpertListSerializer


class LearningContentViewSet(viewsets.ModelViewSet):
    queryset = LearningContent.objects.all()
    serializer_class = LearningContentSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['order', 'title']
    http_method_names = ['get', 'head', 'options']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    ordering_fields = ['created_at']
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR') or 'unknown'

    def _is_rate_limited(self, request):
        rate_limit = getattr(settings, 'CONTACT_FORM_RATE_LIMIT', 3)
        time_window = getattr(settings, 'CONTACT_FORM_TIME_WINDOW', 86400)
        client_ip = self._get_client_ip(request)
        window_start = timezone.now() - timedelta(seconds=time_window)
        recent_count = Contact.objects.filter(
            ip_address=client_ip,
            created_at__gte=window_start,
        ).count()

        if recent_count >= rate_limit:
            first_submission = (
                Contact.objects.filter(
                    ip_address=client_ip,
                    created_at__gte=window_start,
                )
                .order_by('created_at')
                .values_list('created_at', flat=True)
                .first()
            )
            if first_submission is None:
                return True, None

            reset_at = first_submission + timedelta(seconds=time_window)
            wait_seconds = max(1, int((reset_at - timezone.now()).total_seconds()))
            return False, wait_seconds

        return True, None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        allowed, wait_seconds = self._is_rate_limited(request)
        if not allowed:
            return Response(
                {
                    'detail': (
                        'Contact form limit reached. Please try again in '
                        f'{wait_seconds} seconds.'
                    )
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer.save(ip_address=self._get_client_ip(request))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'instructor_name']
    ordering_fields = ['created_at', 'instructor_name']


class TunerConfigurationViewSet(viewsets.ModelViewSet):
    queryset = TunerConfiguration.objects.all()
    serializer_class = TunerConfigurationSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['tuning_name', 'is_default']


class BrandingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        branding, _ = Branding.objects.get_or_create(
            pk=1,
            defaults={
                'name': getattr(settings, 'BRANDING_NAME', 'BAJAGHAR'),
                'contact_email': getattr(settings, 'BRANDING_CONTACT_EMAIL', 'info@bajanepal.com'),
            },
        )
        serializer = BrandingSerializer(branding, context={'request': request})
        return Response(serializer.data)
