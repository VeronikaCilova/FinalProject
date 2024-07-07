from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import CharField, Textarea, forms, ModelForm, ModelChoiceField
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView


from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView

from viewer.models import Profile, Feedback, Position
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, Profile


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
        profile = Profile(position=position, bio=bio, user= result)
        if commit:
            profile.save()
        return result


class ProfileView(View):
    def get(self, request, pk):
        if Profile.objects.filter(id=pk).exists():  # otestujeme, zda profil existuje
            result = Profile.objects.get(id=pk)
            return render(request, 'user_page.html', {'title': 'MyProfile', 'profile': result})

        # TODO: home.html
        return render(request, 'home.html')

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
    profile = Profile.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(subject_of_review=profile).order_by('-creation_date')
    return render(request, 'user_page.html', {'profile': profile, 'feedbacks': feedbacks})


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['description', 'subject_of_review']
        widgets = {
            'description': Textarea(attrs={'rows': 4}),
        }