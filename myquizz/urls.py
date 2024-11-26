from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quizz/', QuizListView.as_view(), name='quiz-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('attend-quiz/<int:quiz_id>/', AttendQuizView.as_view(), name='attend-quiz'),
    path('quiz-check/<int:quiz_id>/', QuizCheckView.as_view(), name='quiz-check'),
    path('edit-question/<int:question_id>/', EditQuestionView.as_view(), name='edit-question'),
    path('response/<int:quiz_id>/', ResponseView.as_view(), name='response'),
    path('edit-quizdetail/<int:quiz_id>/', EditQuizdetailView.as_view(), name='edit-quizdetail'),
    path('add-question/<int:quiz_id>/', AddQuestionView.as_view(), name='add-question'),
    path('question-answer/<int:quiz_id>/<str:name>/<str:email>/', QuestionAnswerView.as_view(), name='question-answer'),
    path('myquiz/', MyQuizView.as_view(), name='myquiz'),
    path('share/<int:quiz_id>/', ShareView.as_view(), name='share'),
    path('create-quiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('delete-quiz/', DeleteQuizView.as_view(), name='delete-quiz'),
    path('delete-question/', DeleteQuestionView.as_view(), name='delete-question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

