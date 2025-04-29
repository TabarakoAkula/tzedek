from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url="/static/favicon.ico", permanent=True)

urlpatterns = [
    re_path(r"^favicon\.ico$", favicon_view),
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/questions/", include("apps.questions.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
