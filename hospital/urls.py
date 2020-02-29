from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from hospital import settings
from server import views

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
        re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name="home"),
    path('home/', views.HomeView.as_view(), name="home"),
    path('chat_box/',views.ChatbotView),
    path('signin/', views.SignInView.as_view(), name="signin"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    #path('404NotFound/', ??, name="404NotFound"),
    #Patient
    path('appointment/', views.AppointmentView.as_view(), name="appointment"),
    # appointment sub-views
    path('get_clinic/',views.Step_1),#POST selected examination
    path('get_clinic_info/', views.get_clinic_info),
    path('get_clinic_name/',views.Step_2),#GET clinic name by clinic id
    path('get_clinic_and_date/', views.Step_3),#GET timeslots from selected: examination, clinic, date
    path('send_date/', views.Step_6),#POST insert new appointment record to database and send email
    ###
    path('patient_profile/', views.ProfileView.as_view(),name="patient_profile"),
    path('bookings/', views.PatientBookingView.as_view(), name="bookings"),
    #Clinic
    path('dashboard/', views.ClinicDashBoardView.as_view(), name="dashboard"),
    path('requestlist/',views.RequestListView.as_view(),name='requestlist'),
    # requestlist views
    path('refese_reqest/', views.refese_reqest),# cancel a request
    path('approve_reqest/',views.approve_reqest),# approve a request
    ###
    path('upload_report/', views.UploadReportView.as_view(), name="upload_report"),
    path('statictics/',views.get_statistics, name='statistics'),
    path('clinic_profile/',views.ClinicProfileView.as_view(), name = 'clinic_profile'),
    # path('clinic_schedule/', views.DocScheduleView.as_view(), name="clinic_schedule")
    # path('schedule/', views.ScheduleApiView.as_view(),name="api_schedule")
]

