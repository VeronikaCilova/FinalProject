from concurrent.futures._base import LOGGER
from datetime import date
from itertools import chain
from operator import attrgetter

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import CharField, Textarea, forms, ModelForm, ModelChoiceField, DateField
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView


from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView

from viewer.models import Profile, Feedback, Position, Review
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, Profile
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
        fields = ['username','first_name', 'last_name', 'password1', 'password2']

    #position = CharField(label='What is your position', widget=Textarea)
    position = ModelChoiceField(queryset=Position.objects.all())
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

class MyProfileView(View):
    def get(self, request):
        user=request.user
        if Profile.objects.filter(user=user).exists():  # otestujeme, zda profil existuje
            result = Profile.objects.get(user=user)
            return render(request, 'user_page.html', {'title': 'MyProfile', 'profile': result})

        # TODO: home.html
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
    user = request.user
    profile = Profile.objects.get(user=user)
    feedbacks = Feedback.objects.filter(subject_of_review=profile).order_by('-creation_date')
    return render(request, 'user_page.html', {'profile': profile, 'feedbacks': feedbacks})


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['description', 'subject_of_review']
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


class GoalsView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        mygoals = Goal.objects.filter(profile=profile).order_by('-deadline')
        mysubordinate = profile.subordinate.all()
        context = {'goals': mygoals, 'subordinates': mysubordinate}
        return render(request, 'goals.html', context)


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


class GoalCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GoalForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.add_goal'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class GoalUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Goal
    form_class = GoalForm
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.change_goal'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class GoalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'goal_confirm_delete.html'
    model = Goal
    success_url = reverse_lazy('goals')
    permission_required = 'viewer.delete_goal'


class ReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if Review.objects.filter(id=pk).exists():
            result = Review.objects.get(id=pk)
            return render(request, 'review.html', {'title': 'MyReview', 'review': result})

        result = Review.objects.all()
        return render(request,
                      'reviews.html',
                      {'title': 'Reviews', 'reviews': result})


class ReviewsView(LoginRequiredMixin, ListView):
    template_name = 'reviews.html'
    model = Review
    context_object_name = 'reviews'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
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


class ReviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('reviews')
    permission_required = 'viewer.add_review'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('reviews')
    permission_required = 'viewer.change_review'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid()


class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'review_confirm_delete.html'
    model = Review
    success_url = reverse_lazy('reviews')
    permission_required = 'viewer.delete_review'
