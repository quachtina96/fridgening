import _mysql
import cgi

#browser based interface to fridge monitoring ecosystem 

#the code below contained within the variable body is the html/css/javascript for creating the GUI part and functionality
# behind the fridge monitoring app. We print this string below with critical values like the user list, and other things inserted
# into the string using string formatting (find the %s !). YOU DO NOT NEED TO UNDERSTAND HOW THIS CODE WORKS, ONLY WHAT IT DOES:

# On loading it creates a page that has field for selecting a user (to receive a message), a message field, a submit button, and a 
# field to display received messages.  

#When Submit is pressed, a POST is sent to a message.py file which interacts with the database for
# logging the message.  

#Every 1 second, the code also runs a GET request on message.py to retrieve any messages associated with the user
# It then displays these messages inside its maroon box at the bottom.
body = '''<heading>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {

clearIt = function(){
    console.log("sending message");
    console.log($("#message").val());
    console.log($("#recipient").val());
    $.ajax({
        url: 'http://iesc-s2.mit.edu/student_code/%s/lab07/message.py/',
        method:"POST",
        type:"POST",
        data: "recipient="+$('#recipient option:selected').text()+"&message="+$("#message").val()+"&sender=%s",
        success: function(data){
            $("#message").val("");
            console.log(data);
        },
    });
};

$("#send").click(function(){
    console.log("clicked");
    clearIt();
});

function periodicMessageUpdate(){
    console.log("requesting");
    $.ajax({
        url: 'http://iesc-s2.mit.edu/student_code/%s/lab07/message.py',
        data: "recipient=%s",
        success: function(data){
            console.log(data);
            $("#display").html(decodeURI(data));
        },
        complete: function(){
            setTimeout(periodicMessageUpdate,1000);
        }
    });
};
all_users = %s;
$.each(all_users, function(key, value) {   
     $('#recipient')
          .append($('<option>', { value : key })
          .text(key)); 
});

setTimeout(periodicMessageUpdate,1000);
});
</script>
</heading>
<style>
#display {
    border-radius: 25px;
    border: 2px solid #9A004B;
    padding: 20px; 
    width: 450px;
    height: auto;    
}
</style>
<body>

<h1>6.S08 Messager</h1>
  Send To:
    <select name="recipient" id="recipient">
        <option value=" " selected> </option>
        <option value="broadcast" >BROADCAST</option>
    </select>
    <br>
  Message:
  <input type="text" id="message" value=""><br>
  <button type="button" id="send">Send!</button>
<p><div id="display">
</div>

</body>'''

exec(open("/var/www/html/student_code/LIBS/s08libs.py").read())

#system specific variables:

site = 'quacht' #replace with your own kerberos (eventually)
users = {'spoop':'fam', 'yeah':'bage', 'naw':'bih'}  #replace with your own user list (eventually)

#put your users here (dictionary of key=username, value=password) DO NOT USE PASSWORDS YOU NORMALLY USE! 

# Do some HTML formatting at the very top!
print( "Content-type:text/html\r\n\r\n")
print('<html>')

method_type = get_method_type() #use this for figuring out if it is a GET or POST!
form = cgi.FieldStorage() #get specified parameters!

if method_type == "GET": #expecting a GET request.
    if 'username' in form.keys() and 'password' in form.keys():
        username = form['username'].value
        password = form['password'].value
        if users[username] != password:
            print('Sorry :( %s. Your password is not correct. Consult your administrator.' %(username))
        else:
            print(body %(site,username,site,username,str(users)))
    else:
        print("You need to specify a user name an password as GET parameters")
    
print('</html>')

