from rest_framework import serializers
from surveys.models import Survey, SurveyQuestions, SurveyResponses, SurveyFilter


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey # this is the model that is being serialized
        fields = ('project','title','form_id','xform','description','created_by','created_on')
        read_only_fields =  ('form_id','project')


class SurveyQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestions # this is the model that is being serialized
        fields = ('survey', 'ref', 'col_name', 'col_type', 'hint', 'label', 'options', 'constraints','page','order','required')


class SurveyResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = SurveyResponses
        fields  = ('survey','instance_id','response','created_by','created_on')



class SurveyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model   = SurveyFilter
        fields  = ('survey','title','data_filter')


