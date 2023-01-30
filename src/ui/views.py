from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls import reverse

from surveys.models import Survey, SurveyQuestions, SurveyResponses
from projects.models import Project, ProjectGroup, ProjectMember

# Create your views here.



class start(generic.TemplateView):
    template_name = "pages/start.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(start, self).get_context_data(**kwargs)
        
        context['title']    = 'Community Based One Health Security'
        context['datatable_list']    = "surveylist"
        
        context['links']    = {
            'Dashboard':        reverse('start'),
            'Projects':         reverse('list_projects'),
            'Tutorial':         reverse('tutorial'),
            'Case Studies':     reverse('case_studies'),
            'Awknoledgments':   reverse('awknoledgement'),
        }
        
        context['pg_actions']   = {
            'Add Project': reverse('list_projects'),
        }
        
        
        return context
    
    

class list_projects(generic.TemplateView):
    template_name = "pages/start.html"
    
    def get_context_data(self, **kwargs):
        context = super(list_projects, self).get_context_data(**kwargs)
        
        context['title']            = 'My Projects'
        context['datatable_list']   = "projectList"
        #context['datatable_delete]
        #context['datatable_detail]
        
        context['links']    = {
            'Dashboard':    reverse('list_projects'),
            'Projects':     reverse('list_projects'),
            'Members':      reverse('list_projects'),
        }
        
        
        context['pg_actions']   = {
            'Add Project': reverse('create_project'),
        }
        
        return context
    
    
 
class create_project(generic.CreateView):
 
    model           = Project
    fields          = ['title', 'description']
    template_name   = 'forms/create_instance.html'
    success_url     = '/ui/project/create'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Form submission successful')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["btn_create"] = "Create Project"
        return context
    

class create_xform(generic.CreateView):

    model           = Survey
    fields          = ['title', 'description', 'xform']
    template_name   = 'forms/create_instance.html'
    
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        
        project_id                  = self.kwargs['pk']
        cur_project                 = Project.objects.get(pk=project_id)
        
        form.instance.created_by    = self.request.user
        form.instance.project       = cur_project
        
        cur_obj             = form.save() 
        survey_cfg          = init_xform(cur_obj.xform.name)
        cur_obj.form_id     = survey_cfg['form_id']
        cur_obj.save()
        #print(survey_cfg)
        self.save_survey_qns(cur_obj, survey_cfg['qns'])
        
        messages.success(self.request, 'Form submission successful')
        return super().form_valid(form)
    
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
                page=obj['page'],
                order=obj['order'],
                label=obj['label'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["btn_create"] = "Add Xform"
        return context  
        
    
                                                     
class project_detail(generic.TemplateView):
    template_name = "pages/start.html"
    
    def get_context_data(self, **kwargs):
        context = super(project_detail, self).get_context_data(**kwargs)
        
        project_id                  = self.kwargs['pk']
        cur_project                 = Project.objects.get(pk=project_id)
        
        context['title']            = cur_project.title
        context['datatable_list']    = "surveylist"
        #context['datatable_delete]
        #context['datatable_detail]
        
        context['links']    = {
            'Dashboard':    reverse('project_dashboard'),
            'Projects':     reverse('project_dashboard'),
            'Members':      reverse('project_dashboard'),
        }
        
        context['pg_actions']   = {
            'Add XForm': reverse('create_xform', args=[project_id]),
            'Add Form': reverse('create_xform', args=[project_id]),
            #'Add Form': "'create_xform' pk="+project_id,
        }
        
        context['extra_data']   = {
            'project_id': project_id,
        }
        
        return context
                                                       
                                                     
                                    
                                               
class form_data(generic.TemplateView):
    template_name = "pages/start.html"
    
    def get_context_data(self, **kwargs):
        context = super(form_data, self).get_context_data(**kwargs)
        
        form_id                     = self.kwargs['pk']
        cur_form                    = Survey.objects.get(pk=form_id)
        
        context['title']            = cur_form.project.title+': '+cur_form.title
        context['datatable_list']   = "formData"
        #context['datatable_delete]
        #context['datatable_detail]
        
        context['links']    = {
            'Dashboard':    reverse('form_dashboard', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
            'Data':         reverse('form_data', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
            'Map':          reverse('form_map', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
            'Chart':        reverse('form_chart', kwargs={'project_id':cur_form.project.id,'pk':form_id}),
        }
        
        context['pg_actions']   = {
            #'Add XForm': reverse('create_xform', args=[project_id]),
            #'Add Form': reverse('create_xform', args=[project_id]),
            #'Add Form': "'create_xform' pk="+project_id,
        }
        
        context['extra_data']   = {
            'project_id': cur_form.project.id,
            'form_id': form_id,
        }
        
        return context
                                                       
                                                     
                                        