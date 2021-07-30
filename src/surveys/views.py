

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
import os
from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django.views.generic import *


import pyxform
from pyxform import xform2json
import json
from django.urls import reverse
import xml.etree.ElementTree as ET

# Create your views here.

def xform_json(request):

    file_path   = os.path.join(settings.BASE_DIR, 'src/assets/xform/data/Clinicians Form_2021-07-29_15-12-33.xml')
    xf          = readFile(file_path)
    tree        = ET.parse(file_path)
    root        = tree.getroot()

    response    = 0

    tmp         = {}
    for elem in root.iter():
        if elem.tag == 'data':
            #print('id '+str(elem.attrib['id']))
            form_id     = elem.attrib['id']
            tmp['id']   = form_id
        if elem.tag == 'instanceID':
            instance_id = elem.text.strip()
        if elem.text.strip() != '':
            #print(elem.tag+' '+elem.text.strip())
            tmp[elem.tag]   = elem.text.strip()

    json_object = json.dumps(tmp)
    
    s  = Survey.objects.filter(form_id=form_id)[0]
    try:
        sr  = SurveyResponses.objects.create(
                    survey=s,
                    instance_id=instance_id,
                    response=json_object,
                    created_by=request.user)

        response = 1
    except:
        response = 2
        


    return HttpResponse(response)


def init_xform(filename):

    file_path   = os.path.join(settings.BASE_DIR, filename)
    xf          = readFile(file_path)
    contents    = xform2json.XFormToDictBuilder(xf)

    zote        = contents.__dict__
    children    = contents.children
    model       = contents.model["bind"]
    form_id     = contents.model["instance"]["data"]["id"]

    survey_cfg              = {}
    survey_cfg['form_id']   = form_id
    survey_cfg['qns']       = []

    for item in model:
        nodeset     = item['nodeset']
        col_name    = nodeset.rsplit('/', 1)[-1]
        col_type    = item['type']
        relevant    = ''
        if "relevant" in item:
            relevant    = item['relevant']

        qns_dict    = {}
        qns_dict['col_name']    = col_name
        qns_dict['col_type']    = col_type
        qns_dict['relevant']    = relevant
        qns_dict['ref']         = nodeset
        survey_cfg['qns'].append(qns_dict)

    return survey_cfg

def readFile(filename):
    f = open(filename, 'r')
    if f.mode == 'r':
       contents =f.read()
       #print (contents)
    return contents 


class SurveyCreateView(CreateView):
    model = Survey
    template_name = "create.html"
    fields          = ['title','xform','description']

    #def form_valid(self, form):
        #self.object = form.save(commit=False)
        #print(self.object.filename)
        #self.object.save()
        #return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        print(self.object.xform)
        survey_cfg              = init_xform(self.object.xform.name)
        self.object.form_id     = survey_cfg['form_id']
        self.object.save()
        self.save_survey_qns(survey_cfg['qns'])
        return reverse('Survey:show_survey', kwargs={'pk': self.object.id})

    def save_survey_qns(self, survey_qns):
        for obj in survey_qns:
            sq  = SurveyQuestions.objects.create(
                survey=self.object,
                ref=obj['ref'],
                col_name=obj['col_name'],
                col_type=obj['col_type'],
                created_by=self.request.user)
        

class SurveyListView(ListView):
    model = Survey
    template_name = "list.html"

class SurveyDetailView(DetailView):
    model = Survey
    template_name = "detail.html"
