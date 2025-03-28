import json
import logging, ast
import operator
from functools import reduce
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django import forms

from . import x2jform

from django.utils.timezone import make_aware
from django.utils.dateformat import DateFormat
from .forms import (
    ProjectForm,
    SurveyForm,
    ManageMemberGroupsFrom,
    ChangePmPasswordForm,
    GroupForm,
)

from django.views.decorators.csrf import csrf_exempt
from surveys.models import Survey, SurveyQuestions, SurveyResponses, perms_user
from projects.models import Project, ProjectGroup, ProjectMember
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.db.models import Q
from .forms import *
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from src.surveys.utils import *


# Create your views here.
CHEVRON = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>'


class DashboardView(generic.TemplateView):
    template_name = "pages/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # data collectors
        data_collectors = User.objects.filter(groups__name="DataCollectors").count()
        context["data_collectors"] = data_collectors

        # published forms
        published_forms = Survey.objects.count()
        context["published_forms"] = published_forms

        # data collected
        data_collected = SurveyResponses.objects.count()
        context["data_collected"] = data_collected

        # messages
        messages = 0
        context["messages"] = messages

        context["title"] = "Dashboard"
        context["breadcrumb"] = {
            "Dashboard": 0,
        }
        context["datatable_list"] = "surveylist"

        context["links"] = {
            "Dashboard": reverse("dashboard"),
            "Projects": reverse("list_projects"),
        }

        return context


class ProjectDashboardView(generic.TemplateView):
    template_name = "pages/projects/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDashboardView, self).get_context_data(**kwargs)

        project_id = self.kwargs["pk"]
        cur_project = Project.objects.get(pk=project_id)

        # data collectors
        members = ProjectMember.objects.filter(project=cur_project).count()
        context["members"] = members

        # published forms
        published_forms = Survey.objects.filter(project=cur_project).count()
        context["published_forms"] = published_forms

        # data collected
        survey_responses = SurveyResponses.objects.filter(survey__project=cur_project)
        context["form_data"] = survey_responses
        # context['geopoints']    = SurveyQuestions.objects.filter(Q(survey__project=cur_project) & Q(col_type='geopoint')).values('survey__project_id','col_name').distinct()

        # print(context['geopoints'])

        context["data_collected"] = survey_responses.count()

        # messages
        messages = 0
        context["messages"] = messages

        context["title"] = "Dashboard"
        context["project_id"] = project_id
        context["breadcrumb"] = {
            "Dashboard": 0,
        }

        context["title"] = cur_project.title
        context["breadcrumb"] = {
            cur_project.title: 0,
        }

        context["links"] = {
            "Dashboard": reverse("project_dashboard", kwargs={"pk": project_id}),
            "Forms": reverse("project_detail", kwargs={"pk": project_id}),
            "Members": reverse("list_members", kwargs={"pk": project_id}),
            "Groups": reverse("list_groups", kwargs={"pk": project_id}),
        }

        return context


