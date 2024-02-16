import requests
import json
import time
import RPi.GPIO as GPIO

# Set the desired pin numbering scheme:
GPIO.setmode(GPIO.BCM)


# GPIO PIN where the LED is connected 
#  pin numbering based on the BCM scheme
LEDPin = 17

# Setup the direction of the GPIO pin - either INput or OUTput 
GPIO.setup(LEDPin, GPIO.OUT)

APIAuthorizationKey = 'Bearer NDdjYzM3NWMtZGVjOS00YTgwLThiZTgtYjUxODAxNGYwOTc4OWUxZTIwYWUtNzIy_PE93_b6f7ca7f-55ce-4df9-855a-8cfebcad253f';

# Using the requests library, create a new HTTP GET Request against the Webex Teams API Endpoint for Webex Teams Rooms:
#  the local object "r" will hold the returned data:
r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers={'Authorization':APIAuthorizationKey}
                )

# Check if the response from the API call was OK (resp. code 200)
if(r.status_code != 200):
    print("Something wrong has happened:")
    print("ERROR CODE: {} \nRESPONSE: {}".format(r.status_code, r.text))
    assert()

# See what is in the JSON data:

jsonData = r.json()

print(
    json.dumps(
        jsonData,
        indent=4
    )
)

rooms = r.json()['items']
for room in rooms:
    print ("Room name: '" + room['title'] + "' ID: " + room['id'])

# Replace contents of this varialble with a real room name from your Webex Teams account
roomNameToSearch = 'test'

# Define a variable that will hold the roomId 
roomIdToMessage = None

rooms = r.json()['items']
for room in rooms:
    #print "Room name: '" + room['title'] + "' ID: " + room['id']
    if(room['title'].find(roomNameToSearch) != -1):
        print ("Found rooms with the word " + roomNameToSearch)
        print ("Room name: '" + room['title'] + "' ID: " + room['id'])
        roomIdToMessage = room['id']
        roomTitleToMessage = room['title']
        break

if(roomIdToMessage == None):
    print("Did not found any room with " + roomNameToSearch + " name in it.")
else:
    print("A valid room has been found and this is the room id: " + roomIdToMessage)

print(roomIdToMessage)

# define the mandatory or optional GET parameters for the `messages` API endpoint:
getMessagesUrlParameters = {
            # mandatory parameter - the room ID
            "roomId": roomIdToMessage,
            # optional parameter - number of the last messages to return
            "max": 8
}

# Using the requests library, create a new HTTP GET Request against the Webex Teams API Endpoint for Webex Teams Messages:
#  the local object "r" will hold the returned data:
r = requests.get(   "https://api.ciscospark.com/v1/messages",
                    params=getMessagesUrlParameters,
                    headers={'Authorization':APIAuthorizationKey}
                )

if(r.status_code != 200):
    print("Something wrong has happened:")
    print("ERROR CODE: {} \nRESPONSE: {}".format(r.status_code, r.text))
    assert()

# See what is in the JSON data:

jsonData = r.json()

print(
    json.dumps(
        jsonData,
        indent=4
    )
)

messages = jsonData['items']
for message in messages:
    print("Message: " + message['text'])
    if(message['text'] == '/Turn On'):
        messageId = message['id']
        print("Found a command message to TURN ON the LED!")
        break
    if(message['text'] == '/Turn Off'):
        messageId = message['id']
        print("Found a command message to TURN OFF the LED!")
        break

lastMessageId = None

while True:
    # the code should not hammer the API service with too many reqeuests in a short time
    #  to limit the number of requests in the while loop, begin with a short 1 second delay:
    time.sleep(1)
    print("Next iteration is starting ...")
    
    # define the mandatory or optional GET parametrs for the `messages` API endpoint:
    getMessagesUrlParameters = {
                # mandatory parameter - the room ID
                "roomId": roomIdToMessage,
                # optional parameter - number of the last messages to return
                #  only interested in the very last message in the room
                #   thefore max = 1
                "max": 1
    }

    # Using the requests library, creare a new HTTP GET Request against the Webex Teams API Endpoint for Webex Teams Messages:
    #  the local object "r" will hold the returned data:
    r = requests.get(   "https://api.ciscospark.com/v1/messages",
                        params=getMessagesUrlParameters,
                        headers={'Authorization':APIAuthorizationKey}
                    )
    if(r.status_code != 200):
        print("Something wrong has happened:")
        print("ERROR CODE: {} \nRESPONSE: {}".format(r.status_code, r.text))
        assert()
    
    
    # Store the json data from the reply
    jsonData = r.json()
    
    # Get the items (array of messages) from the jsonData.
    messages = jsonData['items']

    if(messages):
    # since the request specified max=1, only one message should be returned:
        message  = messages[0]
    else : continue
    # Verify if this is a new message:
    if(lastMessageId == message['id']):
        #this is the same message as before, no new messages
        print("No New Messages.")
    else:
        # this is a new message, its ID is different from the one in the previous iteration
        print("New Message: " + message['text'])
        # save the message id for the next iteration:
        lastMessageId = message['id']
        if(message['text'] == '/Turn On'):
            messageId = message['id']
            print("Found a command message to TURN ON the LED!")
            # Turn on the LED:
            GPIO.output(17, True)
            #break
        if(message['text'] == '/Turn Off'):
            messageId = message['id']
            print("Found a command message to TURN OFF the LED!")
            # Turn off the LED:
            GPIO.output(17, False)
            #break