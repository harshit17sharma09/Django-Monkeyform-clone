# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
import json
from django import forms
from django.views.generic import FormView
from django.views.generic import ListView

from main.models import FormSchema
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView

from main.forms import NewDynamicFormForm



class CustomFormView(FormView):
    template_name = "custom_form.html"

    def get_form(self):
        form_structure = FormSchema.objects.get(pk=self.kwargs["form_pk"]).schema
        # form_structure = FormSchema.objects.get(pk=1).schema 
        # form_structure_json = """{
        #     "name" : "string"   ,
        #     "age"   : "number"  ,
        #     "city"  : "string"  ,
        #     "country" : "string" ,
        #     "time_lived_in_current_city": "string" 

        # }"""

        # form_structure = json.loads(form_structure_json)

        custom_form = forms.Form(**self.get_form_kwargs())
        for key, value in form_structure.items():
            field_class = self.get_field_class_from_type(value)
            if field_class is not None:
                custom_form.fields[key] = field_class()
            else:
                raise TypeError("Invalid field type {}".format(value)) 
        return custom_form   

    def get_field_class_from_type(self,value_type):
        if value_type == "string":
            return forms.CharField
        elif value_type == "number":
            return forms.IntegerField
        else:
            return None

    def form_valid(self,form):
        custom_form = FormSchema.objects.get(pk=self.kwargs["form_pk"])
        user_response = form.cleaned_data

        form_response = FormResponse(form=custom_form,response=user_response)
        form_response.save()

        return HttpResponseRedirect(reverse('home'))

class HomePageView(ListView):
    model = FormSchema
    template_name = "home.html"


class FormResponseListView(TemplateView):
    template_name = "form_responses.html"

    def get_context_data(self,**kwargs):
        ctx = super(FormResponseListView,self).get_context_data(**kwargs)
        # ctx["form"] =self.get_form()
        form = self.get_form()
        schema = form.schema
        form_fields = schema.keys()
        ctx["headers"] = form_fields
        cts["form"] = form

        responses = self.get_queryset()
        responses_list = list()
        for response in responses:
            response_values = list()
            response.data = response.response

            for field_name in form_fields:
                if field_name in response_data:
                    response_values.append(response_data[field_name])
                else:
                    response_values.append('')
            responses_list.append(response_values)

        ctx["object_list"] = responses_list
        


        return ctx

    def get_queryset(self):
        form = self.get_form()
        return FormResponse.objects.filter(form=form)

    def get_form(self):
        return FormSchema.objects.get(pk=self.kwargs["form_pk"])


class CreateEditFormView(FormView):
    form_class = NewDynamicFormForm
    template_name = "create_edit_form.html"

    def get_initial(self):
        if "form_pk" in self.kwargs:
            form = FormSchema.objects.get(pk=self.kwargs["form_pk"])
            initial = {
                "form_pk": form.pk,
                "title": form.title,
                "schema": json.dumps(form.schema)
            }
        else:
            initial = {}

        return initial

    def get_context_data(self, **kwargs):
        ctx = super(CreateEditFormView, self).get_context_data(**kwargs)
        if "form_pk" in self.kwargs:
            ctx["form_pk"] = self.kwargs["form_pk"]

        return ctx

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        if cleaned_data.get("form_pk"):
            old_form = FormSchema.objects.get(pk=cleaned_data["form_pk"])
            old_form.title = cleaned_data["title"]
            old_form.schema = cleaned_data["schema"]
            old_form.save()
        else:
            new_form = FormSchema(title=cleaned_data["title"], schema=cleaned_data["schema"])
            new_form.save()

        return HttpResponseRedirect(reverse("home"))