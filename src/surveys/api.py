from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser

from .serializers import SurveyQuestionsSerializer, SurveySerializer, SurveyResponsesSerializer
from surveys.models import Survey, SurveyQuestions, SurveyResponses
from surveys.utils import init_xform



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