class ProjectListView(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        context["title"] = "Projects"
        context["breadcrumb"] = {
            "My Projects": 0,
        }
        context["datatable_list"] = "projectList"

        context["links"] = {
            "Dashboard": reverse("dashboard"),
            "Projects": reverse("list_projects"),
        }

        context["pg_actions"] = {
            "Create Project": reverse("create_project"),
        }

        return context


class ProjectCreateView(generic.CreateView):
    template_name = "pages/projects/create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {"form": ProjectForm(), "btn_create": "Create Project"}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = self.request.user
            project.save()

            # return response
            logging.info("Project created => " + project.pk)
            return HttpResponse(
                '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Project created</div>'
            )
        return render(
            request, self.template_name, {"form": form, "btn_create": "Create Project"}
        )


class ProjectDetailView(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        project_id = self.kwargs["pk"]
        cur_project = Project.objects.get(pk=project_id)

        context["title"] = cur_project.title
        context["breadcrumb"] = {
            cur_project.title: 0,
        }

        context["links"] = {
            "Dashboard": reverse("project_dashboard", kwargs={"pk": project_id}),
            "Data": reverse("project_detail", kwargs={"pk": project_id}),
            "Members": reverse("list_members", kwargs={"pk": project_id}),
            "Groups": reverse("list_groups", kwargs={"pk": project_id}),
        }

        j = self.request.path.split("/")
        j.reverse()

        if j[0] == "members":
            context["datatable_list"] = "projectMemberslist"
            context["pg_actions"] = {
                "Add Member": reverse("create_member", args=[project_id]),
            }
        elif j[0] == "groups":
            context["datatable_list"] = "projectGroupList"
            context["pg_actions"] = {
                "Add Group": reverse("create_group", args=[project_id]),
            }
        else:
            context["datatable_list"] = "surveylist"
            context["pg_actions"] = {
                "Upload XForm": reverse("create_xform", args=[project_id]),
                "Upload JForm": reverse("create_jform", args=[project_id]),
            }

        context["extra_data"] = {
            "project_id": project_id,
        }

        return context


class ProjectDeleteView(generic.View):
    """Delete Project"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        project_id = kwargs["pk"]

        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
            logging.info("project deleted => " + project.pk)

            """response"""
            return JsonResponse(
                {"error": False, "success_msg": "Project deleted"}, safe=False
            )
        except:
            logging.error("Project does not exists")

            """response"""
            return JsonResponse(
                {"error": True, "error_msg": "Failed to delete project"}, safe=False
            )


class XformCreateView(generic.CreateView):
    template_name = "pages/forms/create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(XformCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "form": SurveyForm(),
            "btn_create": "Upload",
            "project_id": kwargs["pk"],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SurveyForm(request.POST, request.FILES)

        if form.is_valid():
            project_id = self.kwargs["pk"]
            cur_project = Project.objects.get(pk=project_id)

            # process form
            survey_form = form.save(commit=False)
            survey_form.created_by = self.request.user
            survey_form.project = cur_project
            cur_obj = form.save()

            logging.info("Survey created => ")

            # initiate form
            survey_cfg = init_xform(cur_obj.xform.name)
            survey_form.form_type = "XFORM"
            cur_obj.form_id = survey_cfg["form_id"]
            cur_obj.save()

            # save survey questions
            self.save_survey_qns(cur_obj, survey_cfg["qns"])

            return HttpResponse(
                '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Form uploaded</div>'
            )
        return render(
            request,
            self.template_name,
            {"form": form, "btn_create": "Upload", "project_id": kwargs["pk"]},
        )

    def save_survey_qns(self, survey, survey_qns):
        """saving survey question to database"""
        for obj in survey_qns:
            sq = SurveyQuestions.objects.create(
                survey=survey,
                ref=obj["ref"],
                col_name=obj["col_name"],
                col_type=obj["col_type"],
                constraints=obj["relevant"],
                required=obj["required"],
                hint=obj["hint"],
                options=obj["options"],
                page=obj["page"],
                order=obj["order"],
                label=obj["label"],
            )
            # log action
            logging.info("save survey questions")
            logging.info(survey)


class JformCreateView(generic.CreateView):
    template_name = "pages/forms/create_jform.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JformCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "form": SurveyForm(),
            "btn_create": "Upload",
            "project_id": kwargs["pk"],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SurveyForm(request.POST, request.FILES)

        if form.is_valid():
            project_id = self.kwargs["pk"]
            cur_project = Project.objects.get(pk=project_id)

            # process form
            survey_form = form.save(commit=False)
            survey_form.created_by = self.request.user
            survey_form.form_type = "JFORM"
            survey_form.project = cur_project
            cur_obj = form.save()

            logging.info("Survey created => ")

            # initiate form
            survey_cfg = x2jform.x2jform(
                cur_obj.xform.name, survey_form.title, survey_form.description
            )
            cur_obj.form_id = survey_cfg["meta"]["form_id"]
            cur_obj.jForm = survey_cfg
            cur_obj.save()

            # save survey questions
            # self.save_survey_qns(cur_obj, survey_cfg['pages'])

            return HttpResponse(
                '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Form uploaded</div>'
            )
        return render(
            request,
            self.template_name,
            {"form": form, "btn_create": "Upload", "project_id": kwargs["pk"]},
        )

    def save_survey_qns(self, survey, survey_qns):
        """saving survey question to database"""
        for obj in survey_qns:
            sq = SurveyQuestions.objects.create(
                survey=survey,
                ref=obj["ref"],
                col_name=obj["col_name"],
                col_type=obj["col_type"],
                constraints=obj["relevant"],
                required=obj["required"],
                hint=obj["hint"],
                options=obj["options"],
                page=obj["page"],
                order=obj["order"],
                label=obj["label"],
            )
            # log action
            logging.info("save survey questions")
            logging.info(survey)


class XformDeleteView(generic.View):
    """Delete Xform"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(XformDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        xform_id = kwargs["pk"]

        try:
            xform = Survey.objects.get(pk=xform_id)
            xform.delete()
            logging.info("survey deleted")

            # todo: delete xml file

            """response"""
            return JsonResponse(
                {"error": False, "success_msg": "Xform deleted"}, safe=False
            )
        except:
            """response"""
            return JsonResponse(
                {"error": True, "error_msg": "Failed to delete xform"}, safe=False
            )


class MemberCreateView(generic.TemplateView):
    template_name = "pages/projects/members/create.html"
    success_url = "/ui/projects/create"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "form": MemberForm(
                initial={"project": Project.objects.get(pk=kwargs["pk"])}
            ),
            "btn_create": "Add Member",
            "project_id": kwargs["pk"],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()

            # return response
            logging.info("Project member created/assigned")
            return HttpResponse(
                '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Member Added</div>'
            )
        return render(
            request, self.template_name, {"form": form, "btn_create": "Add Member"}
        )


def manage_project_member(request, pk):
    """Manage project members"""
    context = {}
    context["member"] = ProjectMember.objects.get(pk=pk)
    template = "pages/projects/members/index.html"
    return TemplateResponse(request, template, context)


class GroupCreateView(generic.TemplateView):
    template_name = "pages/projects/groups/create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "form": GroupForm(
                initial={"project": Project.objects.get(pk=kwargs["project_id"])}
            ),
            "btn_create": "Create Group in Project",
            "project_id": kwargs["project_id"],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

            # return response
            logging.info("Project group assigned/created")
            return HttpResponse(
                '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Group added to Project</div>'
            )
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "btn_create": "Create Project",
                "project_id": kwargs["project_id"],
            },
        )


