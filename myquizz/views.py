from django.db.models import Q
from django.shortcuts import *
from django.views import *
from .models import *
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.views import View
from django.forms import formset_factory
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm
from .models import QuizCreator
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import logging

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class RegisterView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            form.save()  # Save the user data if the form is valid
            messages.success(self.request, "Registration successful. Please log in.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"An error occurred during registration: {e}")
            return self.form_invalid(form)  # Render the form with errors

    def form_invalid(self, form):
        # Add a generic error message for invalid forms
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('myquiz')  # Adjust this to your intended redirect

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Check if user exists with provided email
        try:
            user = QuizCreator.objects.get(email=email)
            if check_password(password, user.password):  # Verifying password
                # Set session with creator_id
                self.request.session['creater_id'] = user.creater_id
                return super().form_valid(form)
            else:
                form.add_error('password', 'Incorrect password.')
        except QuizCreator.DoesNotExist:
            form.add_error('email', 'Email not registered.')

        return self.form_invalid(form)

    def form_invalid(self, form):
        # This will re-render the form with error messages
        return super().form_invalid(form)

class LogoutView(View):
    def post(self, request):
        auth_logout(request)  # This will log the user out
        return redirect('login')  

from django.views.generic import TemplateView



class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('myquiz')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # Check if user exists with the provided email
        try:
            user = QuizCreator.objects.get(email=email)
            if check_password(password, user.password):  # Verify password
                # Set session with creater_id and name
                self.request.session['creater_id'] = user.creater_id
                self.request.session['name'] = user.name  # Save name to session
                return super().form_valid(form)
            else:
                form.add_error('password', 'Incorrect password.')
        except QuizCreator.DoesNotExist:
            form.add_error('email', 'Email not registered.')

        return self.form_invalid(form)

    def form_invalid(self, form):
        # Re-render the form with error messages
        return super().form_invalid(form)

class MyQuizView(TemplateView):
    template_name = 'myquiz.html'

    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creater_id = self.request.session['creater_id']
        name = self.request.session.get('name', '')  # Get name from session

        # Get search and sort parameters from the request
        search_query = self.request.GET.get('search', '').strip()
        sort_condition = self.request.GET.get('condition', '')
        sort_order = self.request.GET.get('order', 'asc')

        # Annotate the queryset with total_questions and total_marks
        quizzes = QuizDetails1.objects.filter(creator_id=creater_id).annotate(
            total_questions=Count('quizdetails2'),
            total_marks=Sum('quizdetails2__points'),
        )

        # Apply search filter
        if search_query:
            quizzes = quizzes.filter(title_quiz__icontains=search_query)

        # Apply sorting
        if sort_condition == 'username':
            order_by_field = 'created_by' if sort_order == 'asc' else '-created_by'
        elif sort_condition == 'quesion':  # Sorting by the number of questions
            order_by_field = 'total_questions' if sort_order == 'asc' else '-total_questions'
        elif sort_condition == 'score':  # Sorting by score
            order_by_field = 'total_marks' if sort_order == 'asc' else '-total_marks'
        else:
            order_by_field = 'title_quiz'  # Default sorting by title

        quizzes = quizzes.order_by(order_by_field)

        # Handle pagination
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(quizzes, 12)  # Paginate with 12 items per page
        paginated_quizzes = paginator.get_page(page_number)

        # Add pagination details to context
        context['quizzes'] = paginated_quizzes
        context['creater_id'] = creater_id
        context['name'] = name
        return context

class QuizListView(ListView):
    model = QuizDetails1
    template_name = 'start.html'
    context_object_name = 'quizzes'
    paginate_by = 12  # 12 quizzes per page

    def get_queryset(self):
        # Get the base queryset
        queryset = QuizDetails1.objects.annotate(
            total_questions=Count('quizdetails2'),
            total_marks=Sum('quizdetails2__points')
        )

        # Handle search query
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title_quiz__icontains=search_query)

        # Handle sort condition
        sort_condition = self.request.GET.get('condition', '')
        sort_order = self.request.GET.get('order', 'asc')  # Default to ascending order

        if sort_condition == 'username':
            queryset = queryset.order_by('created_by')
        elif sort_condition == 'quesion':  # Assuming you mean number of questions
            queryset = queryset.order_by('total_questions')
        elif sort_condition == 'score':
            if sort_order == 'desc':
                queryset = queryset.order_by('-total_marks')  # Descending order
            else:
                queryset = queryset.order_by('total_marks')  # Ascending order

        # Debugging: Print the queryset for verification
        print(queryset)  # Ensure the queryset is as expected
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_size = self.paginate_by
        queryset = self.get_queryset()

        # Paginate the queryset
        paginator = self.get_paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)  # Get the paginated page object

        # Add pagination data to the context
        context['quizzes'] = page_obj
        context['current_page'] = page_obj.number
        context['total_pages'] = paginator.num_pages
        context['has_next'] = page_obj.has_next()
        context['has_previous'] = page_obj.has_previous()

        return context


