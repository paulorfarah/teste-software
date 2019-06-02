import os,sys, commands, shutil
from subprocess import Popen, PIPE
import share
from uiautomator import Device
import uiautomator
import time, subprocess, signal

#dir = '/home/fanlingling/Desktop/crash_analysis/tool_data/test_stoat/'
output_dir = '/home/lingling/Desktop/reproduce_info/stoat/'
apk_dir1 = '/home/lingling/Desktop/fdroid_apks_versionCode/'
apk_dir2 = '/home/lingling/Desktop/fdroid-apks/'

unknown_event = '/home/lingling/Desktop/unknown_events.txt'

dir = sys.argv[1]
emulator = sys.argv[2]
l = sys.argv[3]
#emulator = '0140a4a70b9437d7'
d = Device(emulator)
def parse(cmd):
    #print cmd
    if cmd.startswith('back') or cmd.startswith('keyevent_back'):
        d.press.back()
    elif cmd.startswith('menu'):
        d.press.menu()
    elif cmd.startswith('scroll(direction=\'up\')'):
        d(scrollable=True).scroll(steps=10)
    elif cmd.startswith('scroll(direction=\'down\')'):
        d(scrollable=True).fling.vert.backward()
    elif cmd.startswith('['):
        activity = cmd.split('\', \'')[-1].split('\']')[0]
        print activity
        os.system('adb -s %s shell am start -n %s'%(emulator, activity))
    elif cmd.startswith('clickLong'):
        # clickLong(className='android.widget.Button',instance='0')@0
        if 'className' in cmd:
            clsname = cmd.split("className='")[1].split("'")[0]
            instance = cmd.split("instance='")[1].split("'")[0]
            d(className=clsname, instance=instance).long_click()
        
        # clickLong(resource-id='at.bitfire.davdroid:id/show_password')@0
        elif 'resource-id' in cmd:
            id = cmd.split("resource-id='")[1].split("'")[0]
            d(resourceId=id).long_click()
        
        # clickLong(textContains='Zoom 11')@0
        elif 'textContains' in cmd:
            text = cmd.split("textContains='")[1].split("'")[0]
            d(textContains=text).long_click()
        
        # clickLong(content-desc='Open navigation drawer')@0
        elif 'content-desc' in cmd:
            content = cmd.split("content-desc='")[1].split("'")[0]
            d(description=content).long_click()

elif cmd.startswith('click('):
    #click(className='android.widget.Button',instance='0')@0
    if 'className' in cmd:
        clsname = cmd.split("className='")[1].split("'")[0]
            instance = cmd.split("instance='")[1].split("'")[0]
            d(className=clsname,instance=instance).click()
        
        #click(resource-id='at.bitfire.davdroid:id/show_password')@0
        elif 'resource-id' in cmd:
            id = cmd.split("resource-id='")[1].split("'")[0]
            d(resourceId=id).click()

    #click(textContains='Zoom 11')@0
    elif 'textContains' in cmd:
        text = cmd.split("textContains='")[1].split("'")[0]
            d(textContains=text).click()
        
        #click(content-desc='Open navigation drawer')@0
        elif 'content-desc' in cmd:
            content = cmd.split("content-desc='")[1].split("'")[0]
            d(description=content).click()

elif cmd.startswith('edit'):
    txt = cmd.split('@')[1]
        # edit(className='android.widget.Button',instance='0')@0
        if 'className' in cmd:
            clsname = cmd.split("className='")[1].split("'")[0]
            instance = cmd.split("instance='")[1].split("'")[0]
            d(className=clsname, instance=instance).set_text(txt)

    # edit(resource-id='at.bitfire.davdroid:id/show_password')@0
    elif 'resource-id' in cmd:
        id = cmd.split("resource-id='")[1].split("'")[0]
            d(resourceId=id).set_text(txt)

else:
    print 'unknown event----------%s-------------'%cmd
        open(unknown_event,'ab').write('unknown event: '+cmd + '\n')


def run_uiautomator(bug_path):
    print 'uiaumator...'
    cmds = open(bug_path, 'rb').readlines()
    os.system('adb -s %s logcat -c'%emulator)
    log_filter = 'AndroidRuntime:E CrashAnrDetector:D ActivityManager:E SQLiteDatabase:E ' \
        'WindowManager:E ActivityThread:E Parcel:E *:F *:S'
    pro = subprocess.Popen('adb -s %s logcat -v brief %s >> %s' % (emulator, log_filter, log),
                           stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
#os.system('adb -s %s logcat -v brief %s >> %s &' % (emulator, log_filter, log))
#d(className='android.widget.Button',instance='0').click()

for cmd in cmds:
    try:
        parse(cmd.strip())
        except uiautomator.JsonRPCError:
            print 'parse error event: %s' % cmd
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def reproduce(apk_path, bug_path):
    for i in range(0, 5):
        share.uninstallAPK(apk_path, emulator)
        share.installAPK(apk_path, emulator)
        share.startApp(apk_path, emulator)# start launch activity
        run_uiautomator(bug_path)
    share.uninstallAPK(apk_path, emulator)
    os.system('adb -s %s shell rm /data/app/*.apk' % (emulator))

def create_avd(avd_name="testAVD_1", sdk_version="android-18"):
    
    # check whether #avd_name already exist?
    res = commands.getoutput("android list avd | grep #{avd_name}")
    
    if not res == '': # if exist and forced to create a new one, delete it
        os.system("kill -9 `ps | grep qemu-system | awk '{print $1}'`")  # make sure the avd is stopped
        os.system("android delete avd -n %s"%avd_name)
    time.sleep(1)  # wait a while

# create the avd
os.system("echo no | android create avd -n %s -t %s -c 512M -b x86 -s WXGA800-7in"%(avd_name, sdk_version))
    time.sleep(2)
def getapkname(pro):
    if pro.endswith('-output'):
        apk = pro.split('-output')[0]+'.apk'
        type = 'hash'
    else:
        apk = pro.split('_')[0] + '_' + pro.split('_')[1] + '.apk'
        type = 'pkgname'
    return apk, type

if __name__ == '__main__':
    
    #create_avd()
    lines = open(l, 'rb').readlines()
    for pro in lines:
        if os.path.exists(output_dir + pro):
            shutil.rmtree(output_dir + pro)
        pro = pro.strip()
        print '------------%s----------------' % pro
        pro_path = dir + pro
        if os.path.isdir(pro_path):
            os.chdir(pro_path)
            uniq = commands.getoutput("find . -name unique").split("\n")[0]
            bug_d = pro_path + '/' + uniq + '/'
            for bug in os.listdir(bug_d):
                bug_dir = bug_d + bug
                apk, type = getapkname(pro)
                share.mkdir(output_dir + pro)
                log = output_dir + pro + '/' + bug + '.log'
                if type == 'hash':
                    reproduce(apk_dir2 + apk, bug_dir + '/bug_event_trace.txt')
                else:
                    reproduce(apk_dir1 + apk, bug_dir + '/bug_event_trace.txt')


