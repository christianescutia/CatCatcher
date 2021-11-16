# Code used to run on a Raspberry Pi

# import needed to connect to postgress server
import psycopg2
import socket
# import needed to find local public IP
from requests import get
# import for email messages
import smtplib
# import for sleep function and threads
from threading import Thread
import time
# import for sms messageing
from twilio.rest import Client

# Global variables
Cage_ID = "CatCage00" # Set Unique per Cage
PORT = '56635'
gmail_user = 'catcatcher.noreply@gmail.com'
gmail_password = 'cat_catcher_2021'
account_sid = 'ACebaf22614c3bf1885d8bb9acf1638ab7'
auth_token = 'f54342d07240369873eddb11dfab5f25'
client = Client(account_sid, auth_token)
TrapTriggered = False


def SendCageInfo(ip):
    # define database connection data
    conn = psycopg2.connect(
        host = "ec2-54-90-13-87.compute-1.amazonaws.com",
        database = "ddg16dt0q9df1t",
        user = "ofxriywaexambz",
        password = "15180294c0a4537da6c6cb7f5ecd6931aa138f1e2968d802268b942554828624",
        port = "5432"
    )

    # create cursor
    c = conn.cursor()

    full_ip = ip + str(':') + str(PORT)

    # add user to database
    sql_command = "INSERT INTO cages ( cage_id, cage_ip) VALUES ( %s, %s)"
    values = (Cage_ID, full_ip)

    # executeb SQL Command
    c.execute( sql_command, values)

    # commit changes
    conn.commit()

    # close database connection
    conn.close()


def CageSensor():
    print('Cage Sensor thread')
    time.sleep(2)
    print('Cage Sensor Complete')

def AppListen():
    print('opening port and listening')
    while True:
        time.sleep(2)
        # next create a socket object
        s = socket.socket()        
        print ("Socket successfully created")
        
        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        port = 55635               
        
        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        s.bind(('', port))        
        print ("socket binded to %s" %(port))
        
        # put the socket into listening mode
        s.listen(5)    
        print ("socket is listening")           
        
        # a forever loop until we interrupt it or
        # an error occurs
        while True:
        
            # Establish connection with client.
            c, addr = s.accept()    
            print ('Got connection from', addr )
            
            # send a thank you message to the client. encoding to send byte type.
            c.send('Thank you for connecting'.encode())
            
            # Close the connection with the client
            c.close()
            
            # Breaking once connection closed
            break



def main():
    print("Hello World!")

    time.sleep(0) # Allow time for wifi to come online

    # Grab the current public ip
    ip = get('https://api.ipify.org').content.decode('utf8')
    print(ip)

    # send current cage data to Heroku Database
    try:
        #SendCageInfo(ip)
        print('test')
    except:
        print("Something went wrong with Database Connection")
    else:
        print("Database Data Sent")

    
    # Create Threads to Check if Cage Activated / Tripped
    #   - Thread to check if user sends message / connects to Pi Remotely
    sensor_thread = Thread(target = CageSensor)
    message_thread = Thread(target = AppListen)
    sensor_thread.start()
    message_thread.start()




if __name__ == "__main__":
    main()