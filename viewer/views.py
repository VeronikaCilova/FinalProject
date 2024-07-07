from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from viewer.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView

from viewer.models import Profile


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
        biography = CharField(label='Tell us more about you', widget=Textarea, min_length=40)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        position = self.cleaned_data['position']
        biography = self.cleaned_data['biography']
        profile = Profile(position=position, biography=biography, user=result)
        if commit:
            profile.save()
        return result


def home(request):
    return render(request, 'home.html')

class ProfileView(View):
    def get(self, request, pk):
        if Profile.objects.filter(id=pk).exists():  # otestujeme, zda profil existuje
            result = Profile.objects.get(id=pk)
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