class EditGroupView(generic.UpdateView):
    model = ProjectGroup
    form_class = GroupForm
    template_name = "pages/projects/groups/edit.html"

    def get_context_data(self, **kwargs):
        context = super(EditGroupView, self).get_context_data(**kwargs)
        context["btn_create"] = "Update"
        context["pk"] = self.kwargs["pk"]
        return context

    def get_success_url(self):
        pk = self.kwargs["pk"]
        messages.success(self.request, "Group updated")
        return reverse("edit_group", kwargs={"pk": pk})


def manage_project_group(request, pk):
    """Manage project group"""
    context = {}
    context["group"] = ProjectGroup.objects.get(pk=pk)
    template = "pages/projects/groups/index.html"
    return TemplateResponse(request, template, context)


def manage_form_summary(request, project_id, pk):
    context = {}
    context["project_id"] = project_id
    context["pk"] = pk
    template = "pages/project/form_summary/index.html"
    return TemplateResponse(request, template, context)


class form_summary_map(generic.TemplateView):
    template_name = "pages/project/form_summary/map.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(form_summary_map, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(form_summary_map, self).get_context_data(**kwargs)

        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        # get col_names of survey questions that are geo points
        context["form_data"] = SurveyResponses.objects.filter(Q(survey__id=form_id))
        context["geopoints"] = get_geopoints(form_id)
        return context


