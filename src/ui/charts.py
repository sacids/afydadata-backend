import json
from datetime import datetime, date, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from surveys.models import Survey, SurveyQuestions, SurveyResponses, perms_user


class SurveyChartView(APIView):
    def get(self, request, format=None):
        # surveys
        surveys = Survey.objects

        # filter per permissions
        surveys = surveys.all()

        arr_data = []
        for val in surveys:
            summation = SurveyResponses.objects.filter(survey_id=val.pk)

            if request.GET.get('period') != None:
                period = request.GET.get('period')

                # declare variable
                this_year = datetime.now().year
                this_month = datetime.now().month
                this_day = date.today()
                last_7_days = date.today() - timedelta(days=7)

                if period == "All":
                    summation = summation
                else:
                    if period == "Monthly":
                        summation = summation.filter(created_on__month=this_month, created_on__year=this_year)
                    elif period == "Weekly":
                        summation = summation.filter(created_on__range=[last_7_days, this_day])
                    elif period == "Daily":
                        summation = summation.filter(created_on__date=this_day)                    
            else:
                summation = summation

            # filter based on user permissions
            summation = summation.count()

            # create dict
            chart = {
                'survey': val.title,
                'data': summation,
            }
            # append to arr_data
            arr_data.append(chart)

        # response
        return Response({"error": False, "chart": arr_data}, status=status.HTTP_200_OK)
