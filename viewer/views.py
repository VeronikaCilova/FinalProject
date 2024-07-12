from concurrent.futures._base import LOGGER
from datetime import date

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm, DateField
from django.shortcuts import render
from django.views import View

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView

from viewer.models import Profile, Goal
import re


def home(request):
    return render(request, 'home.html', {'title': 'Welcome to Personal Portal'})


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'password1', 'password2']

    position = CharField(label='What is your position', widget=Textarea)
    bio = CharField(label='Tell us more about you', widget=Textarea, min_length=40)

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


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')


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
