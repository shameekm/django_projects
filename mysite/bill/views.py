from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse, reverse_lazy

from django.db.models import Q

from bill.forms import PersonForm, ItemForm
from bill.models import Reciept, Item, Person, Split


class RecieptListView(ListView):
    model = Reciept
    template_name = 'bill/all_reciepts.html'
    def get(self, request):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(store_name__icontains=strval)
            #query.add(Q(text__icontains=strval), Q.OR)
            reciept_list = Reciept.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            reciept_list = Reciept.objects.all().order_by('-updated_at')[:10]
        ctx = {'reciept_list': reciept_list, 'search': strval}
        return render(request, self.template_name, ctx)

class RecieptCreateView(CreateView):
    model = Reciept
    template_name = 'bill/reciept_form.html'
    fields = ['store_name', 'tax', 'tip', 'total_before_tax']
    success_url = reverse_lazy('bill:all')

class RecieptUpdateView(UpdateView):
    model = Reciept
    template_name = 'bill/reciept_form.html'
    fields = ['store_name', 'tax', 'tip', 'total_before_tax']
    success_url = reverse_lazy('bill:all')

class RecieptDeleteView(DeleteView):
    model = Reciept
    template_name = 'bill/reciept_delete.html'
    success_url = reverse_lazy('bill:all')

class RecieptDetailView(DetailView):
    model = Reciept
    template_name = 'bill/reciept_detail.html'  

    def get(self, request, pk):
        reciept = Reciept.objects.get(id=pk)
        persons_list = Person.objects.filter(reciept=reciept)
        id_item_person_list = dict()

        for person in persons_list:
            item_list = Item.objects.filter(persons=person.id)
            person.save()
            for item in item_list:
                if item.id not in id_item_person_list.keys():
                    #print(item.id, item.name)
                    id_item_person_list[item.id] = [item.name, item.price]
                    persons = item.persons.values_list('name', flat = True)
                    for person in persons:
                        id_item_person_list[item.id].append(person)

        print(id_item_person_list)
        person_form = PersonForm()
        item_form = ItemForm()


        context = { 'reciept' : reciept, 'persons' : persons_list, 'person_form' : person_form, 'reciept_items' : id_item_person_list, 'item_form' : item_form}
        return render(request, self.template_name, context)

class PersonCreateView(View):
    def post(self, request, pk):
        reciept_id = get_object_or_404(Reciept, id=pk)
        person = Person(name=request.POST['add_a_person'], reciept=reciept_id)
        person.save()
        return redirect(reverse('bill:reciept_detail', args=[pk]))

class PersonDeleteView(DeleteView):
    model = Person
    template_name = "bill/person_delete.html"

    def get_success_url(self):
        reciept = self.object.reciept
        return reverse('bill:reciept_detail', args=[reciept.id])

class ItemCreateView(View):
    def post(self, request, pk):
        reciept_id = get_object_or_404(Reciept, id=pk)
        current_item = Item(name=request.POST['item_name'], price=request.POST['item_price'])
        current_item.save()
        for person_id in request.POST.getlist('person'):
            person_instance = Person.objects.get(pk=person_id)
            Split(item = current_item, person = person_instance).save()
        return redirect(reverse('bill:reciept_detail', args=[pk]))

class ItemDeleteView(DeleteView):
    model = Item
    template_name = "bill/item_delete.html"

    def get_reciept(self):
        person_id = self.object.persons.values_list('id', flat = True)[0]
        person = Person.objects.get(pk=person_id)
        return person.reciept.id

    def get_success_url(self):
        reciept_id = self.get_reciept()
        return reverse('bill:reciept_detail', args=[reciept_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reciept'] = self.get_reciept()
        return context
    
    