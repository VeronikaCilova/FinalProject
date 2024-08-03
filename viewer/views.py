from concurrent.futures._base import LOGGER
from datetime import date

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import CharField, Textarea, forms, ModelForm, ModelChoiceField, DateField
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView


from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView

from viewer.models import Profile, Feedback, Position
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, Profile
from viewer.models import Profile, Goal
import re

from django.shortcuts import render, redirect
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import Todo

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.conf import settings



def home(request):
    return render(request, 'home.html', {'title': 'Welcome to Personal Portal'})


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username','first_name', 'last_name', 'password1', 'password2']

    #position = CharField(label='What is your position', widget=Textarea)
    position = ModelChoiceField(queryset=Position.objects.all())
    bio = CharField(label='Tell us more about you', widget=Textarea, min_length=5)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        position = self.cleaned_data['position']
        bio = self.cleaned_data['bio']
        profile = Profile(position=position, bio=bio, user=result)
        if commit:
            profile.save()
        return result


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if Profile.objects.filter(id=pk).exists():
            result = Profile.objects.get(id=pk)
            return render(request, 'user_page.html', {'title': 'MyProfile', 'profile': result})

    # TODO: vypsat chybovou hlášku
        return render(request,
                      'user_page.html',
                      {'title': 'Profile', 'profile': Profile.objects.all()})

class MyProfileView(View):
    def get(self, request):
        user=request.user
        if Profile.objects.filter(user=user).exists():  # otestujeme, zda profil existuje
            result = Profile.objects.get(user=user)
            return render(request, 'user_page.html', {'title': 'MyProfile', 'profile': result})


        return render(request, 'home.html')


# class ProfileView(DetailView):
#     model = Profile
#     template_name = 'user_page.html'
    # context_object_name = 'profile'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')


@login_required
def send_kudos(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.evaluator = Profile.objects.get(user=request.user)
            feedback.save()
            return redirect('user_page', pk=feedback.subject_of_review.pk)
    else:
        form = FeedbackForm()

    return render(request, 'send_kudos.html', {'form': form})


@login_required
def user_page(request, pk):
    profile = Profile.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(subject_of_review=profile).order_by('-creation_date')
    return render(request, 'user_page.html', {'profile': profile, 'feedbacks': feedbacks})


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['description', 'subject_of_review']
        labels = {
            'description': 'Type your kudos here',
            'subject_of_review': 'Select your colleague here',
        }
        widgets = {
            'description': Textarea(attrs={'rows': 4}),
        }


class FutureDateField(DateField):
    def validate(self, value):
        super().validate(value)
        if value < date.today():
            raise ValidationError('Only future dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return result


class GoalView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if Goal.objects.filter(id=pk).exists():
            result = Goal.objects.get(id=pk)
            return render(request, 'goal.html', {'title': 'MyGoal', 'goal': result})

        result = Goal.objects.all()
        return render(request,
                      'goals.html',
                      {'title': 'Goals', 'goals': result})


class GoalsView(LoginRequiredMixin, ListView):
    template_name = 'goals.html'
    model = Goal
    context_object_name = 'goals'


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'
        #exclude = ['profile']

    deadline = FutureDateField()

    def clean_name(self):
        initial_data = super().clean()
        initial = initial_data['name'].strip()
        return initial.capitalize()

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        return result


class GoalCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GoalForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.add_goal'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Goal
    form_class = GoalForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.change_goal'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'goal_confirm_delete.html'
    model = Goal
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.delete_goal'



class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
        #exclude = ["profile"]



@login_required
def productivity(request):
    profile = Profile.objects.get(user=request.user)
    item_list = Todo.objects.filter(profile=profile).order_by("-date")
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo')
    form = TodoForm()

    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, 'productivity.html', page)


@login_required
def edit(request, item_id):
    item = Todo.objects.get(id=item_id)
    if request.method == "POST":
        form = TodoForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item was updated successfully.")
            return redirect('todo')
    else:
        form = TodoForm(instance=item)

    page = {
        "forms": form,
        "title": "Edit Item",
        "item": "TODO LIST",
    }
    return render(request, 'edit_todo.html', page)

@login_required
def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item was removed !!!")
    return redirect('todo')




@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '')


            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)


            openai.api_key = settings.OPENAI_API_KEY
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_message,
                max_tokens=150
            )


            return JsonResponse({'response': response.choices[0].text.strip()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)