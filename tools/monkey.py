#-*- coding: utf-8 -*-
import subprocess


class Monkey(object):

    def execute(self, params):
        print 'executing monkey tool'
        subprocess.call(
            ["timeout", "1h", "adb", "shell", "monkey", "--throttle", "200", "-p", params[1], "-s", "100",
             "-v", "10", "--ignore-crashes", "--ignore-timeouts"])