class AttendQuizView(View):
    def get(self, request, quiz_id):
        # Retrieve the quiz and its questions
        quiz = get_object_or_404(QuizDetails1, pk=quiz_id)
        questions = QuizDetails2.objects.filter(quiz=quiz)

        return render(request, 'attend-quiz.html', {
            'quiz': quiz,
            'questions': questions,
            'quiz_id': quiz_id,
        })

    def post(self, request, quiz_id):
        # Retrieve quiz and questions
        quiz = get_object_or_404(QuizDetails1, pk=quiz_id)
        questions = QuizDetails2.objects.filter(quiz=quiz)

        # Extract participant details
        name = request.POST.get('name')
        email = request.POST.get('email')

        total_marks = 0
        question_status = []
        user_exists = False

        # Check if the user already exists in the Response1 table for this quiz
        if Response1.objects.filter(name=name, email=email, quiz=quiz).exists():
            user_exists = True

        # If user doesn't exist, process answers and save to Response1 table
        if not user_exists:
            # Iterate through each question and process the response
            for question in questions:
                question_id = question.question_id
                user_answer = request.POST.get(f'q{question_id}')

                if user_answer:  # Process only if user answered
                    is_correct = question.correct_option == user_answer
                    points = question.points if is_correct else 0
                    total_marks += points

                    # Save to Response1 model
                    try:
                        Response1.objects.create(
                            quiz=quiz,
                            name=name,
                            email=email,
                            question=question,
                            correct_answer=user_answer,
                            points=points,
                        )
                    except Exception as e:
                        print(f"Error saving response: {e}")

                    # Add correctness to each question
                    question.is_correct = is_correct
                else:
                    question.is_correct = None

        # Render the template with relevant context
        return render(request, 'attend-quiz.html', {
            'quiz': quiz,
            'questions': questions,
            'quiz_id': quiz_id,
            'total_marks': total_marks,
            'user_exists': user_exists,  # Pass this flag to the template
        })

class QuizCheckView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, quiz_id):
        # Retrieve the quiz and its questions
        quiz = get_object_or_404(QuizDetails1, pk=quiz_id)
        questions = QuizDetails2.objects.filter(quiz=quiz)

        # Calculate total marks
        total_marks = sum(question.points for question in questions)

        return render(request, 'quiz-check.html', {
            'quiz': quiz,
            'questions': questions,
            'total_marks': total_marks,
        })
    
class ResponseView(TemplateView):
    
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'response.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_id = self.kwargs.get('quiz_id')  # Get quiz_id from URL parameters
        context['quiz_id'] = quiz_id  # Add quiz_id to context
        
        # Fetch the quiz name from QuizDetails1
        quiz = QuizDetails1.objects.filter(quiz_id=quiz_id).first()
        context['quiz_name'] = quiz.title_quiz if quiz else "Quiz not found"

        # Get the search query
        search_query = self.request.GET.get('search', '').strip()

        # Fetch all responses for the specific quiz and filter by search query
        responses = Response1.objects.filter(quiz_id=quiz_id)
        if search_query:
            responses = responses.filter(
                Q(name__icontains=search_query)
            )

        # Annotate the results with total scores and sort them
        responses = responses.values(
            'name', 'email'
        ).annotate(total_score=Sum('points')).order_by('name', 'email')
        
        # Prepare data for the table
        context['responses'] = responses
        return context


class QuestionAnswerView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, quiz_id, name, email):
        # Fetch all responses for the given quiz, name, and email
        responses = Response1.objects.filter(
            quiz_id=quiz_id,
            name=name,
            email=email
        )

        # Calculate total score
        total_score = responses.aggregate(total_score=Sum('points'))['total_score'] or 0

        # Prepare question, user answer, correct answer, and score
        question_data = [
            {
                'question': response.question.question,         # Question text
                'user_answer': response.correct_answer,         # User's provided answer
                'correct_answer': response.question.correct_option,  # Correct answer
                'points': response.points,                      # Points scored
            }
            for response in responses
        ]

        # Render the question-answer.html template
        return render(request, 'question-answer.html', {
            'quiz_id': quiz_id,
            'name': name,
            'email': email,
            'total_score': total_score,   # Total score
            'question_data': question_data,  # Data for each question
        })



