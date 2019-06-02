import re

from uiautomator import device as d

from eventos import *


# d.screen.off()
# print 'teste'
# d.screen.on()
# print ' teste2'
# d.click(250.0, 360.0)
# print d.info

# def executar():
   # d = Device('Nexus_5x_API_18', adb_server_port=5554)
    #d.screen.on()
    # d.info
    #d.click(350.0, 280.0)
    #d(text="Clock").click()
    #d.screenshot("teste.png")

def parser(action_cmd):
    print action_cmd
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
        # print action_type + action_param + ' ' + action_param_value
        return [action_type + action_param, action_param_value]

    else:
        # execute action by classname and instance
        # exemplo: clickLong(className='android.widget.Button',instance='1'):android.widget.Button@"Jan"

        class_name_pattr = re.compile('className=\'(.*)\',')
        class_name = class_name_pattr.findall(action_cmd)[0]
        instance_pattr = re.compile('instance=\'(.*)\'')
        instance = instance_pattr.findall(action_cmd)[0]
        return [action_type + action_param, class_name, instance]

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

def abrir_app(nome):
    # adb - s
#     # emulator - 5554
#     # shell
#     # am
#     # start - S - n
#     # com.commonsware.android.arXiv / com.commonsware.android.arXiv.arXiv
    print 'nao implementado...'

if __name__ == '__main__':
    f = open('logs/mcmc_all_history_testsuites.txt', 'r')
    f1 = f.readlines()
    for l in f1:
        executar_evento(l)
