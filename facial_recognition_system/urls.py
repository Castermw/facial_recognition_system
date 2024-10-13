from django.contrib import admin
from django.urls import path, include
from attendance.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include('attendance.urls')),  # Include app-level URLs
     path('', home, name='home'),  # Add a path for the home view
]
