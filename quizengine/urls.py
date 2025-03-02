from django.contrib import admin
from django.urls import path,include
from . import views 


app_name = "quizengine" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home, name="home"),
    path('about/',views.about, name="about"),
    path('contact',views.contact,name="contact"),

    path('service',views.service,name="service"),
    path('get_video_comments/',views.get_video_comments,name="get_video_comments"),
    path('fetch_comments_view/', views.fetch_comments_view, name='fetch_comments_view'),

    path('creatingQuiz/',views.creatingQuiz,name='creatingQuiz'),
    path("news_view/", views.news_view, name="news_view"),
    
    path("web_saper/", views.web_saper, name="web_saper"),
    path("recommender", views.recommender, name="recommender"),


    # Quiz
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('get_question/', views.get_question, name='get_question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.results, name='results'),
    path('reset/', views.reset_quiz, name='reset_quiz'),
]