class ManagePmGroups(generic.UpdateView):
    """Manage Member Groups"""

    model = ProjectMember
    form_class = ManageMemberGroupsFrom
    template_name = "pages/projects/members/manage_groups.html"

    def get_context_data(self, **kwargs):
        context = super(ManagePmGroups, self).get_context_data(**kwargs)
        context["btn_create"] = "Update Member Groups"
        context["pk"] = self.kwargs["pk"]
        return context

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("manage_pm_groups", kwargs={"pk": pk})

    def get_form_kwargs(self):
        kwargs = super(ManagePmGroups, self).get_form_kwargs()
        Member = ProjectMember.objects.get(pk=self.kwargs["pk"])
        kwargs["project_id"] = Member.project.id
        return kwargs


class FormDataView(generic.TemplateView):
    """Form data"""

    template_name = "pages/forms/data.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormDataView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormDataView, self).get_context_data(**kwargs)

        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        context["breadcrumb"] = {
            cur_form.project.title: reverse(
                "project_detail", kwargs={"pk": cur_form.project.id}
            ),
            cur_form.title: 0,
        }

        context["title"] = cur_form.title
        context["datatable_list"] = reverse("form_data_list", kwargs={"pk": form_id})
        context["links"] = _get_form_links_context(cur_form, form_id)

        # get jform

        context["tbl_header"] = get_table_header(cur_form.jForm)
        #print(context["tbl_header"])
        
        context["pg_actions"] = {}

        context["extra_data"] = {
            "project_id": cur_form.project.id,
            "form_id": form_id,
        }

        return context


def get_table_header(jform):

    header = {}
    for item in jform["pages"]:
        if item["type"] == "group":
            for k,v in item['fields'].items():
                header[k]   = v
    return header


class FormMappingView(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormMappingView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormMappingView, self).get_context_data(**kwargs)
        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        context["breadcrumb"] = {
            cur_form.project.title: reverse(
                "project_detail", kwargs={"pk": cur_form.project.id}
            ),
            cur_form.title: 0,
        }

        context["title"] = cur_form.title
        context["datatable_list"] = "FormMappingList"
        context["links"] = _get_form_links_context(cur_form, form_id)
        context["pg_actions"] = {}
        context["responsive"] = "false"

        context["extra_data"] = {
            "project_id": cur_form.project.id,
            "form_id": form_id,
        }

        return context


class FormDashboardView(generic.TemplateView):
    template_name = "pages/forms/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormDashboardView, self).get_context_data(**kwargs)

        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        context["breadcrumb"] = {
            cur_form.project.title: reverse(
                "project_dashboard", kwargs={"pk": cur_form.project.id}
            ),
            cur_form.title: 0,
            "Dashboard": 0,
        }

        context["title"] = cur_form.title
        context["links"] = _get_form_links_context(cur_form, form_id)
        context["geopoints"] = get_geopoints(form_id)

        survey_responses = SurveyResponses.objects

        context["form_data"] = survey_responses.filter(Q(survey__id=form_id))
        context["data_collectors"] = (
            survey_responses.filter(survey__id=form_id).values("created_by").count()
        )
        context["data_collected"] = survey_responses.count()

        # published forms
        published_forms = Survey.objects.count()
        context["published_forms"] = published_forms

        # messages
        messages = 0
        context["messages"] = messages

        return context


class FormMapView(generic.TemplateView):
    template_name = "pages/forms/map.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormMapView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormMapView, self).get_context_data(**kwargs)

        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        context["breadcrumb"] = {
            cur_form.project.title: reverse(
                "project_detail", kwargs={"pk": cur_form.project.id}
            ),
            cur_form.title: 0,
            "Map": 0,
        }

        context["title"] = cur_form.title
        context["links"] = _get_form_links_context(cur_form, form_id)
        context["form_data"] = SurveyResponses.objects.filter(Q(survey__id=form_id))
        context["geopoints"] = get_geopoints(form_id)
        return context


