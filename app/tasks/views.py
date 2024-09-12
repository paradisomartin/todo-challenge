from django.utils import timezone
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as dj_filters

class TaskFilter(dj_filters.FilterSet):
    created_at = dj_filters.DateFilter(method='filter_by_date')
    is_completed = dj_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = ['created_at', 'tags__title', 'is_completed']

    def filter_by_date(self, queryset, name, value):
        date_start = timezone.make_aware(timezone.datetime.combine(value, timezone.datetime.min.time()))
        date_end = date_start + timezone.timedelta(days=1)
        return queryset.filter(created_at__gte=date_start, created_at__lt=date_end)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'is_completed']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response({'status': 'task updated', 'is_completed': task.is_completed})

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
