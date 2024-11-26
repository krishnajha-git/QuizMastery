from django.db import models

from django.db import models

class QuizCreator(models.Model):
    creater_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Add name field for Quiz Creator
    email = models.EmailField(unique=True)   # Ensure unique emails
    password = models.CharField(max_length=128)  # To store hashed password

    def __str__(self):
        return self.email


# 2. Quiz Details (Basic Quiz Information)
class QuizDetails1(models.Model):
    creator = models.ForeignKey(QuizCreator, to_field='creater_id', on_delete=models.CASCADE)
    quiz_id = models.AutoField(primary_key=True)
    quiz_img = models.ImageField(upload_to='quiz/profile/', null=True, blank=True)
    created_by = models.CharField(max_length=150) 
    title_quiz = models.CharField(max_length=300)
    description_quiz = models.TextField(max_length=300)

    def __str__(self):
        return self.title_quiz

# 3. Quiz Questions and Options
class QuizDetails2(models.Model):
    quiz = models.ForeignKey(QuizDetails1, on_delete=models.CASCADE)
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self):
        return f"Question {self.question_id} in {self.quiz.title_quiz}"

# 4. Response Table (Records Quiz Attempts)
class Response1(models.Model):
    quiz = models.ForeignKey(QuizDetails1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    email = models.EmailField(max_length=100, default="example@example.com")
    question = models.ForeignKey(QuizDetails2, on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=300)
    points = models.IntegerField()
    id = models.BigAutoField(primary_key=True)
        
        
    def __str__(self):
        return f"Response by {self.name} for Quiz {self.quiz.title_quiz}"
