

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
import os
from surveys.models import Survey, SurveyQuestions, SurveyResponses
from django.views.generic import *
import random


import pyxform
from pyxform import xform2json
import json
from django.urls import reverse
import xml.etree.ElementTree as ET

# Create your views here.
def xform_json1(request):

    sr      = SurveyResponses.objects.filter(response__village='Test')
    print(sr)
    d  = random.randint(10,50)
    s  = Survey.objects.get(pk=18)
    sr  = SurveyResponses.objects.create(
                    survey=s,
                    instance_id=d,
                    response={'name':'eric','age':d,'sex':'Male'},
                    created_by=request.user)

    return HttpResponse(1)


def xform_json1(request):

    file_path   = os.path.join(settings.BASE_DIR, 'src/media/xform/data/Dalili_za_Binadamudemo_BjRiogz.xml')
    xf          = readFile(file_path)
    tree        = ET.parse(file_path)
    root        = tree.getroot()

    response    = 0
    d  = random.randint(1,500)

    tmp         = {}
    for elem in root.iter():
        if elem.tag == 'data':
            #print('id '+str(elem.attrib['id']))
            form_id     = elem.attrib['id']
            tmp['id']   = form_id+str(d)
        if elem.tag == 'instanceID':
            instance_id = elem.text.strip()+str(d)
        if elem.text.strip() != '':
            #print(elem.tag+' '+elem.text.strip())
            tmp[elem.tag]   = elem.text.strip()

    #json_object = json.dumps(tmp)
    json_object = tmp
    print(tmp)
    
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

def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iter())}
    d.update(('@' + k, v) for k, v in t.attrib.items())
    d['mtext'] = t.text
    return d

def init_xform(filename):

    filename    = os.path.join(settings.MEDIA_ROOT, 'xform/defn/Dalili_za_Binadamudemo_3SjQ12t.xml')
    file_path   = os.path.join(settings.BASE_DIR, filename)
    xf          = readFile(file_path)


    contents    = xform2json.XFormToDictBuilder(xf)

    zote        = contents.__dict__
    ref_order   = contents.ordered_binding_refs
    group       = contents.body['group']

    pages       = {}
    page_num    = 1
    for x in group:
        r           = x['ref']
        pages[r]    = page_num
        page_num    = page_num + 1

    #zote        = contents.translations[1]['text']
    trans       = contents.translations
    
    holder      = {}

    #return HttpResponse(zote,content_type="application/json")
    #return HttpResponse(json.dumps(zote, sort_keys=True, indent=4), content_type="application/json")

    for itext in trans:
        lang    = itext['lang']
        text    = itext['text']
        for item in text:
        #for item in vitem:
            tmp     = item['id'].split(":")
            ref     = tmp[0]
            anchor  = tmp[1]

            if ref not in holder:
                holder[ref] = {
                    'option'    :{},
                    'label'     :{},
                    'hint'      :{},
                }
            
            if anchor[0:6] == 'option':
                if lang not in holder[ref]['option']:
                    holder[ref]['option'][lang] = []
                holder[ref]['option'][lang].append(item['value'])
            else:
                if lang not in holder[ref][anchor]:
                    holder[ref][anchor][lang] = ''
                holder[ref][anchor][lang] = item['value']

        #print(item['value'])

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
        required    = False
        page        = 0
        order       = 0

        for p in pages:
            if nodeset.find(p) > -1:
                page    = pages[p]

        if "relevant" in item:
            relevant    = item['relevant']
        if "required" in item:
            required    = item['required']
        if nodeset in ref_order:
            order = ref_order.index(nodeset) + 1
            print(nodeset,' - ',order)

        
        qns_dict    = {}
        qns_dict['col_name']    = col_name
        qns_dict['col_type']    = col_type
        qns_dict['relevant']    = relevant
        qns_dict['required']    = required
        qns_dict['ref']         = nodeset
        qns_dict['page']        = page
        qns_dict['order']       = order

        if nodeset in holder:
            qns_dict['hint']        = holder[nodeset]['hint']
            qns_dict['options']     = holder[nodeset]['option']
            qns_dict['label']       = holder[nodeset]['label']
        else:
            qns_dict['hint']        = ''
            qns_dict['options']     = ''
            qns_dict['label']       = ''

        survey_cfg['qns'].append(qns_dict)

    #print(survey_cfg)
    return HttpResponse(json.dumps(survey_cfg, sort_keys=True, indent=4), content_type="application/json")
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

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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
                constraints=obj['relevant'],
                hint=obj['hint'],
                options=obj['options'],
                label=obj['label'])
        

class SurveyListView(ListView):
    model = Survey
    template_name = "list.html"

class SurveyDetailView(DetailView):
    model = Survey
    template_name = "detail.html"
