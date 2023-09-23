from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturalday

from surveys.models import Survey, SurveyQuestions, SurveyResponses
from projects.models import Project, ProjectGroup, ProjectMember

import json
from django.forms.models import model_to_dict

class PermissionAjaxDatatableView(AjaxDatatableView):

    model                   = Permission
    title                   = 'Permissions'
    show_column_filters     = False
    initial_order           = [["app_label", "asc"], ]
    length_menu             = [[8, 20, 50, 100, -1], [8, 20, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select         = False

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'codename', 'visible': True, },
        {'name': 'name', 'visible': True, 'className':'text-left text-green-800 font-medium' },
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]
    
    

class SurveyList(AjaxDatatableView):
    model                       = Survey
    title                       = 'Survey'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'title', 'visible': True,'className':'text-left font-semibold cursor-pointer' },
        {'name': 'description', 'visible': True,'className':'text-left ' },
        {'name': 'form_id', 'visible': True,'className':'text-left  ' },
        {'name': 'xform', 'visible': True,'className':'text-left ' },
        {'name': 'project_id', 'foreign_field': 'project__id', 'title': '', 'visible': False,},
        {'name': 'created_on', 'title':'Created','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'del','title':'','visible': True, 'className':'w-4 text-left','placeholder':'True','searchable': False,},
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        #row['title'] = '<a href="%s">%s</a>' % (
        #    reverse('event', args=(obj.id,)),
        #    obj.title
        #)
        
        #url = reverse('form_data', args=['pk':'1', 'project_id':'1'])
        absolute_url = reverse('form_data', kwargs=({'project_id':obj.project_id,'pk': obj.id}))
        form_summary_url = reverse('manage_form_summary', kwargs=({'project_id':obj.project_id,'pk': obj.id}))
        
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''

        row['qv']           = '<span class="text-sm" @click="sidebar = !sidebar, dataDetail(\''+str(obj.title)+'\',\''+form_summary_url+'\')" >'+arr+'</span>'
        row['title']        = '<a class="" href="'+absolute_url+'" >'+str(obj.title)+'</a>'      
        row['created_on']   = naturalday(obj.created_on)
        row['del']          = '''<svg xmlns="http://www.w3.org/2000/svg" 
                                    class="h-4 w-4 text-slate-300 hover:text-rose-900 hover:cursor-pointer" 
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" 
                                    @click="deleteSurvey(\'''' + str(obj.id) + '''\')">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>'''
        
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'project_id' in request.REQUEST:
            project_id = request.REQUEST.get('project_id')
            queryset = queryset.filter(project__id=project_id)

        return queryset


class projectMemberslist(AjaxDatatableView):
    model                       = ProjectMember
    title                       = 'Project Members'
    show_column_filters         = False
    initial_order               = [["member", "desc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'member', 'visible': True,'className':'text-left' },
        {'name': 'projectGroup', 'visible': True,'className':'text-left ' },
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''

        url         = reverse('manage_members', kwargs=({'pk':obj.id}))
        row['qv']   = '<span class="text-sm" @click="sidebar = 1, dataDetail(\''+str(obj.member.first_name)+'\',\''+url+'\')" >'+arr+'</span>'
        
        
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'project_id' in request.REQUEST:
            project_id = request.REQUEST.get('project_id')
            queryset = queryset.filter(project__id=project_id)

        return queryset
    

class projectGrouplist(AjaxDatatableView):
    model                       = ProjectGroup
    title                       = 'Project Groups'
    show_column_filters         = False
    initial_order               = [["title", "desc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'title', 'visible': True,'className':'text-left' },
        {'name': 'description', 'visible': True,'className':'text-left' },
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''

        url         = reverse('manage_project_group', kwargs=({'pk':obj.id}))
        row['qv']   = '<span class="text-sm" @click="sidebar = 1, dataDetail(\''+str(obj.title)+'\',\''+url+'\')" >'+arr+'</span>'
        
        
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'project_id' in request.REQUEST:
            project_id = request.REQUEST.get('project_id')
            queryset = queryset.filter(project__id=project_id)

        return queryset
    

class ProjectList(AjaxDatatableView):
    model                       = Project
    title                       = 'My Projects'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'title', 'visible': True,'className':'text-left font-semibold cursor-pointer' },
        {'name': 'description', 'visible': True,'className':'text-left ' },
        {'name': 'created_on', 'title':'Created On','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'del','title':'','visible': True, 'className':'w-4 text-left','placeholder':'True','searchable': False,},
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):        
        absolute_url = reverse('project_detail', kwargs=({'pk': obj.id}))
        
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''

        #row['qv']           = '<span class="text-sm" @click="sidebar = true, dataDetail(\''+str(obj.title)+'\',\''+str(obj.id)+'\')" >'+arr+'</span>'
        row['qv']           = '<span class="text-sm">'+arr+'</span>'
        row['title']        = '<a class="" href="'+absolute_url+'">'+str(obj.title)+'</a>'      
        row['created_on']   = naturalday(obj.created_on)        
        row['del']          = '''<svg xmlns="http://www.w3.org/2000/svg" 
                                    class="h-4 w-4 text-slate-300 hover:text-rose-900 hover:cursor-pointer" 
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" 
                                    @click="deleteProject(\'''' + str(obj.id) + '''\')">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>'''
        
        
      
class FormMappingList(AjaxDatatableView):
    model                       = SurveyQuestions
    title                       = 'Form Mapping'
    show_column_filters         = False
    initial_order               = [["order", "asc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'ref', 'visible': True,'className':'text-left cursor-pointer' },
        {'name': 'col_name', 'title': 'Column Name','visible': True,'className':'text-left ' },
        {'name': 'col_type', 'title':'Column Type','visible': True, 'className':'text-left'  },
        {'name': 'label', 'title':'Label','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'options', 'visible': True,'className':'text-left cursor-pointer' },
        {'name': 'hint', 'visible': True,'className':'text-left ' },
        {'name': 'constraints', 'visible': True,'className':'text-left cursor-pointer' },
        {'name': 'required', 'visible': True,'className':'text-left ' },
        {'name': 'order', 'title':'Order','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'page','title':'Page','visible': True, 'className':'w-4 text-left','placeholder':'True','searchable': False,},
    ]
    
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        #row['title'] = '<a href="%s">%s</a>' % (
        #    reverse('event', args=(obj.id,)),
        #    obj.title
        #)
        url = reverse('update_mapping', kwargs=({'pk': obj.id}))
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''

        row['qv']           = '<span class="text-sm" @click="sidebar = true, dataDetail(\''+str(obj.col_name)+'\',\''+url+'\')" >'+arr+'</span>'
         
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'form_id' in request.REQUEST:
            form_id = request.REQUEST.get('form_id')
            queryset = queryset.filter(survey__id=form_id)

        return queryset    
        
      

class formData(AjaxDatatableView):
    model                       = SurveyResponses
    title                       = 'Data'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[9, 50, 100, -1], [9, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'qv','title':'','visible': True, 'className':'w-3 text-left text-rose-800 cursor-pointer','placeholder':'True','searchable': False,},
        {'name': 'instance_id','title':'Instance', 'visible': True,'className':'text-left font-semibold cursor-pointer' },
        #{'name': 'age','title':'Age','visible': True, 'className':'text-left','placeholder':'True','searchable': True,},
        {'name': 'response', 'visible': True,'className':'text-left flex-1' },
        {'name': 'created_on', 'title':'Created On','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'del','title':'','visible': True, 'className':'w-4 text-left','placeholder':'True','searchable': False,},
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        #row['title'] = '<a href="%s">%s</a>' % (
        #    reverse('event', args=(obj.id,)),
        #    obj.title
        #)
        
        
        absolute_url = reverse('instance', kwargs=({'pk': obj.id}))
        
        arr = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>'''
              
        #format json field  
        resp_json   = obj.response
        content     = ''
        count       = 0
        exclude     = ['start','id','end','instanceID']
        for field in resp_json:
            count = count + 1
            if(field not in exclude):
                content += '<span class="font-semibold pr-2">'+field+'</span><span class="pr-2">'+resp_json[field]+'</span>'
            if count == 13:
                break
        

        row['qv']           = '<span class="text-sm" @click="sidebar = true, dataDetail(\''+str(obj.instance_id)+'\',\''+str(obj.id)+'\')" >'+arr+'</span> ddd'
        row['instance_id']  = '<span class="text-sm line-clamp-1" @click="sidebar = true, dataDetail(\''+str(obj.instance_id)+'\',\''+absolute_url+'\')">'+obj.instance_id+'</span>'      
        row['response']     = content
        #row['age']          = obj.response['age']
        row['created_on']   = naturalday(obj.created_on)
        row['del']          = '''<svg xmlns="http://www.w3.org/2000/svg" 
                                    class="h-4 w-4 text-slate-300 hover:text-rose-900 hover:cursor-pointer" 
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" 
                                    @click="discardSignal('+str(obj.id)+')">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>'''
        
                
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'form_id' in request.REQUEST:
            form_id = request.REQUEST.get('form_id')
            queryset = queryset.filter(survey__id=form_id)

        return queryset
 