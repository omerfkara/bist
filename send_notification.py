from plyer import notification


import time

#Use while loop to create notifications indefinetly
#while(True):
    #notification
notification.notify(
    title = "Reminder to take a break",
    message = '''Drink water, take a walk''',
    timeout = 60
)
    #System pause the execution of this programm for 60 minutes
#    time.sleep(60*60)

