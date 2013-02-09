# takes a reddit link URL (the one that shows comments for the post) and
# outputs a Gource custom log file for visualization of comment structure

import json
import urllib.request
import time

LAST_API_CALL = int(time.time())

def api_get_json(url):

    global LAST_API_CALL
    call_time = int(time.time())
    if call_time - LAST_API_CALL < 5:
        time.sleep(5)
 
    print("Making API call to " + url)
    
    url_request = urllib.request.Request(url)
    url_request.add_header("User_Agent", "Gource vis, kdbanman")

    response = ""
    while response == "":
        try:
            response = urllib.request.urlopen(url_request)
            print("WTFBALLS??")
        except urllib.error.HTTPError:
            print("AAAAHHHHH")
            time.sleep(35)
            print("HTTP Error, Trying API call again.")
            response = ""
        
    LAST_API_CALL = int(time.time())
    response_lines = response.readlines()
    
    raw_json = ""
    for line in response_lines:
        raw_json += line.decode("utf8")

    return json.loads(raw_json)
    

def api_get_comment(comment_id, root_id):
    url = "http://www.reddit.com/comments/" + root_id + "/_/" + comment_id\
            + ".json"
    encoded = api_get_json(url)
    ##DEBUG
    while "error" in encoded:
        time.sleep(35)
        encoded = api_get_json(url)

    try:
        comment = encoded[1]["data"]["children"][0]
    except IndexError:
        return None
    
    return comment

def recur_print(comment, path, file):
    
    # we want to treat the comment's "data" dictionary as the comment itself
    # if not all comments were retrieved, use API calls to get them
    if comment["kind"] == "more":
        comment_id = comment["data"]["id"]
        root_id = path.split("/")[0]
        comment = api_get_comment(comment_id, root_id)

    if comment != None:

        comment = comment["data"]

        timestamp = str(int(comment["created_utc"]))
        user = comment["author"]
        if comment["id"] != path:
            path = path + "/" + comment["id"]
        edited = str(comment["edited"])

        ##DEBUG
        if type(timestamp) != type(""):
            print("timestamp not string type")
        if type(user) != type(""):
            print("user not string type")
        if type(path) != type(""):
            print("path not string type")
        if type(edited) != type(""):
            print("edited not string type")

        has_replies = comment["replies"] != ""
        if has_replies:
            ##DEBUG
            print(path + " HAS REPLIES")
            reply_list = comment["replies"]["data"]["children"]
        
            for reply in reply_list:
                recur_print(reply, path, file)

        file.write(timestamp + "|" + user + "|A|" + path + "\n")
    
    else:
        print("Blank thing found at path " + path)
        

url_input = input("URL: ")
output_name = input("Output: ")

# assumes url is valid http, and points to a reddit link page
url_ready = url_input + ".json"

url_request = urllib.request.Request(url_ready)
url_request.add_header("User_Agent", "Gource vis user kdbanman")
response = urllib.request.urlopen(url_request)
time.sleep(5)
response_lines = response.readlines()

raw_json = ""
for line in response_lines:
    raw_json += line.decode("utf8")

encoded = json.loads(raw_json)
link_dict = encoded[0]["data"]["children"][0]
comment_dict = encoded[1]
# merge the two dictionaries to be a consistent tree with the link as the root
link_dict["data"]["replies"] = comment_dict
root_id = link_dict["data"]["id"]

outputfile = open(output_name + ".log", "w")
recur_print(link_dict, root_id, outputfile)
outputfile.close()