def get_geopoints(form_id):
    # return data
    logging.info("Filtering geopoints data")
    return SurveyQuestions.objects.filter(
        Q(survey__id=form_id) & Q(col_type="geopoint")
    ).values("col_name")


class FormPermsView(generic.TemplateView):
    template_name = "pages/forms/perms.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FormPermsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormPermsView, self).get_context_data(**kwargs)

        form_id = self.kwargs["pk"]
        cur_form = Survey.objects.get(pk=form_id)

        context["breadcrumb"] = {
            cur_form.project.title: reverse(
                "project_detail", kwargs={"pk": cur_form.project.id}
            ),
            cur_form.title: 0,
        }

        context["title"] = cur_form.title
        context["all_members"] = ProjectMember.objects.filter(
            project__id=cur_form.project.id
        )
        context["sel_members"] = list(
            cur_form.user_access.all().values_list("user_id", flat=True)
        )

        context["all_groups"] = ProjectGroup.objects.filter(
            project__id=cur_form.project.id
        )
        context["sel_groups"] = list(
            cur_form.group_access.all().values_list("group_id", flat=True)
        )

        context["form_id"] = form_id
        context["links"] = _get_form_links_context(cur_form, form_id)
        context["pg_actions"] = {}

        return context


@csrf_exempt
def update_survey_access(request, pk):
    cur_form = Survey.objects.get(pk=pk)
    # Remove all permissions
    cur_form.user_access.all().delete()
    cur_form.group_access.all().delete()

    try:
        for item in request.POST.getlist("perms"):
            if item[:3] == "MMM":
                cur_form.user_access.create(user=ProjectMember.objects.get(pk=item[3:]))
            else:
                cur_form.group_access.create(
                    group=ProjectGroup.objects.get(pk=item[3:])
                )

        # return response
        logging.info("Update survey access to user/group")
        return HttpResponse(
            '<span class="bg-green-300 px-4 py-1 rounded-md">Successfully Updated</span>'
        )
    except:
        logging.error("Failed to update survey access to user/group")
        return HttpResponse(
            '<span class="bg-red-300 px-4 py-1" rounded-md>Failed to Update</span>'
        )


class MembersPermsView(generic.TemplateView):
    template_name = "pages/projects/members/perms.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MembersPermsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MembersPermsView, self).get_context_data(**kwargs)

        member_id = self.kwargs["pk"]
        cur_member = ProjectMember.objects.get(pk=member_id)

        context["all_surveys"] = Survey.objects.filter(
            project__id=cur_member.project.id
        )
        context["sel_surveys"] = list(
            Survey.objects.filter(user_access__user=cur_member).values_list(
                "id", flat=True
            )
        )
        context["member_id"] = member_id
        return context


@csrf_exempt
def update_members_access(request, pk):
    member = ProjectMember.objects.get(pk=pk)
    # Remove all permissions
    perms_user.objects.filter(survey_users__user_access__user=member).delete()

    try:
        for item in request.POST.getlist("perms"):
            cur_form = Survey.objects.get(pk=item)
            cur_form.user_access.create(user=member)

        # return response
        logging.info("Update survey access to member")
        return HttpResponse(
            '<span class="bg-green-300 px-4 py-1 rounded-md">Successfully Updated</span>'
        )
    except:
        logging.error("Failed to update survey access to member")
        return HttpResponse(
            '<span class="bg-red-300 px-4 py-1" rounded-md>Failed to Update</span>'
        )


