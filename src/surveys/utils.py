
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.conf import settings
import urllib.parse



import os
import pyxform
from pyxform import xform2json
import json
from django.urls import reverse
from surveys.models import Survey, SurveyQuestions, SurveyResponses
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
from django.contrib.auth.models import User
from hashlib import md5
import hashlib











OPEN_ROSA_VERSION_HEADER = 'X-OpenRosa-Version'
HTTP_OPEN_ROSA_VERSION_HEADER = 'HTTP_X_OPENROSA_VERSION'
OPEN_ROSA_VERSION = '1.0'
DEFAULT_CONTENT_TYPE = 'text/xml; charset=utf-8'
DEFAULT_CONTENT_LENGTH = settings.DEFAULT_CONTENT_LENGTH

nonce                   = hashlib.md5(get_random_string(length=32).encode()).hexdigest()
DIGEST_AUTHENTICATION   = 'Digest realm="'+settings.DIGEST_REALM+'",qop="auth",nonce="'+nonce+'",opaque="'+nonce+'"'










def init_xform(filename, filetype="xform"):

    file_path   = os.path.join(settings.MEDIA_ROOT, filename)
    xf          = readFile(file_path)
    contents    = xform2json.XFormToDictBuilder(xf)
    trans       = contents.translations
    group       = contents.body['group']
    ref_order   = contents.ordered_binding_refs
    
    holder      = {}
    pages       = {}
    page_num    = 1

    #for x in group:
        #r           = x['ref']
        #pages[r]    = page_num
        #page_num    = page_num + 1

    for itext in trans:
        lang    = itext['lang']
        text    = itext['text']
    
    
        for item in text:
            tmp     = item['id'].split(":")
            ref     = tmp[0]
            anchor  = tmp[1]

            if ref not in holder:
                holder[ref] = {
                    'option'        :{},
                    'label'         :{},
                    'hint'          :{},
                    'requiredMsg'   :{},
                    'constraintMsg' :{},
                }
            
            if anchor[0:6] == 'option':
                if lang not in holder[ref]['option']:
                    holder[ref]['option'][lang] = []
                holder[ref]['option'][lang].append(item['value'])
            else:
                if lang not in holder[ref][anchor]:
                    holder[ref][anchor][lang] = ''
                holder[ref][anchor][lang] = item['value']

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
        required    = 0
        page        = 0
        order       = 0

        for p in pages:
            if nodeset.find(p) > -1:
                page    = int(pages[p])


        if "relevant" in item:
            relevant    = item['relevant']

        if "required" in item:
            if item['required'] == 'true()':
                required = 1
        if nodeset in ref_order:
            order = ref_order.index(nodeset) + 1

        qns_dict    = {}
        qns_dict['col_name']    = col_name
        qns_dict['col_type']    = col_type
        qns_dict['relevant']    = relevant
        qns_dict['required']    = required
        qns_dict['ref']         = nodeset
        qns_dict['page']        = page
        qns_dict['order']       = order

        if nodeset in holder:
            qns_dict['hint']            = holder[nodeset]['hint']
            qns_dict['options']         = holder[nodeset]['option']
            qns_dict['label']           = holder[nodeset]['label']
            qns_dict['requiredMsg']     = holder[nodeset]['requiredMsg']
            qns_dict['constraintMsg']   = holder[nodeset]['constraintMsg']
        else:
            qns_dict['hint']            = ''
            qns_dict['options']         = ''
            qns_dict['label']           = ''
            qns_dict['requiredMsg']     = ''
            qns_dict['constraintMsg']   = ''

        survey_cfg['qns'].append(qns_dict)

    return survey_cfg


def readFile(filename):
    f = open(filename, 'r')
    if f.mode == 'r':
       contents =f.read()
       #print (contents)
    return contents 



def process_odk_submission(request):

    xml     = request.FILES['xml_submission_file']
    xf_dict = get_xf_dict(xml.file.read())

    # check if form is available
    s  = Survey.objects.filter(form_id=xf_dict['id'])
    if s.count() == 0:
        # survey not found
        #print('survey not found')
        return False
    
    # check if user has permission to submit


    # copy files and images
    if not copy_response_files(request):
        return False

    # insert survey response
    try:
        sr  = SurveyResponses.objects.create(
                    survey=s[0],
                    instance_id=xf_dict['instanceID'],
                    response=xf_dict,
                    created_by=request.user)
        return 1
    except Exception as e:
        #print(type(e))
        return False
    


def copy_response_files(request):

    dest_folder     = 'media/xform/data/'
    xml             = request.FILES['xml_submission_file']

    try:
        destination = open(dest_folder+xml.name, 'wb+')
        for chunk in xml.chunks():
            destination.write(chunk)
        destination.close()

        media_files = request.FILES.values()
        for m in media_files:
            destination = open(dest_folder+'/'+m.name, 'wb+')
            for chunk in m.chunks():
                destination.write(chunk)
            destination.close()
        
        return True
    except:
        return False




def get_xf_dict(xf):
    tree    = ET.ElementTree(ET.fromstring(xf))
    root    = tree.getroot()

    tmp         = {}
    for elem in root.iter():
        #print(elem)
        if elem.tag == 'data':
            #print('id '+str(elem.attrib['id']))
            tmp['id']   = elem.attrib['id']
        elif elem.text != None and elem.text.strip() != '':
            #print(elem.tag+' '+elem.text.strip())
            tmp[elem.tag]   = elem.text.strip()
    
    return tmp


