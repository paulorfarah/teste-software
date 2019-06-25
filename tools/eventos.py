#-*- coding: utf-8 -*-


from uiautomator import device as d


def back():
    # press the menu
    d.press.back()


def click_by_classname_instance(classname, instance):
    if d(className=classname).count > int(instance):
        d(className=classname,instance=int(instance)).click()

def click_by_content_desc(description):
    # check whether the description exists
    if d(description=description).exists:
        d(description=description).click()


def click_by_resource_id(resourceId):
    # check whether the resourceId exists
    if d(resourceId=resourceId).exists:
        d(resourceId=resourceId).click()


def click_by_text(text):
    # check whether the text exists
    if d(text=text).exists:
        d(text=text).click()


def device():
    # press the menu
    print d.info


def down():
    # press the menu
    d.click(50, 50)


def dump(filename):
    # dump ui xml
    d.dump(filename)


def dump_verbose(filename):
    # dump ui xml
    d.dump(filename, False)


def edit_by_classname_instance(className, instance):
    inputs = ["test", "12"]
    if d(className=className).count > int(instance):
        d(className=className,instance=int(instance)).set_text(inputs[random.randint(0, 1)])


def edit_by_content_desc(description):
    # edit text
    inputs = ["test", "12"]
    if d(description=description).exists:
        d(description=description).set_text(inputs[random.randint(0, 1)])


def edit_by_resource_id(resourceId):
    # edit text
    inputs = ["test", "12"]
    if d(resourceId=resourceId).exists:
        d(resourceId=resourceId).set_text(inputs[random.randint(0, 1)])


def edit_by_text(text):
    # edit text
    inputs = ["test", "12"]
    if d(text=text).exists:
        d(text=text).set_text(inputs[random.randint(0, 1)])


def long_click_by_classname_instance(className, instance):
    # long click
    if d(className=className).count > int(instance):
        d(className=className,instance=int(instance)).long_click()

def long_click_by_content_desc(description):
    # check whether the description exists
    if d(description=description).exists:
        d(description=description).long_click()

def long_click_by_resource_id(resourceId):
    # check whether the resourceId exists
    if d(resourceId=resourceId).exists:
        d(resourceId=resourceId).long_click()


def long_click_by_text(text):
    # check whether the text exists
    if d(text=text).exists:
        d(text=text).long_click()


def menu():
    # press the menu
    d.press.menu()


def rotation():
    # dump the orientation
    inputs = ["l", "r", "n"]
    #print d.orientation
    d.orientation = inputs[random.randint(0, 2)]
    #d.orientation = "r"


def rotation_natural():
    # dump the orientation
    #print d.orientation
    if d.orientation != "n":
        d.orientation = "n"


def scroll_by_direction(direction):
    # press the menu
    if direction == 'up':
        d(scrollable=True).scroll.toBeginning()
    elif direction == 'down':
        d(scrollable=True).scroll.toEnd()
    else:
        print "error direction?"


