from rest_framework import serializers
from surveys.models import Survey, SurveyQuestions, SurveyResponses, SurveyFilter


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survey # this is the model that is being serialized
        fields = ('project','title','form_id','xform','description','created_by','created_on')
        read_only_fields =  ('form_id','project')


class SurveyQuestionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SurveyQuestions # this is the model that is being serialized
        fields = ('survey', 'ref', 'col_name', 'col_type', 'qn_options', 'page','created_on','created_by')


class SurveyResponsesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model   = SurveyResponses
        fields  = ('survey','instance_id','response','created_by','created_on')



class SurveyFilterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model   = SurveyFilter
        fields  = ('survey','title','data_filter')


