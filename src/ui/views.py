from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django import forms
from .forms import ProjectForm, SurveyForm

from surveys.models import Survey, SurveyQuestions, SurveyResponses
from projects.models import Project, ProjectGroup, ProjectMember
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.db.models import Q
from .forms import *
from functools import reduce
import operator
import json

# Create your views here.
CHEVRON     = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>'


class DashboardView(generic.TemplateView):
    template_name = "pages/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch( *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        
        context['title']          = 'Dashboard'
        context['breadcrumb']     = {'Dashboard': 0,}
        context['datatable_list'] = "surveylist"
        
        context['links'] = {
            'Dashboard':        reverse('dashboard'),
            'Projects':         reverse('list_projects'),
            # 'Tutorial':         reverse('tutorial'),
            # 'Case Studies':     reverse('case_studies'),
        }
        
        #context['pg_actions']  = { 'Add Project': reverse('list_projects'),}    
        return context
    
    
class ProjectListView(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectListView, self).dispatch( *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        
        context['title'] = 'My Projects'
        context['breadcrumb'] = {'My Projects': 0,}
        context['datatable_list']   = "projectList"
        
        context['links']    = {
            'Dashboard':    reverse('dashboard'),
            'Projects':     reverse('list_projects'),
        }
        
        context['pg_actions']   = {
            'Create Project': reverse('create_project'),
        }
        
        return context
    
    
class ProjectCreateView(generic.CreateView):
    template_name   = 'forms/create_project.html'
    success_url     = '/ui/projects/create'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch( *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {'form': ProjectForm(), 'btn_create': "Create Project"}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = self.request.user
            project.save()

        return HttpResponse('<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">Project created</div>')
    
                                                     
class ProjectDetailView(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectDetailView, self).dispatch( *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        
        project_id                  = self.kwargs['pk']
        cur_project                 = Project.objects.get(pk=project_id)
        
        context['title']            = cur_project.title   
        context['breadcrumb']       = {
            cur_project.title: 0,
        }
           
        context['links']    = {
            'Dashboard':    reverse('project_dashboard'),
            'My Project':   reverse('project_detail', kwargs={'pk':project_id}),
            'Members':      reverse('list_members', kwargs={'pk':project_id}),
            'Groups':       reverse('list_groups', kwargs={'pk':project_id}),
        }
        
        j = self.request.path.split('/')
        j.reverse()
        if(j[0] == 'members'):
            context['datatable_list']    = "projectMemberslist"
            context['pg_actions']   = {'Add Member': reverse('create_xform', args=[project_id]),}
        else:      
            context['datatable_list']    = "surveylist"
            context['pg_actions']   = {
                'Upload XForm': reverse('create_xform', args=[project_id]),
                # 'Add Form': reverse('create_xform', args=[project_id]),
                #'Add Form': "'create_xform' pk="+project_id,
            }
            
        context['extra_data']   = {'project_id': project_id,}
        
        return context
    

class create_xform(generic.CreateView):
    template_name   = 'forms/create_instance.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(create_xform, self).dispatch( *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        context = {'form': SurveyForm(), 'btn_create': "Upload", 'project_id': pk}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        pass
    
    # def get_success_url(self):
    #     return self.request.path

    # def form_valid(self, form):     
    #     project_id                  = self.kwargs['pk']
    #     cur_project                 = Project.objects.get(pk=project_id)
        
    #     form.instance.created_by    = self.request.user
    #     form.instance.project       = cur_project
        
    #     cur_obj             = form.save() 
    #     survey_cfg          = init_xform(cur_obj.xform.name)
    #     cur_obj.form_id     = survey_cfg['form_id']
    #     cur_obj.save()
    #     #print(survey_cfg)
    #     self.save_survey_qns(cur_obj, survey_cfg['qns'])
        
    #     messages.success(self.request, 'Form submission successful')
    #     return super().form_valid(form)
    
    # def save_survey_qns(self, survey, survey_qns):

    #     for obj in survey_qns:
    #         sq  = SurveyQuestions.objects.create(
    #             survey=survey,
    #             ref=obj['ref'],
    #             col_name=obj['col_name'],
    #             col_type=obj['col_type'],
    #             constraints=obj['relevant'],
    #             required=obj['required'],
    #             hint=obj['hint'],
    #             options=obj['options'],
    #             page=obj['page'],
    #             order=obj['order'],
    #             label=obj['label'])
    
        
                                                       
def manage_project_member(request, pk):
    
    context             = {}
    context['member']   = ProjectMember.objects.get(pk=pk)
    
    template            = 'pages/project/manage_member.html'
    return TemplateResponse(request,template,context)                                        
                                    
                                               
class form_data(generic.TemplateView):
    template_name = "pages/data.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(start, self).dispatch( *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(form_data, self).get_context_data(**kwargs)
        
        form_id                     = self.kwargs['pk']
        cur_form                    = Survey.objects.get(pk=form_id)
        
        context['breadcrumb']            = {
            cur_form.project.title: reverse('project_detail', kwargs={'pk':cur_form.project.id}), 
            cur_form.title: 0,
        }
        
        context['datatable_list']   = reverse('form_data_list', kwargs={'pk':form_id})
        context['links']            = _get_form_links_context(cur_form,form_id)
        context['tbl_header']       = SurveyQuestions.objects.filter(survey__id=form_id)
        context['pg_actions']       = {
            #'Add XForm': reverse('create_xform', args=[project_id]),
            #'Add Form': reverse('create_xform', args=[project_id]),
            #'Add Form': "'create_xform' pk="+project_id,
        }
        
        
        
        context['extra_data']   = {
            'project_id': cur_form.project.id,
            'form_id': form_id,
        }
        
        return context

   
                                                     
class form_mapping(generic.TemplateView):
    template_name = "pages/start.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(start, self).dispatch( *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(form_mapping, self).get_context_data(**kwargs)
        
        
        form_id                     = self.kwargs['pk']
        cur_form                    = Survey.objects.get(pk=form_id)
        
        context['breadcrumb']            = {
            cur_form.project.title: reverse('project_detail', kwargs={'pk':cur_form.project.id}), 
            cur_form.title: 0,
        }
        
        context['datatable_list']   = 'FormMappingList'
        context['links']            = _get_form_links_context(cur_form,form_id)
        
        print(context['links'])
        
        context['pg_actions']   = {
            #'Add Form': "'create_xform' pk="+project_id,
        }
         
        context['extra_data']   = {
            'project_id': cur_form.project.id,
            'form_id': form_id,
        }
        
        return context           
     
                            
def form_data_list(request, pk):
    
    # get data
    
    start               = int(request.GET.get('start',0))
    length              = int(request.GET.get('length',5))
    draw                = int(request.GET.get('draw',1))
    search              = request.GET.get('search[value]')
    
    
    
    #req_val             = request.GET   
    #for i,j in req_val.items():
    #    print(i,' - ',j)
        
    sort_col            = int(request.GET.get('order[0][column]',-1))
    sort_dir            = request.GET.get('order[0][dir]',-1)
    
    cols            = SurveyQuestions.objects.filter(survey__id=pk).values("col_name")  
    adata           = SurveyResponses.objects.filter(survey__id=pk)
    recordsTotal    = adata.count()
    
    
    if search:
        or_filter   = []
        for k in cols:
            or_filter.append(("response__"+k['col_name']+"__icontains",search))
        
        q_list  = [Q(x) for x in or_filter]
        adata    = adata.filter(reduce(operator.or_, q_list))
    
    if sort_col > -1:
        if sort_dir == 'desc':
            sd = "-"+"response__"+cols[0]['col_name']
        else:
            sd = "response__"+cols[0]['col_name']
            
        adata   = adata.order_by(sd)
    
    
    
    recordsFiltered     = adata.count()
    data                = adata[start:start+length]
    
    bb      = []
    for r in data:
        jj      = [r.id]
        for k in cols:
            jj.append(r.response.get(k['col_name'],""))
        bb.append(jj)
    
    jan = {
        "draw": draw,
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsFiltered,
        "data": bb
        }
    
    return JsonResponse(jan,safe=False)
      

                                              
class data_instance_wrp(generic.TemplateView):
    
    template_name = "pages/instance.html"
    
    def get_context_data(self, **kwargs):
        context = super(data_instance_wrp, self).get_context_data(**kwargs)
        id      = self.kwargs['pk']
        con     = get_data_from_instance(id)
        context['id']   = id
        for k,v in con.items():
            context[k]  = v
        
        return context
                                                       
def instance_data(request,pk):
    context     = {}
    context     = get_data_from_instance(pk)
    
    return render(request, 'pages/instance_data.html', context)

                                             
def instance_messages(request,pk):
    context     = {}
    context     = get_data_from_instance(pk)
    
    return render(request, 'pages/instance_messages.html', context)

                                             
def instance_location(request,pk):
    pass 

                                             
def instance_media(request,pk):
    pass 

def get_data_from_instance(pk):
    instance                    = SurveyResponses.objects.get(pk=pk)
    questions                   = SurveyQuestions.objects.filter(survey__id=instance.survey.id).order_by('order').values()
    
    qn  = []
    tmp     = {}
    for que in questions:
        j = que['ref'].split('/')
        if j[2] not in tmp:
            tmp[j[2]]   = []
            
        tmp[j[2]].append(que)
    qn.append(tmp)
    
    context     = {}
    context['data_instance']    = instance.response
    context['data_questions']   = qn
        
    return context
                                 
                                              
class data_chat(generic.TemplateView):
    template_name = "pages/chat.html"
    
    


def _get_form_links_context(cur_form,form_id):
    
    links = {
                'Dashboard':    reverse('form_dashboard', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Data':         reverse('form_data', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Map':          reverse('form_map', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Chart':        reverse('form_chart', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Mapping Fields':        reverse('form_mapping', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Permissions':        reverse('form_chart', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
                'Triggers and Alerts':     reverse('form_chart', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
            }
    
    return links






class SurveyQuestionsUpdateView(generic.UpdateView):
    model           = SurveyQuestions
    form_class      = UpdateMappingForm
    template_name   = 'forms/update_mapping.html'
    
    def get_context_data(self, **kwargs):
        context = super(SurveyQuestionsUpdateView, self).get_context_data(**kwargs)
        context['btn_create'] = "Update"
        
        return context
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('update_mapping', kwargs={'pk': pk})
        
        