from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from visitor.views import home
from visitor.views import checkout_visitor, view_gatepass
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("visitor/", include("visitor.urls")),
    path("organisation/", include("organisation.urls")),
    path("home/", home, name="home"),
    path("checkout-visitor/", checkout_visitor, name="checkout-visitor"),
    path("view_gatepass/<uuid:visit_id>", view_gatepass, name="view_gatepass"),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

# Serving media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
