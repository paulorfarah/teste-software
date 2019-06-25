#-*- coding: utf-8 -*-
import random
import logging
import re

from tools.eventos import *


def volume():
    t = random.randint(0, 2)
    # volume up, down, mute
    if t == 0:
        d.press.volume_up()
    elif t == 1:
        d.press.volume_down()
    else:
        d.press.volume_mute()

def parser(action_cmd):
    logging.info(action_cmd)
    action_type = ''
    action_param = ''
    if action_cmd == "menu\n":
        # print 'menu'
        d.press.menu()
    elif action_cmd.__contains__("click("):
        action_type = "click"
    elif action_cmd.__contains__("clickLong("):
        action_type = "long_click"
    elif action_cmd.__contains__("edit("):
        action_type = "edit"
    elif action_cmd.__contains__("scroll("):
        action_type = "scroll"

    if action_cmd.__contains__("(text="):
        action_param = "_by_text"
    elif action_cmd.__contains__("(content-desc="):
        action_param = "_by_content_desc"
    elif action_cmd.__contains__("(resource-id="):
        action_param = "_by_resource_id"
    elif action_cmd.__contains__("direction="):
        action_param = "_by_direction"
    elif action_cmd.__contains__("className=") and action_cmd.__contains__("instance="):
        action_param = "_by_classname_instance"

    if action_param == '':
        return [action_type]
    elif action_param != '_by_classname_instance':
        first_quote_index = action_cmd.index("\'")  # get the action param value
        last_quote_index = action_cmd.rindex("\'")
        # Note we should include the quotes to avoid the existence of whitespaces in the action_param_value
        action_param_value = action_cmd[first_quote_index:last_quote_index]
        # puts "[D]: #{action_type}, #{action_param}, #{action_param_value}"
        print action_type + action_param + ' ' + action_param_value
        return [action_type + action_param, action_param_value]

    else:
        # execute action by classname and instance
        # exemplo: clickLong(className='android.widget.Button',instance='1'):android.widget.Button@"Jan"

        class_name_pattr = re.compile('className=\'(.*)\',')
        class_name = class_name_pattr.findall(action_cmd)[0]
        # instance_pattr = re.compile('instance=\'(.*)\'')
        instance_pattr = re.compile("instance=\'[0-9]+\'")
        instance_number = int(re.findall("(\d+)", instance_pattr.findall(action_cmd)[0])[0])
        # print(matches)
        # print instance_number
        #instance = (instance_pattr.findall(instance_number)[0])#.replace('//', '')
        return [action_type + action_param, class_name, instance_number]


def executar_evento(action_cmd):

    comando = parser(action_cmd)
    if comando[0] == 'back':
        back()
    elif comando[0] == 'click_by_classname_instance':
        click_by_classname_instance(comando[1], comando[2])
    elif comando[0] == 'click_by_content_desc':
        click_by_content_desc(comando[1])
    elif comando[0] == 'click_by_resource_id':
        click_by_resource_id(comando[1])
    elif comando[0] == 'click_by_text':
        click_by_text(comando[1])
    elif comando[0] == 'device':
        device()
    elif comando[0] == 'down':
        down()
    elif comando[0] == 'dump':
        dump(comando[1])
    elif comando[0] == 'dump_verbose':
        dump_verbose(comando[1])
    elif comando[0] == 'edit_by_classname_instance':
        edit_by_classname_instance(comando[1], comando[2])
    elif comando[0] == 'edit_by_content_desc':
        edit_by_content_desc(comando[1])
    elif comando[0] == 'edit_by_resource_id':
        edit_by_resource_id(comando[1])
    elif comando[0] == 'edit_by_text':
        edit_by_text(comando[1])

    elif comando[0] == 'long_click_by_classname_instance':
        long_click_by_classname_instance(comando[1], comando[2])
    elif comando[0] == 'long_click_by_content_desc':
        long_click_by_content_desc(comando[1])
    elif comando[0] == 'long_click_by_resource_id':
        long_click_by_resource_id(comando[1])
    elif comando[0] == 'long_click_by_text':
        long_click_by_text(comando[1])
    elif comando[0] == 'menu':
        menu()
    elif comando[0] == 'rotation':
        rotation()
    elif comando[0] == 'rotation_natural':
        rotation_natural()
    elif comando[0] == 'scroll_by_direction':
        scroll_by_direction(comando[1])
    elif comando[0] == 'volume':
        volume()

class Stoat(object):

    def execute(self, params):
        f = open(params[0], 'r')
        f1 = f.readlines()
        for l in f1:
            executar_evento(l)
        f.close()
