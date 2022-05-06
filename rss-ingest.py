# RSS feed pull and transform to JSON; POC is CISA Alerts RSS feed
# Requires the 'feedparser' library
# Last updated 5/5/2022 MTG

# Get necessary libraries
import feedparser  # https://feedparser.readthedocs.io/en/latest/
import json  # https://docs.python.org/3/library/json.html
import sys  # https://docs.python.org/3/library/sys.html

# Set necessary variables
feedUrl = 'https://www.cisa.gov/uscert/ncas/alerts.xml'  # RSS feed to pull down
outFile = 'outfile.json'  # Output file for JSON events
alertTracker = 'alert-tracker.txt'  # State file to track already received events (alerts)

def feed_work(feedUrl):
    '''
    The 'feed_work' function does the bulk of the work to check for duplicate events and add
    new events to a list to be called by the JSON library.
    '''
    feedObj = feedparser.parse(feedUrl)  # RSS parse the feed
    feedEnt = feedObj.entries  # Grab the entries from the parsed RSS feed
    alertList =[]  # List to hold all the alerts as a collection
    eventsAdded = 0  # Event counter
    for alert in feedEnt:
        alertObj = dict()  # Dict for Alert objects
        try:
            with open(alertTracker) as f2:
                pass
        except IOError:
            print('Error! Check the alert tracker file.')
            sys.exit()
        alertID = alert.title.split(':')[0].strip()  # Isolate Alert ID from RSS <title>
        with open(alertTracker) as f2:
            if alertID in f2.read():  # Check if we already grabbed the alerts
                pass
            else:
                eventsAdded = eventsAdded + 1  # Count up if we have new events
                with open(alertTracker, 'a') as f2:
                    f2.write(alertID+'\n')  # Write new events to state file
                    alertObj['title'] = alert.title  # Grab RSS <title> for each Alert, add to dict
                    alertObj['link'] = alert.link  # Grab RSS <link> for each Alert, add to dict
        alertList.append(alertObj)  # Add new alerts in dict format to the list
    print('Retrieved '+str(eventsAdded)+' new events!')
    return (alertList)  # Return new events (alerts)

# Get things going
if __name__ == '__main__':
    print('Starting up...')
    jsonGoods = feed_work(feedUrl)  # Function return to a var
    try:
        with open(outFile, 'w') as f1:
            pass
    except IOError:
        print('Error! Check the output json file.')
        sys.exit()
    if feedUrl:
        with open(outFile, 'w') as f1:
            f1.write(json.dumps(jsonGoods))  # Use our function return var
        with open(outFile) as f3:
            for i in f3:
                if '[{},' in i:  # Check if no new events (empyty JSON)
                    print('Empty outfile. Should match events.')  # To-Do: Depending on implementation, insert abort here
        print('All done!')
    else:
        print('Error! Check feed URL.')
        sys.exit()
