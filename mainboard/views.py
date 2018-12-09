# django library
from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'mainboard/index.html',)


class MedicalsPresenceView(View):

    def get(self, request):
        return render(request, 'registration/medical_presence_view.html')
