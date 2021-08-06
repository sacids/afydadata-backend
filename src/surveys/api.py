from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.mixins import CreateModelMixin
from rest_framework import renderers
from rest_framework.parsers import JSONParser

from .serializers import SurveyQuestionsSerializer, SurveySerializer, SurveyResponsesSerializer
from surveys.models import Survey, SurveyQuestions, SurveyResponses
from surveys.utils import * 
from django.template import RequestContext, loader
from django.contrib.auth import login
from src.surveys.utils import do_authenticate, process_odk_submission



class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Survey.objects.all().order_by('-created_on')
    serializer_class = SurveySerializer
    parser_classes = (MultiPartParser, FormParser,)
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, obj):
        cur_obj     = obj.save()
        survey_cfg              = init_xform(cur_obj.xform.name)
        cur_obj.form_id     = survey_cfg['form_id']
        cur_obj.save()
        #print(survey_cfg)
        self.save_survey_qns(cur_obj, survey_cfg['qns'])
    
    def save_survey_qns(self, survey, survey_qns):

        for obj in survey_qns:
            sq  = SurveyQuestions.objects.create(
                survey=survey,
                ref=obj['ref'],
                col_name=obj['col_name'],
                col_type=obj['col_type'],
                created_by=self.request.user)



class SurveyQuestionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SurveyQuestions.objects.all()
    serializer_class = SurveyQuestionsSerializer
    #permission_classes = [permissions.IsAuthenticated]



class SurveyResponsesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SurveyResponses.objects.all()
    serializer_class = SurveyResponsesSerializer
    #permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def form_submission(request):
    
    if request.method == 'HEAD':
        header                    = request.headers
        if 'Authorization' in header:
            response                = OpenRosaResponse(status=204)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        else:
            response                = RequestAuthentication(status=401)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    
    if request.method != 'POST':
        response                    = BadRequest(status=401)
        response['Location']        = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    
    # authenticate
    current_user = do_authenticate(request)

    if not current_user:
        response                = OpenRosaResponse(status=401)
        response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
   
    login(request, current_user)
    
    if 'xml_submission_file' not in request.FILES:
        response                    = BadRequest(status=404)
        response['Location']        = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    
    # process submission

    result  = process_odk_submission(request)

    if result:

        context     = {
            'nature': 'submit_success',
            'message': 'Success',
        }

        response    = render(request,'odk_submission.xml',context, content_type="text/xml; charset=utf-8",status=201)
        response    = attach_openRosaHeader(response)
        response['Location'] = request.build_absolute_uri().replace(request.get_full_path(), '/submission')

        return response
    else:
        resp = BadRequest("Submission Error.")
        resp.status_code = 500
        resp['Location'] = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return resp



@csrf_exempt
def form_list(request):

    if request.method == 'HEAD':
        header                    = request.headers
        if 'Authorization' in header:
            response                = OpenRosaResponse(status=204)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        else:
            response                = RequestAuthentication(status=401)
            response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    
    if request.method != 'GET':
        response                    = BadRequest(status=401)
        response['Location']        = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response
    
    # authenticate
    current_user = do_authenticate(request)

    if not current_user:
        response                = OpenRosaResponse(status=401)
        response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return response

    # check form permissions
    surveys     = Survey.objects.all()
    context     = {
        'surveys': surveys,
    }

    response    = render(request,'odk_xform_list.xml',context, content_type="text/xml; charset=utf-8")
    response    = attach_openRosaHeader(response)
    return response

    # 

def form_get(request, id):

    survey  = get_object_or_404(Survey, pk=id)

    if os.path.exists(survey.xform.path):
        response = HttpResponse(survey.xform.read(), content_type="text/xml; charset=utf-8")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(survey.xform.path)
        return response
    raise Http404


    