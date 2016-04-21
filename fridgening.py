#l07B version
# logs and retrieves messages from db

#the goal is to get server to communicate with the teensy over wifi
#teensy should send post requests in order to send periodic info such as
    # "temp" in degrees F (float)
    # "alert" when temp exceeds threshold (bit)
    # "closed" when limit switch indicates closed fridge door (bit)
    # "resistance" flex sensor readings (float)
#fridgening.py should figure out the time--datetime?

#when we send the response from the server,  it needs opening(`<html>`) and closing HTML tag (`</html>`) 
#displaying the response: parse the html response for relevant text

#key need: a way to distinguish between the teensy and the browser

import _mysql
import cgi
import datetime

exec(open("/var/www/html/student_code/LIBS/s08libs.py").read())
print( "Content-type:text/html\r\n\r\n")


#system specific variables:
site = 'fridgening'# site  name (your kerberos)
users = {'brenda':'bae', 'tina':'bae', 'instructor':'pw'}  #replace with your own user list (eventually)


method_type = get_method_type()
form = cgi.FieldStorage() #get specified parameters!

if method_type == 'POST':

    #GENERAL CONSTRUCTOR FOR DATETIME OBJ = datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    #get current time: 
    currTime = datetime.datetime.now() #currTime is a datetime object of the above format. 
    date = str(currTime.date())
    time = str(currTime.time())
    temp = form.getvalue('temp')
    #define the variables sender, recipient, message for use in the query creation below
    alert = form.getvalue('alert')
    closed = form.getvalue('closed')
    flex_reading = form.getvalue('resistance') #check with brenda about what to call this--perhaps ask if we can change the name of this param in db?
    #connect to database:
    cnx = _mysql.connect(user='student', passwd='6s08student',db='iesc') 
    #create a mySQL query and commit to database relevant information for logging message

    multrecipients = []
    if recipient == "BROADCAST":
        for user in users:
            if user != sender:
                query = ("INSERT INTO messenger (sender, recipient, message, site) VALUES ('%s','%s','%s','%s')" %(sender,user,message,site)) #logs the message
                cnx.query(query)
                cnx.commit()
    else:
        query = ("INSERT INTO messenger (sender, recipient, message, site) VALUES ('%s','%s','%s','%s')" %(sender,recipient,message,site)) #logs the message
        cnx.query(query)
        cnx.commit()
    if teensy != None:
        print("<html>")
        print("</html>")
elif method_type == 'GET':
    teensy = form.getvalue('teensy')
    user =form.getvalue('recipient')
    #connect to database
    cnx = _mysql.connect(user='student', passwd='6s08student',db='iesc') 
    #Create query to database to get all messages meeting certain criteria (to a user and associated with the site
    query = ("SELECT * FROM messenger WHERE recipient='%s' AND site='%s'" %(user,site))
    cnx.query(query)
    result =cnx.store_result()  
    rows = result.fetch_row(maxrows=0,how=0) 
    messages = []
    #generate list of messages (and take care of unicode issues so everything is a Python String)
    for row in rows:
        messages.append([e.decode('utf-8') if type(e) is bytes else e for e in row])
    #print(messages)

    #[['spoop', 'naw', 'hi', '2016-03-15 15:55:06', 'quacht'], ['yeah', 'naw', 'hi', '2016-03-15 15:55:40', 'quacht']]
    if teensy == None:
        print("<ul>\n")
        for message in messages:
            sender = message[0]
            timestamp = message[3]
            f = '%Y-%m-%d %H:%M:%S'
            datetime_msg = datetime.datetime.strptime(timestamp, f)
            now = datetime.datetime.now()
            diff = now- datetime_msg
            limit = datetime.timedelta(minutes=5)

            content = message[2]
            if diff < limit:
                print("<li><b>%s</b> (%s): %s</li>\n" %(sender,timestamp,content)) #wondering if i need to ahve \n at the end 
        print("</ul>\n")
    else:
        print("<html>")
        for message in messages:
            sender = message[0]
            timestamp = message[3]
            f = '%Y-%m-%d %H:%M:%S'
            datetime_msg = datetime.datetime.strptime(timestamp, f)
            now = datetime.datetime.now()
            diff = now- datetime_msg
            limit = datetime.timedelta(minutes=1)

            content = message[2]
            if diff < limit:
                print("%s: %s\n" %(sender,content)) #wondering if i need to ahve \n at the end 
        print('</html>')


