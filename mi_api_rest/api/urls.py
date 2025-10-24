from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

schema_view = get_schema_view(
	openapi.Info(
		title="Fintech API",
		default_version='v1',
		description="Documentación de la API Fintech",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

@api_view(['GET'])
def custom_api_root(request, format=None):
	return Response({
		'accounts': request.build_absolute_uri('accounts/'),
		'transactions': request.build_absolute_uri('transactions/'),
		'swagger': request.build_absolute_uri('swagger/'),
	})

urlpatterns = [
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('', custom_api_root, name='api-root'),
] + router.urls