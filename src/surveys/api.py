from django.http import Http404, HttpResponse, JsonResponse


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt



from django.shortcuts import redirect, get_object_or_404, render

from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.mixins import CreateModelMixin
from rest_framework import renderers
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SurveyQuestionsSerializer, SurveySerializer, SurveyResponsesSerializer, SurveyFilterSerializer
from surveys.models import Survey, SurveyQuestions, SurveyResponses, SurveyFilter, notes
from surveys.utils import * 
from django.template import RequestContext, loader
from django.contrib.auth import login
from src.surveys.utils import do_authenticate, process_odk_submission

from django.utils.decorators import decorator_from_middleware
from django.conf import settings
from django.middleware.common import CommonMiddleware


from django.db.models import Q



class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Survey.objects.all().order_by('-created_on')
    serializer_class = SurveySerializer
    parser_classes = (MultiPartParser, FormParser,)
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, obj):
        cur_obj             = obj.save()
        survey_cfg          = init_xform(cur_obj.xform.name)
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
                constraints=obj['relevant'],
                required=obj['required'],
                hint=obj['hint'],
                options=obj['options'],
                requiredMsg=obj['requiredMsg'],
                constraintMsg=obj['constraintMsg'],
                page=obj['page'],
                order=obj['order'],
                label=obj['label'])



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


class SurveyFilterViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SurveyFilter.objects.all()
    serializer_class = SurveyFilterSerializer
    #permission_classes = [permissions.IsAuthenticated]

'''
@modify_settings(MIDDLEWARE={
            'remove': 'corsheaders.middleware.CorsMiddleware',
            'remove': 'django.middleware.common.CommonMiddleware',
            'remove': 'django.middleware.csrf.CsrfViewMiddleware',
            'remove': 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        })

'''

@csrf_exempt
@xframe_options_exempt
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
        response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        
        return response      
    
    else:
        resp = BadRequest("Submission Error.")
        resp.status_code = 500
        resp['Location'] = request.build_absolute_uri().replace(request.get_full_path(), '/submission')
        return resp



@csrf_exempt
def form_list(request):

    
    if 'Authorization' in request.headers:
        # authenticate
        current_user = do_authenticate(request)
    else:
        response                = RequestAuthentication(status=401)
        response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/formList')
        return response

    if not current_user:
        response                = OpenRosaResponse(status=401)
        response['Location']    = request.build_absolute_uri().replace(request.get_full_path(), '/formList')
        return response

    # check form permissions
    #surveys     = Survey.objects.all()
    
    surveys     = Survey.objects.filter(user_access__user__member=current_user)
    #print(surveys)
    #print(current_user)
    context     = {
        'surveys': surveys,
    }

    response    = render(request,'odk_xform_list.xml',context, content_type="text/xml; charset=utf-8")
    response    = attach_openRosaHeader(response)
    return response

    # 

def form_get(request, id):

    survey  = get_object_or_404(Survey, pk=id)

    print(survey)
    
    if os.path.exists(survey.xform.path):
        response = HttpResponse(survey.xform.read(), content_type="text/xml; charset=utf-8")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(survey.xform.path)
        return response
    raise Http404


    






class SurveyList(generics.ListAPIView):
    serializer_class = SurveySerializer

    def get_queryset(self):
        """
        This view should return a list of all the surveys for
        the project as determined by the project_id portion of the URL.
        """
        project_id = self.kwargs['project_id']
        return Survey.objects.filter(project_id=project_id)




class SurveyResponseList(generics.ListAPIView):
    serializer_class = SurveyResponsesSerializer

    def get_queryset(self):
        """
        This view should return a list of all the surveys for
        the project as determined by the project_id portion of the URL.
        """
        survey_id = self.kwargs['survey_id']
        return SurveyResponses.objects.filter(survey=survey_id)



class SurveyConfig(generics.ListAPIView):
    serializer_class = SurveyQuestionsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the surveys for
        the project as determined by the project_id portion of the URL.
        """
        survey_id = self.kwargs['survey_id']
        return SurveyQuestions.objects.filter(survey=survey_id)
    
    
    
    
class getFeedback(APIView):
    
    def get(self, request):
        
        username    = request.GET.get('username',0)
        #last_id     = request.GET.get('lastId','')
        
        if  not username:
            response    = {
                'status':   'failed',
                'message':  'Username is required',
            }
            logging.info('Feedback: Username not supplied')
            return Response(response,status=202);
        
        if not User.objects.filter(username=username).exists():
            
            response    = {
                'status':   'failed',
                'message':  'Invalid Username',
            }
            logging.info('Feedback: Invalid Username')
            return Response(response,status=202);
            
        # retrieve feedback
        try: 
            user            = User.objects.get(username=username)
            all_feedback    = notes.objects.filter(Q(survey_notes__created_by=user))
            holder          = []
            print(all_feedback)
            for feedback in all_feedback:
                
                tmp = {
                    'id':           feedback.id,
                    'form_id':      feedback.survey_notes.all()[0].survey.form_id,
                    'instance_id':  feedback.survey_notes.all()[0].instance_id,
                    'title':        feedback.survey_notes.all()[0].survey.title,
                    'message':      feedback.message,
                    'sender':       feedback.created_by.username,
                    'chr_name':     feedback.survey_notes.all()[0].created_by.first_name+ ' '+feedback.survey_notes.all()[0].created_by.last_name,
                    'date_created': feedback.created_on.strftime('%Y-%m-%d'),
                    'status':       "pending",
                    'reply_by':     feedback.created_by.first_name+' '+feedback.created_by.last_name
                }
                holder.append(tmp)
            response    = {
                'status':   'success',
                'feedback': holder,
            }
            
            print(response)
            
            return Response(response,status=200);
        
        except Exception as e:
            print(e)
            logging.error('Feedback: failed to fetch feedback '+str(e))
            response    = {
                'status':   'failed',
                'message':  'Failed to receive messages',
            }
            return Response(response,status=200)
            
            
            

class sendFeedback(APIView):
    
    def post(self, request):
        
        username        = request.POST.get('username',False)
        instance_id     = request.POST.get('instance_id',False)
        message         = request.POST.get('message',False)
        
        
        # retrieve feedback
        try: 
            user            = User.objects.get(username=username)
            surv_resp_obj   = SurveyResponses.objects.get(instance_id=instance_id)
            
            print(surv_resp_obj)
            
            surv_resp_obj.notes.create(message=message,created_by=user)
           
            response    = {
                'status':   'success',
                'feedback': 'Feedback received',
            }
            print(response)
            return Response(response,status=200);
        
        except Exception as e:
            print(e)
            logging.error('Feedback: failed to fetch feedback '+str(e))
            response    = {
                'status':   'failed',
                'message':  'Failed to post message',
            }
            return Response(response,status=200)
            
           