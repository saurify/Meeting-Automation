from headers import *
from driver import teamsproxy, meetproxy                        #functions that joion the classes

timings = []                                                    #stores time for every class                
daywise_classes = []                                            # nested list contaning all classes


def process():                                                  #preprocess data from xls file
    df = pd.read_excel(r'Calendar.xls')                         #reading schedule from excel file
    timings[:] = [str(i)[:-3] for i in df][1:]                  #reading timings for classes

    for _ in df.itertuples():
        temp = []
        for i in _[2:]:
            if i==i: temp.append(i)
            else: temp.append('0')
        daywise_classes.append(temp)                             #making nested list of classes


def manage():                                                    #schedules classes
    daily = len(timings)

    for i in range(daily):                                       #sceduling for monday       
            if (i+1)<daily and daywise_classes[0][i]==daywise_classes[0][i+1]: schedule.every().monday.at(timings[i]).do(join, daywise_classes[0][i],2)
            else: schedule.every().monday.at(timings[i]).do(join, daywise_classes[0][i],1)
            
    for i in range(daily):                                       #sceduling for tuesday
        if (i+1)<daily and daywise_classes[1][i]==daywise_classes[1][i+1]: schedule.every().tuesday.at(timings[i]).do(join, daywise_classes[1][i],2)
        else: schedule.every().tuesday.at(timings[i]).do(join, daywise_classes[1][i],1)
    
    for i in range(daily):                                       #sceduling for wednesday
        if (i+1)<daily and daywise_classes[2][i]==daywise_classes[2][i+1]: schedule.every().wednesday.at(timings[i]).do(join, daywise_classes[2][i],2)
        else: schedule.every().wednesday.at(timings[i]).do(join, daywise_classes[2][i],1)

    for i in range(daily):                                       #sceduling for thursday
        if (i+1)<daily and daywise_classes[3][i]==daywise_classes[3][i+1]: schedule.every().thursday.at(timings[i]).do(join, daywise_classes[3][i],2)
        else: schedule.every().thursday.at(timings[i]).do(join, daywise_classes[3][i],1)
    
    for i in range(daily):                                       #sceduling for friday
        if (i+1)<daily and daywise_classes[4][i]==daywise_classes[4][i+1]: schedule.every().friday.at(timings[i]).do(join, daywise_classes[4][i],2)
        else: schedule.every().friday.at(timings[i]).do(join, daywise_classes[4][i],1)


def join(link, duration):                                        #function that decides and calls proxy function
    print("starting")
    if 'teams' in link: teamsproxy(link, duration*60)            #passing duration of classes in seconds   
    if 'meet' in link: meetproxy(link, duration*60)                 
    if link=='0' : print(f'No classes now {str(time.localtime())}')


process()
print(timings)
print(daywise_classes)
manage()

while True: 
    schedule.run_pending()
    time.sleep(1)
