from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bill.models import Reciept, Item, Person


class RecieptListView(View):
    template_name = 'bill/all_reciepts.html'
    def get(self, request):
        rl = Reciept.objects.all()
        ctx = {'reciept_list': rl}
        return render(request, self.template_name, ctx)

class BillCreateView(View):
    template_name = 'bill/calc.html'
    
