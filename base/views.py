from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from .models import Member
from .forms import PositionForm
from django.views import View
from django.db import transaction
from .models import MemberForm

class MemberList(ListView):
    model = Member
    context_object_name = 'members'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['members'].filter(b="0000000").count()

       
        return context

class MemberDetail(DetailView):
    model = Member
    context_object_name = 'member'
    template_name = 'base/member.html'

class MemberCreate(CreateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy('members')
    template_name = 'base/member_form.html'


    def form_valid(self, form):
        return super().form_valid(form)

class MemberEdit(UpdateView):
    template_name = 'base/member_edit.html'
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy('members')

class DeleteView(DeleteView):
    model = Member
    context_object_name = 'member'
    success_url = reverse_lazy('members')
    def get_queryset(self):
        return self.model.objects.filter(b="0000000")



