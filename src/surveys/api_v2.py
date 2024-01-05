from django.http import Http404, HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from surveys.models import Survey, SurveyQuestions, SurveyResponses, SurveyFilter, notes

from django.shortcuts import redirect, get_object_or_404, render
import os
from django.conf import settings


@csrf_exempt
def submission(request):
    pass


@csrf_exempt
def form_list(request):
    surveys = Survey.objects.all()
    # print(surveys)
    # print(current_user)
    context = {
        "surveys": surveys,
    }

    response = render(
        request, "odk_xform_list.json", context, content_type="text/json; charset=utf-8"
    )

    return response


def form_get(request, id):

    survey  = get_object_or_404(Survey, pk=id)


    if os.path.exists(survey.xform.path):
       
        file_path   = os.path.join(settings.MEDIA_ROOT, 'jform/defn/',survey.form_id+'.json')
        text_file = open(file_path, "rb")
        data = text_file.read()
        text_file.close()

        response = HttpResponse(data, content_type="text/json; charset=utf-8")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(survey.xform.path)
        return response
    
    raise Http404