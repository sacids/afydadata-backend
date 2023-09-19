from django import template
register = template.Library()



@register.filter(name='make_title')
def make_title(value):
    return value.replace("_"," ").lower().title()




@register.filter(name='get_value')
def get_value(value,args):
    tmp     = value.get(args)
    #if tmp is not None:
    #    tmp = tmp.replace(" ",", ")
    #    tmp = tmp.replace("_", " ")
    return tmp