def form_data_list(request, pk):
    """Show form data"""
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 5))
    draw = int(request.GET.get("draw", 1))
    search = request.GET.get("search[value]")
    search_from = request.GET.get("search_from")
    search_to = request.GET.get("search_to")
    sort_col = int(request.GET.get("order[0][column]", -1))
    sort_dir = request.GET.get("order[0][dir]", -1)

    # print(search_from+' '+search_to)
    # print(request.GET.get)

    if search:
        search_str = json.loads(search)
    else:
        search_str = {}
    # print(search_str)

    search_val = search_str.get("search_val")
    min_date = search_str.get("min_date")
    max_date = search_str.get("max_date")

    cols = SurveyQuestions.objects.filter(survey__id=pk).values()
    adata = SurveyResponses.objects.filter(survey__id=pk)
    recordsTotal = adata.count()

    if cols.count() > 0:

        if search_val:
            or_filter = []
            for k in cols:
                or_filter.append(
                    ("response__" + k["col_name"] + "__icontains", search_val)
                )

            q_list = [Q(x) for x in or_filter]
            adata = adata.filter(reduce(operator.or_, q_list))

        if min_date:
            adata = adata.filter(
                created_on__gte=datetime.strptime(min_date, "%Y-%m-%d").date()
            )

        if max_date:
            adata = adata.filter(
                created_on__lte=datetime.strptime(max_date, "%Y-%m-%d").date()
            )

        if sort_col > -1:
            print(cols)
            if sort_dir == "desc":
                sd = "-" + "response__" + cols[0]["col_name"]
            else:
                sd = "response__" + cols[0]["col_name"]

            adata = adata.order_by(sd)

    recordsFiltered = adata.count()
    data = adata[start : start + length]

    final_data = []
    for r in data:
        jj = [r.id]
        for k in cols:
            jj.append(r.response.get(k["col_name"], ""))
            if k["col_type"] == "select":
                selected_options = r.response.get(k["col_name"], "").split(" ")
                avail_options = ast.literal_eval(k["options"])
                if "pair" in avail_options:
                    for opt in avail_options["pair"]:
                        for i in opt:
                            if i in selected_options:
                                jj.append("1")
                            else:
                                jj.append("0")

        dt = DateFormat(r.created_on)
        jj.append(dt.format("Y-m-d H:i:s"))
        jj.append(r.created_by.first_name + " " + r.created_by.last_name)
        jj.append(r.created_by.username)
        final_data.append(jj)

    jan = {
        "draw": draw,
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsFiltered,
        "data": final_data,
    }

    return JsonResponse(jan, safe=False)


class data_instance_wrp(generic.TemplateView):
    """show single data instance"""

    template_name = "pages/instances/instance.html"

    def get_context_data(self, **kwargs):
        context = super(data_instance_wrp, self).get_context_data(**kwargs)
        id = self.kwargs["pk"]
        con = get_data_from_instance(id)
        context["id"] = id
        context["notes"] = _get_survey_notes(id)
        for k, v in con.items():
            context[k] = v

        return context


def instance_data(request, pk):
    context = {}
    context = get_data_from_instance(pk)

    return render(request, "pages/instances/instance_data.html", context)


def instance_messages(request, pk):
    if request.method == "POST":
        sr = SurveyResponses.objects.get(pk=pk)
        sr.notes.create(message=request.POST.get("message"), created_by=request.user)
        return JsonResponse(1, safe=False)
    else:
        context = {}
        return render(request, "pages/instances/instance_messages.html", context)


def _get_survey_notes(pk):
    sr_obj = SurveyResponses.objects.get(pk=pk)
    all_notes = sr_obj.notes.all().order_by("-created_on")
    notes = []

    for n in all_notes:
        tmp = {
            "message": n.message,
            "created_by": n.created_by.id,
            "initials": n.created_by.first_name[0].upper()
            + n.created_by.last_name[0].upper(),
            "name": n.created_by.first_name + " " + n.created_by.last_name,
            "created_on": naturalday(n.created_on),
        }
        notes.append(tmp)

    return notes


def instance_messages_add(request):
    if request.method == "POST":
        sr = SurveyResponses.objects.get(pk=request.POST.get("survey_id"))
        sr.notes.create(message=request.POST.get("message"), created_by=request.user)

    return JsonResponse(1, safe=False)


def instance_location(request, pk):
    context = {}
    context["locations"] = get_loc_from_instance(pk)
    return render(request, "pages/instances/instance_map.html", context)


