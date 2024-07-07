from concurrent.futures._base import LOGGER

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm
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


class ProfileView(View):
    def get(self, request, pk):
        if Profile.objects.filter(id=pk).exists():  # otestujeme, zda profil existuje
            result = Profile.objects.get(id=pk)
            return render(request, 'user_page.html', {'title': 'MyProfile', 'profile': result})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')


class GoalView(View):
    def get(self, request, pk):
        if Goal.objects.filter(id=pk).exists():
            result = Goal.objects.get(id=pk)
            return render(request, 'goal.html', {'title': result, 'goal': result})

        result = Goal.objects.all()
        return render(request,
                      'goals.html',
                      {'title': 'Goals', 'goals': result})


class GoalsView(ListView):
    template_name = 'goals.html'
    model = Goal
    context_object_name = 'goals'


class GoalModelForm(ModelForm):

    class Meta:
        model = Goal
        fields = '__all__'

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


class GoalFormView(FormView):
    template_name = 'form.html'
    form_class = GoalModelForm
    success_url = reverse_lazy('goal_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Goal.objects.create(name=cleaned_data['name'])
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class GoalCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GoalModelForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.add_goal'


class GoalUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Goal
    form_class = GoalModelForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.change_goal'


class GoalDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'goal_confirm_delete.html'
    model = Goal
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.delete_goal'
