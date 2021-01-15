from headers import *
from driver import loadDriver

driver = loadDriver()
driver.get('https://apps.google.com/meet/')
driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to.window("tab2")
driver.get('https://teams.microsoft.com')