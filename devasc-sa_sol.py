###############################################################
# INSTRUCTOR NOTE:
#  To demonstrate or test this program, hard-code your
#  Webex and MapQuest keys in steps 2 and 6.
###############################################################
# This program:
# - Asks the user to enter an access token or use the hard coded access token.
# - Lists the user's Webex Teams rooms.
# - Asks the user which Webex Teams room to monitor for "/location" requests.
# - Monitors the selected Webex Team room every second for "/location" messages.
# - Discovers GPS coordinates for the "location" using MapQuest API.
# - Discovers the date and time of the next ISS flyover over the "location" using the ISS API
# - Formats and sends the results back to the Webex Team room.
#
# The student will:
# 1. Import libraries for API requests, JSON formatting, and epoch time conversion.
# 2. Complete the if statement to ask the user for the Webex access token.
# 3. Provide the URL to the Webex Teams room API.
# 4. Create a loop to print the type and title of each room.
# 5. Provide the URL to the Webex Teams messages API.
# 6. Provide your MapQuest API consumer key.
# 7. Provide the URL to the MapQuest address API.
# 8. Provide the MapQuest key values for latitude and longitude.
# 9. Provide the URL to the ISS pass times API.
# 10. Provide the ISS key values risetime and duration.
# 11. Convert the risetime epoch value to a human readable date and time.
# 12. Complete the code to format the response message.
# 13. Complete the code to post the message to the Webex Teams room.
###############################################################
 


#######################################################################################
# 1. Import libraries for API requests, JSON formatting, and epoch time conversion.

import requests
import json
import time

#######################################################################################
# 2. Complete the if statement to ask the user for the Webex access token.
#     Ask the user to use either the hard-coded token (access token within the code)
#     or for the user to input their access token.
#     Assign the hard-coded or user-entered access token to the variable accessToken.

choice = input("Do you wish to use the hard-coded Webex token? (y/n) ")

if choice == "N" or choice == "n":
	accessToken = input("What is your access token? ")
	accessToken = "Bearer " + accessToken
else:
    accessToken = "Bearer <!!!REPLACEME with hard-coded token!!!>"

#######################################################################################
# 3. Provide the URL to the Webex Teams room API.
#     Using the requests library, create a new HTTP GET Request to the Webex Teams API 
#     endpoint for Webex Teams Rooms. The local object "r" will hold the returned data.

r = requests.get(   "https://webexapis.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )
#######################################################################################
# DO NOT EDIT ANY BLOCKS WITH r.status_code
if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

#######################################################################################
# 4. Create a loop to print the type and title of each room.
#     Displays a list of rooms.

print("List of rooms:")
rooms = r.json()["items"]
for room in rooms:
    print ("Type: " + room["type"] + ", Name: " + room["title"])

#######################################################################################
# SEARCH FOR WEBEX TEAMS ROOM TO MONITOR
#  - Searches for user-supplied room name.
#  - If found, print "found" message, else prints error.
#  - Stores values for later use by bot.
# DO NOT EDIT CODE IN THIS BLOCK
#######################################################################################

while True:
    # Input the name of the room to be searched 
    roomNameToSearch = input("Which room should be monitored for /location messages? ")

    # Defines a variable that will hold the roomId 
    roomIdToGetMessages = None
    
    for room in rooms:
        # Searches for the room "title" using the variable roomNameToSearch 
        if(room["title"].find(roomNameToSearch) != -1):

            # Displays the rooms found using the variable roomNameToSearch (additional options included)
            print ("Found rooms with the word " + roomNameToSearch)
            print(room["title"])

            # Stores room id and room title into variables
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room : " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, I didn't find any room with " + roomNameToSearch + " in it.")
        print("Please try again...")
    else:
        break

######################################################################################
# WEBEX TEAMS BOT CODE
#  Starts Webex bot to listen for and respond to /location messages.
######################################################################################

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                         }
# 5. Provide the URL to the Webex Teams messages API.
    # Send a GET request to the Webex Teams messages API.
	# - Use the GetParameters to get only the latest message.
	# - Store the message in the "r" variable.
    r = requests.get("https://webexapis.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    # get the JSON formatted returned data
    json_data = r.json()
    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")
    
    # store the array of messages
    messages = json_data["items"]
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)
    
    # check if the text of the message starts with the magic character "/" followed by a location name
    #  e.g.  "/San Jose"
    if message.find("/") == 0:
        # name of a location (city) where we check for GPS coordinates using the MapQuest API
        #  message[1:]  returns all letters of the message variable except the first "/" character
        #   "/San Jose" is turned to "San Jose" and stored in the location variable
        location = message[1:]
        
