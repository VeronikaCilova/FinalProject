from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from viewer.models import Profile


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
