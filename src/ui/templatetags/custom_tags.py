from django import template

register = template.Library()
from django.utils.html import mark_safe

import json
import ast


@register.filter(name="make_title")
def make_title(value):
    return value.replace("_", " ").lower().title()


@register.filter(name="get_value")
def get_value(value, args):
    tmp = value.get(args)
    # if tmp is not None:
    #    tmp = tmp.replace(" ",", ")
    #    tmp = tmp.replace("_", " ")
    return tmp


import mimetypes

mimetypes.init()


@register.filter(name="getMediaFile")
def getMediaFile(fileName, dir):
    # print(fileName)
    mimestart = mimetypes.guess_type(fileName)[0]

    if mimestart != None:
        mimestart = mimestart.split("/")[0]

        if mimestart == "audio":
            return (
                '<audio controls><source src="/' + dir + "/" + fileName + '"></audio>'
            )
        elif mimestart == "image":
            return '<img src="/' + dir + "/" + fileName + '" class="w-full">'
        elif mimestart == "video":
            return (
                '<video controls><source src="/' + dir + "/" + fileName + '"></video>'
            )
        else:
            return "<div>Not supported</div>"

    return False


@register.filter(name="get_view")
def get_view(value, col_name):
    cn = value.response[col_name]
    loc = " ".join(cn.split(" ", 2)[:-1])
    gps = "[" + loc.replace(" ", ", ") + "]"
    return gps


@register.filter(name="get_location")
def get_location(value, col_name):
    cn = value.response[col_name]
    loc = " ".join(cn.split(" ", 2)[:-1])
    gps = "[" + loc.replace(" ", ", ") + "],{ id: '" + str(value.id) + "'}"
    return mark_safe(gps)


@register.filter(name="perm_selected")
def perm_selected(value, arr):
    # print(arr)
    if value.id in arr:
        return "selected"


@register.filter(name="data_header")
def data_header(value):

    col_name = "<th>" + value.col_name + "</th>"
    if value.label is not None:
        # json_data = ast.literal_eval(value.label)
        # for k,v in json_data.items():
        # print(k+' - '+v)

        col_name = "<th>" + value.label + "</th>"

    if value.col_type == "select":
        json_data = ast.literal_eval(value.options)
        for k, v in json_data.items():
            for i in v:
                col_name += "<th>" + i + "</th>"
            break

    return mark_safe(col_name)


@register.filter(name="jdata_header")
def jdata_header(value):

    col_name = "<th>" + value["name"] + "</th>"

    if value["type"] in ["select_one", "select", "rank"]:
        # json_data = ast.literal_eval(value['options'])
        # print(value["options"])
        for opt in value["options"]:
            print(opt["label"])
            col_name += "<th>" + opt["label"] + "</th>"
            break

    return mark_safe(col_name)
