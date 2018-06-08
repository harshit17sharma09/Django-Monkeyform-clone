# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
import json
from django import forms
from django.views.generic import FormView
from django.views.generic import ListView

from main.models import FormSchema



class CustomFormView(FormView):
    template_name = "custom_form.html"

    def get_form(self):
        form_structure = FormSchema.objects.get(pk=1).schema 
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

class HomePageView(ListView):
    model = FormSchema
    template_name = "home.html"