def submitXForm(request,filename):

    file_path   = os.path.join(settings.BASE_DIR, 'media/xform/data/'+filename)
    xf          = readFile(file_path)
    tree        = ET.parse(file_path)
    root        = tree.getroot()

    response    = 0

    tmp         = {}
    for elem in root.iter():
        #print(elem)
        if elem.tag == 'data':
            #print('id '+str(elem.attrib['id']))
            form_id     = elem.attrib['id']
            tmp['id']   = form_id
        elif elem.tag == 'instanceID':
            instance_id = elem.text.strip()
        elif elem.text != None and elem.text.strip() != '':
            #print(elem.tag+' '+elem.text.strip())
            tmp[elem.tag]   = elem.text.strip()
    
    # check if survey is available
    s  = Survey.objects.filter(form_id=form_id)[0]

    
    u = User.objects.get(pk=1)
    try:
        sr  = SurveyResponses.objects.create(
                    survey=s,
                    instance_id=instance_id,
                    response=tmp,
                    created_by=u)
    except:
        sr  = False
    return sr




















class BaseOpenRosaResponse(HttpResponse):
    status_code = 201

    def __init__(self, *args, **kwargs):
        super(BaseOpenRosaResponse, self).__init__(*args, **kwargs)

       # self[OPEN_ROSA_VERSION_HEADER] = OPEN_ROSA_VERSION
        tz = pytz.timezone(settings.TIME_ZONE)
        dt = datetime.now(tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
        self['Date'] = dt
        self['X-OpenRosa-Version'] = "1.0"
        self['X-OpenRosa-Accept-Content-Length'] = ""
        


class OpenRosaResponse(BaseOpenRosaResponse):
    status_code = 201

    def __init__(self, *args, **kwargs):
        super(OpenRosaResponse, self).__init__(*args, **kwargs)
        # wrap content around xml
        self.content = '<?xml version="1.0" encoding="UTF-8" ?><OpenRosaResponse xmlns="http://openrosa.org/http/response"><message>Success</message></OpenRosaResponse>'



class OpenRosaResponseSuccess(BaseOpenRosaResponse):
    status_code = 201

    def __init__(self, *args, **kwargs):
        super(OpenRosaResponseSuccess, self).__init__(*args, **kwargs)
        # wrap content around xml
        #self.content = '<?xml version="1.0" encoding="UTF-8" ?><OpenRosaResponse xmlns="http://openrosa.org/http/response"><message nature="submit_success">Success</message></OpenRosaResponse>'
        self.content = '<OpenRosaResponse xmlns="http://openrosa.org/http/response"><message nature="submit_success">Success</message></OpenRosaResponse>'


class OpenRosaResponseNotFound(OpenRosaResponse):
    status_code = 404


class BadRequest(OpenRosaResponse):
    status_code = 400


class OpenRosaResponseNotAllowed(OpenRosaResponse):
    status_code = 405

class RequestAuthentication(BaseOpenRosaResponse):
    status_code = 401
    
    def __init__(self, *args, **kwargs):
        super(RequestAuthentication, self).__init__(*args, **kwargs)
        self['WWW-Authenticate']    = DIGEST_AUTHENTICATION


def OpenRosaSuccessResponse(message):
    return '<OpenRosaResponse xmlns="http://openrosa.org/http/response"><message nature="submit_success">Success</message></OpenRosaResponse>'




def handle_response_files(xml, media_files):

    dest_folder     = 'media/xform/data/'
    for f in xml:
        destination = open(dest_folder+f.name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

    for m in media_files:
        destination = open(dest_folder+'/'+m.name, 'wb+')
        for chunk in m.chunks():
            destination.write(chunk)
        destination.close()

    return 1



def calculate_digest(username,password):
    #print(password)
    tmp         = username+":"+settings.DIGEST_REALM+":"+password
    digest      = hashlib.md5(tmp.encode()).hexdigest()
    return digest

def do_authenticate(request):

    header       = request.headers
    if 'Authorization' in header:
        authorization = header['Authorization']
    else:
        return False

    tmp1    = authorization[7:].replace(', ',"&").replace('"','')
    parts   = dict(urllib.parse.parse_qsl(tmp1))
    
    print(parts)
    
    try:
        u   = User.objects.get(username=parts['username'])
    except User.DoesNotExist:
        return False

    A1      = u.profile.digest
    tmp     = request.method+":"+(parts['uri'].replace(':','%3A'))
    A2      = hashlib.md5(tmp.encode()).hexdigest()
    A3      = hashlib.md5((A1+":"+parts['nonce']+":"+parts['nc']+":"+parts['cnonce']+":"+parts['qop']+":"+A2).encode()).hexdigest()

    if A3   == parts['response']:
        print('authentication success')
        return u
    else:
        return False


def digest_authenticate(request):
    if request.method == 'HEAD':
        header                    = request.headers
        if 'Authorization' in header:
            # Authenticate
            current_user = do_authenticate(header['Authorization'])
            if current_user:
                response                = OpenRosaResponse(status=204)
            else: 
                response                = OpenRosaResponse(status=401)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        else:
            response                = RequestAuthentication(status=401)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    else:
        return False





def attach_openRosaHeader(response):

    response[OPEN_ROSA_VERSION_HEADER] = OPEN_ROSA_VERSION
    tz = pytz.timezone(settings.TIME_ZONE)
    dt = datetime.now(tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
    #dt = datetime.now(tz=ZoneInfo('UTC')).strftime('%a, %d %b %Y %H:%M:%S %Z')
    response['Date'] = dt
    response['X-OpenRosa-Accept-Content-Length'] = DEFAULT_CONTENT_LENGTH
    response['Content-Type'] = DEFAULT_CONTENT_TYPE
        
        
    return response
