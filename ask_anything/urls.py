from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views
from ask_anything import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('index', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('profile/edit', views.settings, name='settings'),
    path('ask', views.ask, name='ask'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('signup', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
