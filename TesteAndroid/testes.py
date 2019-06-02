from uiautomator import device as d


d.screen.off()
print 'teste'
d.screen.on()
print ' teste2'
d.click(250.0, 360.0)
print d.info