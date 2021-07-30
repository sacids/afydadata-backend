
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
import os
import pyxform
from pyxform import xform2json
import json
from django.urls import reverse



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