class CreateQuizView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'create-quiz.html'
    QuizDetails2FormSet = formset_factory(QuizDetails2Form, extra=1)

    def get(self, request):
        quiz_form = QuizDetails1Form()
        formset = self.QuizDetails2FormSet()
        creator_id = request.GET.get('creator_id')  # Get creator_id from query parameters
        name = request.GET.get('name')  # Get the creator's name

        return render(request, self.template_name, {
            'quiz_form': quiz_form,
            'formset': formset,
            'creator_id': creator_id,
            'name': name  # Pass name to the template
        })

    def post(self, request):
        # Get the form data
        creator_id = request.POST.get('creator_id')
        title_quiz = request.POST.get('title_quiz')
        description_quiz = request.POST.get('description_quiz')
        created_by = request.POST.get('created_by')
        quiz_img = request.FILES.get('quiz_img')

        # Create a new QuizDetails1 instance
        try:
            quiz_detail = QuizDetails1.objects.create(
                creator_id=creator_id,
                title_quiz=title_quiz,
                description_quiz=description_quiz,
                created_by=created_by,
                quiz_img=quiz_img
            )
        except Exception:
            return render(request, self.template_name, {
                'quiz_form': QuizDetails1Form(),
                'formset': self.QuizDetails2FormSet(),
                'creator_id': creator_id,
                'name': request.POST.get('name'),  # Pass name to the template on error
                'error': "Error saving quiz details."
            })

        # Now save questions and options for QuizDetails2
        question_index = 1
        while True:
            question = request.POST.get(f'question_{question_index}')
            if not question:  # If there are no more questions, break the loop
                break
            
            option_1 = request.POST.get(f'option_1_{question_index}')
            option_2 = request.POST.get(f'option_2_{question_index}')
            option_3 = request.POST.get(f'option_3_{question_index}')
            correct_option = request.POST.get(f'correctOption_{question_index}')
            points = request.POST.get(f'score_{question_index}')

            # Create a new QuizDetails2 instance
            try:
                QuizDetails2.objects.create(
                    quiz=quiz_detail,  # Reference to the quiz created
                    question=question,
                    option1=option_1,
                    option2=option_2,
                    option3=option_3,
                    correct_option=correct_option,  # Ensure this matches your logic
                    points=int(points)  # Ensure points are saved as an integer
                )
            except Exception:
                return render(request, self.template_name, {
                    'quiz_form': QuizDetails1Form(),
                    'formset': self.QuizDetails2FormSet(),
                    'creator_id': creator_id,
                    'name': request.POST.get('name'),  # Pass name to the template on error
                    'error': "Error saving quiz questions."
                })

            question_index += 1
        
        return redirect('myquiz')

class AddQuestionView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'add-question.html'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(QuizDetails1, quiz_id=quiz_id)
        return render(request, self.template_name, {
            'quiz_id': quiz_id,
            'quiz': quiz
        })

    def post(self, request, quiz_id):
        quiz = get_object_or_404(QuizDetails1, quiz_id=quiz_id)

        question_index = 1
        errors = []
        while True:
            # Dynamically read question data
            question = request.POST.get(f'question_{question_index}')
            if not question:
                break  # Exit the loop when no more questions are found

            try:
                option_1 = request.POST[f'option_1_{question_index}']
                option_2 = request.POST[f'option_2_{question_index}']
                option_3 = request.POST[f'option_3_{question_index}']
                correct_option = request.POST[f'correctOption_{question_index}']
                points = int(request.POST[f'score_{question_index}'])

                # Save the question to QuizDetails2
                QuizDetails2.objects.create(
                    quiz=quiz,
                    question=question,
                    option1=option_1,
                    option2=option_2,
                    option3=option_3,
                    correct_option=correct_option,
                    points=points
                )
            except (KeyError, ValueError) as e:
                errors.append(f"Error in question {question_index}: {str(e)}")
                break

            question_index += 1

        if errors:
            return render(request, self.template_name, {
                'quiz_id': quiz_id,
                'quiz': quiz,
                'error': " ".join(errors)
            })

        # Redirect back to the quiz-check page after successful submission
        return redirect('quiz-check', quiz_id=quiz_id)


