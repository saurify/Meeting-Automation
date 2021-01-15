from headers import *
timeout = 10                                                    #default timeout for each load


def loadDriver():                                               #loading selenum driver
    option = Options()
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 
    })
    option.add_experimental_option("detach", True)
    option.add_argument("--user-data-dir=selenium")
    driver = webdriver.Chrome("./chromedriver.exe" , options = option)

    return driver


def leaveteams(driver, duration):                               #leaves meeting after set duration
    sleep(1)
    curr = time.time()
    temp = time.time() 
    cutoff = 60*10                                              #cutoff time
    sleep(5)

    #disabling the css on toggle menu
    driver.execute_script("var element = document.getElementsByClassName('ts-calling-unified-bar-container')[0];element.classList.remove('ts-calling-unified-bar-container'); ")

    roster = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CLASS_NAME,'toggle-roster')))
    roster.click()
    
    print("Time before leaving: ", str(duration))
    
    while temp - curr < duration :                              #loop while total time in meeting is less than total duration
        temp =time.time()
        
        try:
            num = driver.find_elements_by_class_name('toggle-number')[1].text.split('(')[1].split(')')[0]
            print("people in MEETING: ", num)
            if(int(num)<5 and temp - curr >= cutoff ): break    #if less than 5 people in meeting for 10 mins, then leave the meating 
        except:
            roster = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CLASS_NAME,'toggle-roster')))
            roster.click()

        sleep(20)                                               #updating every 20 seconds
    
    sleep(1)    
    driver.quit()


def teamsproxy(link, duration):
    driver = loadDriver()
    driver.get(link)
    
    try:                                                         #locating join button for meeting 
        join_buttons = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ts-calling-join-button")))      
        sleep(1)
        join_buttons[-1].click()
    except TimeoutException:
        print("Timed out while waiting to fing join button")
    finally:
        print("Joining")

    try:                                                         #toggling the video and mic switches and joining the meeting room                                            
        toggle_buttons = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ts-toggle-button")))      
        if 'OFF' in toggle_buttons[0].get_attribute('track-summary'): toggle_buttons[0].click()
        if 'OFF' in toggle_buttons[1].get_attribute('track-summary'): toggle_buttons[1].click()
        sleep(1)
        fjoin = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "join-btn")))
        fjoin.click()
    except:
        print("Error while toggling the audio-video switches")
    finally:
        print("Joined")
        leaveteams(driver,duration)


def leavemeet(driver, duration):
    sleep(1)
    curr =time.time()
    cutoff = 60*15
    print("Time before leaving: ", str(duration))
    while 1:
        temp =time.time()
        print("people in MEETING: ", driver.find_element_by_class_name('wnPUne').text)

        if(temp-curr >= duration):
            break
        if(int(driver.find_element_by_class_name('wnPUne').text)<5 and temp-curr >= cutoff ):
            break
        sleep(20)
    sleep(1)    
    driver.quit()


def meetproxy(link, duration):
    print('Almost Done!!')
    driver = loadDriver()
    driver.get(link)
    sleep(8)
    try:
        if 'off' in driver.find_elements_by_class_name('JRY2Pb')[1].get_attribute('aria-label'):
            driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'e')
        sleep(1)
        if 'off' in driver.find_elements_by_class_name('JRY2Pb')[0].get_attribute('aria-label'):
            driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'd')
        sleep(3)
        try:
            driver.find_element_by_class_name('Y5sE8d').click()
        except:
            try:
                driver.find_element_by_class_name('M9Bg4d').click()
            except:
                print("Error thrown cannot join!")
                driver.quit()
                return -1
        sleep(1)
        leavemeet(driver,duration)
        
    except:
        print("Error thrown Google meet not loaded!")
        driver.quit()
        return -1 

############IGNORE############
'''
tlink = input()
dur = 300 #seconds
teamsproxy(tlink, dur)
'''