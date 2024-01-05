import pandas
import json

from django.conf import settings
import os


def init_settings(settings):
    setting_map     = {}
    for setting in settings:
        setting_map.update(setting)
            
    return setting_map

def init_choices(choices):
    choice_map = {}
    for choice in choices:
        list_name   = choice['list name']
        if list_name != None:
            list_name = list_name.strip()
            if list_name not in choice_map:
               choice_map[list_name] = []
            tmp = {
                'label' : choice['label'],
                'value' : choice['name'],
            }
            choice_map[list_name].append(tmp)
            
    
    return choice_map
           
def make_jform(survey, choice_map, settings_map):
    survey_map  = {
        "meta": settings_map,
        "pages": {},
        "workflow": {},
    }
    page_count  = 0
    in_group    = False
    for item in survey:
        type    = item['type']
        if type == None:
            continue
        elif type.strip() == 'begin group':
            in_group    = True
            tmp         = item
            tmp['type']     = 'group'
            tmp['fields']   = []
            survey_map['pages'][page_count] = tmp
        elif type.strip() == 'end group':
            in_group    = False,
            page_count = page_count + 1
        else:
            if in_group:
                arr    = item['type'].split()
                item['type']    = arr[0].strip()
                item['val']     = ''
                if len(arr) > 1:
                    if arr[1].strip() in choice_map:
                        key     = arr[1]
                        item['options'] = choice_map[key]
                if len(arr) == 3:
                    if arr[2].strip() == 'or_other':
                        item['or_other']    = '1'
                    else:
                        item['or_other']    = '0'
                survey_map['pages'][page_count]['fields'].append(item)
            else:
                survey_map['pages'][page_count] = {
                    'type'  : 'group',
                    'val'   : '',
                    'fields': [item]
                }
                in_group    = False
                page_count  = page_count + 1
            
    return survey_map
        
def x2jform(filename): 
    
    xlsform             = os.path.join(settings.MEDIA_ROOT, filename)

    try:
        choice_df       = pandas.read_excel(xlsform, sheet_name='choices')
        choice_obj      = json.loads(choice_df.to_json(orient='records'))
        choice_map      = init_choices(choice_obj)

        settings_df     = pandas.read_excel(xlsform, sheet_name='settings')
        settings_obj    = json.loads(settings_df.to_json(orient='records'))
        settings_map    = init_settings(settings_obj)

        survey_df       = pandas.read_excel(xlsform, sheet_name='survey')
        survey_obj      = json.loads(survey_df.to_json(orient='records'))
        survey_map      = make_jform(survey_obj, choice_map, settings_map)
    
        dest            = os.path.join(settings.MEDIA_ROOT, 'jform/defn/',settings_map['form_id']+'.json')
        f = open(dest, "w")
        json.dump(survey_map, f)
        f.close()
        
        return survey_map
    
    except Exception as error:
        print("An exception occurred:", error)
        return 0
    
    
    