# Initialize logger
logger = logging.getLogger(__name__)

class EditQuestionView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            logger.warning("Unauthorized access attempt. Redirecting to login.")
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, question_id):
        # Fetch the question from QuizDetails2 by question_id
        question = get_object_or_404(QuizDetails2, question_id=question_id)
        return render(request, 'edit-question.html', {'question': question})

    def post(self, request, question_id):
        # Fetch the question from QuizDetails2 by question_id
        question = get_object_or_404(QuizDetails2, question_id=question_id)
        
        # Get updated data from the form
        question_text = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        correct_option = request.POST.get('correct_option_radio')  # This is the value of the selected radio button
        points = request.POST.get('points')

        # Validate and update the question
        try:
            # Update the question attributes with the new values
            question.question = question_text
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.correct_option = correct_option  # Correctly store the selected option value
            question.points = int(points)
            
            # Save the updated question to the database
            question.save()

            # Log success
            logger.info(f"Question {question_id} updated successfully.")

            # Add success message
            messages.success(request, 'Question updated successfully.')
            
            # Redirect to quiz-check with optional parameters if needed
            return redirect('quiz-check', quiz_id=question.quiz_id)  # Replace `quiz_id` with the appropriate field
        except Exception as e:
            # Log error
            logger.error(f"Error updating question {question_id}: {e}")

            # If there's an error, show an error message
            messages.error(request, f'Error updating question: {e}')
            
            # Render the form again with the current data
            return render(request, 'edit-question.html', {'question': question})
    
class EditQuizdetailView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'creater_id' not in request.session:
            return redirect('login')  # Redirect to login if session is not valid
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, quiz_id):
        # Fetch the quiz using quiz_id
        quiz = get_object_or_404(QuizDetails1, pk=quiz_id)
        return render(request, 'edit-quizdetail.html', {'quiz': quiz, 'quiz_id': quiz_id})

    def post(self, request, quiz_id):
        # Fetch the quiz using quiz_id
        quiz = get_object_or_404(QuizDetails1, pk=quiz_id)

        # Get the updated data from the form
        title_quiz = request.POST.get('title_quiz')
        description_quiz = request.POST.get('description_quiz')
        quiz_img = request.FILES.get('quiz_img')  # Check for file upload

        # Update quiz details
        try:
            quiz.title_quiz = title_quiz
            quiz.description_quiz = description_quiz
            if quiz_img:  # Update image only if a new image is provided
                quiz.quiz_img = quiz_img
            quiz.save()  # Save the updated quiz

            messages.success(request, 'Quiz details updated successfully.')
            return redirect('quiz-check', quiz_id=quiz.quiz_id)  # Redirect to quiz-check page
        except Exception as e:
            messages.error(request, f'Error updating quiz: {e}')
            return render(request, 'edit-quizdetail.html', {'quiz': quiz, 'quiz_id': quiz_id, 'error': e})

class ShareView(TemplateView):
    template_name = 'share.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_id'] = kwargs['quiz_id']  # Pass quiz_id to the template
        return context

class DeleteQuizView(View):
    def post(self, request, *args, **kwargs):
        quiz_id = request.POST.get('quiz_id')  # Get quiz_id from the POST data
        try:
            # Delete related quiz questions and responses
            QuizDetails2.objects.filter(quiz_id=quiz_id).delete()
            Response1.objects.filter(quiz_id=quiz_id).delete()
            
            # Delete the quiz itself
            QuizDetails1.objects.filter(quiz_id=quiz_id).delete()

            # Add a success message
            messages.success(request, "Quiz deleted successfully!")
        except QuizDetails1.DoesNotExist:
            # Add an error message if quiz is not found
            messages.error(request, "Quiz not found. Unable to delete.")
        
        # Redirect back to the 'myquiz' page
        return redirect('myquiz')
    
class DeleteQuestionView(View):
    def post(self, request):
        question_id = request.POST.get('question_id')
        
        # Fetch the question object
        question = get_object_or_404(QuizDetails2, question_id=question_id)
        
        # Delete associated responses
        Response1.objects.filter(question=question).delete()
        
        # Delete the question itself
        question.delete()
        
        # Redirect to the quiz-check page after deletion
        return redirect('quiz-check', quiz_id=question.quiz.quiz_id)