# 6. Provide your MapQuest API consumer key.
        # MapQuest API GET parameters:
        # - "location" is the the location to lookup
        # - "key" is the Consumer Key you generated at https://developer.mapquest.com/user/me/apps
        mapsAPIGetParameters = { 
                                "location": location, 
                                "key": "<!!!REPLACEME with your MapQuest API Key!!!>" # MapQuest API key here
                               }
# 7. Provide the URL to the MapQuest address API.
        # Get location information using the MapQuest API geocode service using the HTTP GET method
        r = requests.get("https://www.mapquestapi.com/geocoding/v1/address?", 
                             params = mapsAPIGetParameters
                        )
        # Verify if the returned JSON data from the MapQuest API service are OK
        json_data = r.json()
        # check if the status key in the returned JSON data is "0"
        if not json_data["info"]["statuscode"] == 0:
            raise Exception("Incorrect reply from MapQuest API. Status code: {}".format(r.statuscode))

        # store the location received from the MapQuest API in a variable
        locationResults = json_data["results"][0]["providedLocation"]["location"]
        # print the location address
        print("Location: " + locationResults)

# 8. Provide the MapQuest key values for latitude and longitude.
        # Set the lat and lng key as retuned by the MapQuest API in variables
        locationLat = json_data["results"][0]["locations"][0]["displayLatLng"]["lat"]
        locationLng = json_data["results"][0]["locations"][0]["displayLatLng"]["lng"]
        # print the location address
        print("Location GPS coordinates: " + str(locationLat) + ", " + str(locationLng))

        # ISS flyover Documentation: http://open-notify-api.readthedocs.io/en/latest/iss_pass.html
        # the ISS flyover API GET parameters
        #  "lat" is the latitude of the location
        #  "lon" is the longitude of the location
        issAPIGetParameters = { 
                                "lat": locationLat, 
                                "lon": locationLng
                              }
# 9. Provide the URL to the ISS pass times API.
        # Get IIS flyover information for the specified GPS coordinates.
        r = requests.get("http://api.open-notify.org/iss-pass.json", 
                             params = issAPIGetParameters
                        )
        # Format the returned data as JSON.
        json_data = r.json()
        # Verify the returned JSON data containes the response key. If not, display error.
        if not "response" in json_data:
            raise Exception("Incorrect reply from open-notify.org API. Status code: {}. Text: {}".format(r.status_code, r.text))

# 10. Provide the ISS key values risetime and duration.
        # Store the risetime and duration of the first flyover in variables.
        risetimeInEpochSeconds = json_data["response"][0]["risetime"]
        durationInSeconds      = json_data["response"][0]["duration"]

# 11. Convert the risetime epoch value to a human readable date and time.
        # Use the time.ctime function to convert the risetime to a human readable date and time.
        risetimeInFormattedString = str(time.ctime(risetimeInEpochSeconds))

# 12. Complete the code to format the response message.
#     Example responseMessage result: In Austin, Texas the ISS will fly over on Thu Jun 18 18:42:36 2020 for 242 seconds.
        responseMessage = "In {} the ISS will fly over on {} for {} seconds.".format(locationResults, risetimeInFormattedString, durationInSeconds)
        # print the response message
        print("Sending to Webex Teams: " +responseMessage)

# 13. Complete the code to post the message to the Webex Teams room.         
        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        HTTPHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        # The Webex Teams POST JSON data
        # - "roomId" is is ID of the selected room
        # - "text": is the responseMessage assembled above
        PostData = {
                            "roomId": roomIdToGetMessages,
                            "text": responseMessage
                        }
        # Post the call to the Webex Teams message API.
        r = requests.post( "https://webexapis.com/v1/messages", 
                              data = json.dumps(PostData), 
                              headers = HTTPHeaders
                         )
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


    