def instance_media(request, pk):
    context = {}
    context["media"] = get_media_from_instance(pk)
    return render(request, "pages/instances/instance_media.html", context)


def get_media_from_instance(pk):
    instance = SurveyResponses.objects.get(pk=pk)
    questions = SurveyQuestions.objects.filter(survey__id=instance.survey.id).values()
    loc_arr = []
    for item in questions:
        if item["col_type"] == "binary":
            tmp = {}
            cn = item["col_name"]
            tmp["desc"] = cn
            tmp["media"] = instance.response[cn]
            loc_arr.append(tmp)

    return loc_arr


def get_loc_from_instance(pk):
    instance = SurveyResponses.objects.get(pk=pk)
    questions = SurveyQuestions.objects.filter(survey__id=instance.survey.id).values()
    loc_arr = []
    for item in questions:
        if item["col_type"] == "geopoint":
            tmp = {}
            cn = item["col_name"]
            tmp["desc"] = cn
            loc = instance.response[cn]
            loc = " ".join(loc.split(" ", 2)[:-1])
            tmp["gps"] = loc.replace(" ", ", ")
            loc_arr.append(tmp)

    return loc_arr


def get_data_from_instance(pk):
    instance = SurveyResponses.objects.get(pk=pk)
    questions = (
        SurveyQuestions.objects.filter(survey__id=instance.survey.id)
        .order_by("order")
        .values()
    )

    qn = []
    tmp = {}
    for que in questions:
        j = que["ref"].split("/")
        if j[2] not in tmp:
            tmp[j[2]] = []

        tmp[j[2]].append(que)
    qn.append(tmp)

    context = {}
    context["data_instance"] = instance.response
    context["data_questions"] = qn

    return context


class data_chat(generic.TemplateView):
    template_name = "pages/chat.html"

                                                  
class ChangePmPassword(generic.TemplateView):
    template_name = "pages/projects/members/change_password.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChangePmPassword, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "form": ChangePmPasswordForm(),
            "btn_create": "Update Password",
            "id": self.kwargs["pk"],
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ChangePmPasswordForm(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data["new_password1"]
            new_password2 = form.cleaned_data["new_password2"]
            if new_password1 == new_password2:
                u = User.objects.get(pk=self.kwargs["pk"])
                u.set_password(new_password1)
                u.save()
                update_session_auth_hash(request, self.request.user)  # Important!
                u.profile.digest = calculate_digest(u.username, new_password1)
                u.save()

                # return response
                return HttpResponse(
                    '<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Password Updated</div>'
                )
            else:
                return HttpResponse(
                    '<div class="bg-red-200 p-3 text-sm text-gray-600 rounded-sm">Password Update Failed - passwords mismatch</div>'
                )

        return render(
            request, self.template_name, {"form": form, "btn_create": "Update Password"}
        )


def _get_form_links_context(cur_form, form_id):
    links = {
        "Dashboard": reverse(
            "form_dashboard", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        "Data": reverse(
            "form_data", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        "Map": reverse(
            "form_map", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        "Chart": reverse(
            "form_chart", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        "Humanize Fields": reverse(
            "form_mapping", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        "Permissions": reverse(
            "form_perms", kwargs={"project_id": cur_form.project.id, "pk": form_id}
        ),
        #'Triggers and Alerts':     reverse('form_chart', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
    }

    if get_geopoints(form_id).count() == 0:
        links.pop("Map", None)

    return links


class SurveyQuestionsUpdateView(generic.UpdateView):
    model = SurveyQuestions
    form_class = UpdateMappingForm
    template_name = "pages/forms/update_mapping.html"

    def get_context_data(self, **kwargs):
        context = super(SurveyQuestionsUpdateView, self).get_context_data(**kwargs)
        context["btn_create"] = "Update"
        context["uuid"] = self.kwargs["pk"]

        return context

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("update_mapping", kwargs={"pk": pk})
