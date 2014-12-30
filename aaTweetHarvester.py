import requests
# import saveTweets
# import saveTweets2
import datetime
# import clearJSONStore
# import clearJSONStore2
import saveLastTweetId
# import saveTweetsCSV
import requests_oauthlib
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
from threading import Timer
import PMRkeys #PMRkeys is a separate local .py file with the Twitter Application Oauth credentials listed (not here for obvious reasons!) 
import json # will be needed to handle json
# import sqlite3 as lite # sqlite database
import sys
   

  
# ---------- define variables -------------------------------
adminURL='https://docs.google.com/spreadsheet/pub?key=0AgTXh43j7oFVdGp1NmxJVXVHcGhIel9CNUxJUk8yYXc&output=csv'
stopwordsURL ='https://docs.google.com/spreadsheet/pub?key=0AgTXh43j7oFVdEJGSWJNRXJJQVc5ZVo2cHNGRFJ3WVE&output=csv'
searchTerm=""
searchType=""
tweetNum=""
harvestPeriod=""
introText=""
text2=""
#stopcheck=0
lastSavedTweetIdDB=0
wordles=[""] # array to store words in

saveTweet=saveTweets.saveTweet
saveTweet2=saveTweets2.saveTweet
clearJSON=clearJSONStore.clearJSON
clearJSON2=clearJSONStore2.clearJSON
saveTweetCSV=saveTweetsCSV.saveTweet
saveTweetId=saveLastTweetId.saveTweetId

def retrieveTweetIdJS ():
    contents = open('lastTweet.json', 'r')
    cons = contents.read()
    ltids = json.loads(cons)
    global lastSavedTweetIdJS
    lastSavedTweetIdJS=ltids['lasttweetID']
    
    print ('-------------')
    print ('-------------')
   
    print('cons = '+cons)
    print('ID of last tweet saved in JSON file = '+lastSavedTweetIdJS)
    lastSavedTweetIdJS=int(lastSavedTweetIdJS)
    print ('-------------')
    print ('-------------')
    contents.close()
#def jasoniseTweets ():
    
    # turns a line separatedlist of JSON into a full on JSON object


#  --------------------------------------------------------------------------------------
#       ----------- end - above this line are set ups and imports etc ------------
#  --------------------------------------------------------------------------------------


# ------------- search twitter as a function ---------------
def search_tweets (term,count) : # params: term= 'what to search for' type = 'how to search' Count = 'number of tweets' (max 100)    search_url_root='https://api.twitter.com/1.1/search/tweets.json?q='
    retrieveTweetIdJS()
    # check what type the search term is
    clearJSON() # empties the temporary tweet store (line break version)
    clearJSON2() # empties the temporary tweet store (JSON version)
    #-------------------------
    ### clearTermStore ()
    #-------------------------
    saveTweet2('{"store":[')
    search_url_root='https://api.twitter.com/1.1/search/tweets.json?q='
    x= term.find('#') # look to see what position the hashtag is
    y=term.find('@') # look to see what position the @ sign is
    global termTXT
    if x==0 : #  this is checking if the first character is a hashtag
        print ('searching twitter API for hashtag: '+term)
        term2 = term.split('#')[1] # strip off the hash
        termTXT= term2 # allows the search term to be passed as a parameter
        term='%23'+term2 # add unicode for # sign (%23) if a hashtag search term
    else:
        if y==0: # if @ is the first character
            print ('searching twitter API for username: @'+term)
            term3 = term.split('@')[1] # strip off the @
            termTXT= term3 # allows the search term to be passed as a parameter
            term='%40'+term3 # add unicode for @ sign (%40) if a username search
        else:
            print ('searching for term: '+term) # or just search!
            termTXT= term # allows the search term to be passed as a parameter
    search_url=str(search_url_root+term+'&count='+count) # create the full search url from search term and admin setting for number of results
    print ('---------------------------')
    print ()
    try:
        auth = OAuth1(PMRkeys.PMR_consumer_key, PMRkeys.PMR_consumer_secret,PMRkeys.PMR_access_token,PMRkeys.PMR_access_secret )
        auth_response=requests.get(search_url, auth=auth)
        # print ('auth_response.text') # - uncomment to check the text is returning as expected
        # print (auth_response.text) # - uncomment to check the text is returning as expected
        j = (auth_response.text)
        js = json.loads(j)
        c = int(count)
        x=0
        try:
            while (x<c-1):
                try:
                    # - this is the processing script for tweets.
                    tweet_id = js['statuses'][x]['id']
                    testID=int(tweet_id)
                    print ('testID= '+str(testID))
                    print('-------')
                    print ('---------------')
                    if (x==0):
                        saveTweetId (str(tweet_id)) # saving current tweet id
                    print ('Tweet '+str(x+1)+' of '+str(c)+'. Tweet id: '+str(tweet_id))
                    name = js['statuses'][x]['user']['name']
                    user = js['statuses'][x]['user']['screen_name']
                    username= '@'+user
                    print ('From:'+username+'('+name+')')
                    tweet = js['statuses'][x]['text']
                    # following line gets rid of Twitter line breaks...
                    tweet=tweet.replace("\n","")
                    tweet=tweet.replace("\"","'")
                    tweet=tweet.replace("\\","")
                    print (tweet)
                    fullTweet='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } '
                    fullTweet2='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } ,'
                    print ('WTF = x = '+str(x))
                    saveTweet(fullTweet)
                    saveTweet2(fullTweet2)
                    tid=int(tweet_id)
                    fullTweetCSV=str(tweet_id)+','+str(username)+','+str(name)+','+str(tweet)
                    saveTweetCSV(fullTweetCSV)
                except UnicodeEncodeError:
                    print ('BREAK ERROR - Tweet text not available - dodgy term in tweet broke the API')
                    print ('---------------')
                x=x+1
        except  IndexError:
            print ('BREAK ERROR - Not enough tweets compared to TweetNum')
            print ('---------------')   
        fullTweet2='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } ]}'
        saveTweet2(fullTweet2)
    except KeyError:
        print ('BREAK ERROR - twitter search terms broke the API')
        print ('---------------')
    
# ------------- end search twitter -------------------------

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ >>>>>>>>>>>>>>>>>>>>>>>>>>

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ >>>>>>>>>>>>>>>>>>>>>>>>>>

# ------------- search twitter as a function 2 ---------------
def search_tweets_inc (term,count) : # params: term= 'what to search for' type = 'how to search' Count = 'number of tweets' (max 100)    search_url_root='https://api.twitter.com/1.1/search/tweets.json?q='
    retrieveTweetIdJS()
    # check what type the search term is
    clearJSON() # empties the temporary tweet store (line break version)
    clearJSON2() # empties the temporary tweet store (JSON version)
    saveTweet2('{"store":[')
    search_url_root='https://api.twitter.com/1.1/search/tweets.json?q='
    x= term.find('#') # look to see what position the hashtag is
    y=term.find('@') # look to see what position the @ sign is
    global termTXT
    if x==0 : #  this is checking if the first character is a hashtag
        print ('searching twitter API for hashtag: '+term)
        term2 = term.split('#')[1] # strip off the hash
        termTXT= term2 # allows the search term to be passed as a parameter
        term='%23'+term2 # add unicode for # sign (%23) if a hashtag search term
    else:
        if y==0: # if @ is the first character
            print ('searching twitter API for username: @'+term)
            term3 = term.split('@')[1] # strip off the @
            termTXT= term3 # allows the search term to be passed as a parameter
            term='%40'+term3 # add unicode for @ sign (%40) if a username search
        else:
            print ('searching for term: '+term) # or just search!
            termTXT= term # allows the search term to be passed as a parameter
    search_url=str(search_url_root+term+'&count='+count) # create the full search url from search term and admin setting for number of results
    print ('---------------------------')
    print ()
    try:
        auth = OAuth1(PMRkeys.PMR_consumer_key, PMRkeys.PMR_consumer_secret,PMRkeys.PMR_access_token,PMRkeys.PMR_access_secret )
        auth_response=requests.get(search_url, auth=auth)
        # print ('auth_response.text') # - uncomment to check the text is returning as expected
        # print (auth_response.text) # - uncomment to check the text is returning as expected
        j = (auth_response.text)
        js = json.loads(j)
        c = int(count)
        x=0
        while (x<c-1):
            try:
                tweet_id = js['statuses'][x]['id']
                testID=int(tweet_id)
                print ('testID= '+str(testID))
                print('-------')
                print ('---------------')
                if (x==0):
                    saveTweetId (str(tweet_id))
                print ('Tweet '+str(x+1)+' of '+str(c)+'. Tweet id: '+str(tweet_id))
                name = js['statuses'][x]['user']['name']
                user = js['statuses'][x]['user']['screen_name']
                username= '@'+user
                print ('From:'+username+'('+name+')')
                tweet = js['statuses'][x]['text']
                # following line gets rid of Twitter line breaks...
                tweet=tweet.replace("\n","")
                tweet=tweet.replace("\"","'")
                
                print (tweet)
                fullTweet='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } '
                fullTweet2='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } ,'
                print ('WTF = x = '+str(x))
                if (x==c-2):
                    fullTweet2='{"tweet_id": "'+str(tweet_id)+'","username": "'+str(username)+'","screen_name": "'+str(name)+'","tweet_text": "'+str(tweet)+'" } ]}'
                saveTweet(fullTweet)
                saveTweet2(fullTweet2)
                tid=int(tweet_id)
                fullTweetCSV=str(tweet_id)+','+str(username)+','+str(name)+','+str(tweet)
                saveTweetCSV(fullTweetCSV)                
            except UnicodeEncodeError:
                print ('Tweet text not available - dodgy term in tweet broke the API')
                print ('---------------')
            x=x+1
    except KeyError:
        print ('twitter search terms broke the API')
        print ('---------------')
    
# ------------- end search twitter2 -------------------------

#@@@@@@@@@@@@@@@@@@@

# ------------- get admin settings--------------------------
def loadAdmin (url):
    retrieveArray(adminURL)
    
    st=results[0] # get search term
    aa=st.split(',')
    global searchTerm
    searchTerm =aa[1]
    
    stype=results[1] # get search term
    bb=stype.split(',')
    global searchType
    searchType =bb[1]
    
    tNum=results[2] # get search term
    cc=tNum.split(',')
    global tweetNum
    tweetNum =cc[1]

    hPeriod=results[3] # get search term
    dd=hPeriod.split(',')
    global harvestPeriod
    harvestPeriod =dd[1]
    
    iText=results[4] # get search term
    ee=iText.split(',')
    global introText
    introText =ee[1]
    
    t2=results[5] # get search term
    ff=t2.split(',')
    global text2
    text2 =ff[1]
    print('-------- end of loadAdmin() ------------------')
    print('----------------------------------------------')
   
    
# ----------------------------------------------------------

# ------------- retrieve any google spreadsheet as data ----
def retrieveArray (url):
    try:
        Ws= requests.get(url)
        yy= Ws.text
        global results
        results = yy.splitlines()

        print ('stopwords ------------')
        print (results)
        print ('--------')
    
        print ('full list returned raw with line breaks --------')
        #print (yy)
        print ('results for '+url+' --------')
        # print (results)
        print ('--------')
        swCount=0
        for count in results:
            swCount+=1
        print ('count  for ' + url +'-----')
        print ('count = '+str(swCount))
        print (' end retrieveArray() ----------------------')
    # end retrieveArray
    except:
        print ('Can\'t connect to admin settings - no connection') 


# retrieveTweetsStoreContents
import json

global le
le = 0
def saveURLs (ul):
    
    ul=ul.replace("...","")
    try :
        urls = open('urls.txt', 'a')
        urls.write(',\"'+ul+'\"')
        urls.close()
    except:
        print ('error oepning urls.txt')

def saveUserMentions (un):
    un=un.replace(":","")
    un=un.replace("...","")
    try :
        usernames = open('mentions.txt', 'a')
        usernames.write(',\"'+un+'\"')
        usernames.close()
    except:
        print ('error oepning mentions.txt')
def saveHashtags (ht):
    ht=ht.replace(":","")
    ht=ht.replace("...","")
    #------
    ht=ht.replace('?', '')
    #--------------
    try:
        hashtags = open('hashtags.txt', 'a')
        hashtags.write(',\"'+ht+'\"')
        hashtags.close()
    except:
        print ('error oepning hashtags.txt')

def saveWords (word):
    
    #ul=ul.replace("...","")
    try :
        urls = open('words.txt', 'a')
        urls.write(','+word)
        urls.close()
    except:
        print ('error oepning urls.txt')

def saveTerms(array):
    # assumes array can be passed as a parameter. If not, change to call each term + repeat
    try:
        terms = open ('terms.txt','a')
        terms.write (',\"'+array+'\"')
        terms.close()
    except:
        print ('error oepning terms.txt')
        
def saveTermsRowCSV ():
    #dat=
    wws = open('words.txt', 'r')
    print ("words file CSV = ")
    print (wws)
    wws=wws.replace("[","")
    wws=wws.replace("]","")
    #wordies = open('wordsRows.CSV', 'a')
    #wordies.write(wws)
    #wordies.write('\n')
    #wordies.close()
    wws.close()


def retrieveTweetStore ():
    savedTweets = open('tweetstore2.json', 'r')
    cons = savedTweets.read()
    tweets = json.loads(cons)
    x=0
    l=0
    #global le
    global hh
    while x<150: # not dynamic, but x can never be more than 100 anyway due to twitter api rate capping
        try:
            hh=tweets['store'][x]['tweet_id']
            print ('hh = '+hh)
            x=x+1
        except:
            l=x
            print ('length = '+str(l))
            break
    x=0
    
    usernames = open('mentions.txt', 'w')
    usernames.write('[')
    usernames.close()
    while x<150: # not dynamic, but x can never be more than 100 anyway due to twitter api rate cappining
        try:
            hh=tweets['store'][x]['tweet_text'] ### duplicated?
            print ('tweet@['+str(x)+'] = '+hh)
            yy=hh.split(' ')
            print (yy)
            global le
            le=len(yy)
            ck=0
            i=0
            while i<le:
                # add in here the term array creation function
                at=yy[i].find('@')
                if at==0:
                    oo=yy[i]
                    oo=oo.replace(":","")
                    oo=oo.replace("...","")
                    oo=oo.replace("?","")
                    if i<(le-1) and x==0 and ck==0:
                        ck=1
                        print ('BANG')
                        usernames = open('mentions.txt', 'a')
                        usernames.write('\"'+oo+'\"')
                        print ('oo= '+oo)
                        usernames.close()
                    else:
                        saveUserMentions(yy[i])
                        print (yy[i])
                        print ('i = '+str(i))
                        ck=ck+1                   
                i=i+1
            print ('length of yy[] = '+str(le) )
            print('#########')
            x=x+1
        except:
            print (' some thing wrong here...')
            usernames = open('mentions.txt', 'a')
            usernames.write(']')
            usernames.close()
            l=x
            print ('returned '+str(l)+' tweets')
            break
    print ('------------- usernames processed -----------------')
    x=0 # reset counter
    print ('inside hashtags, yy = ')
    print (yy)
    hashtags = open('hashtags.txt', 'w')
    hashtags.write('[')
    hashtags.close()
    while x<150: # not dynamic, but x can never be more than 100 anyway due to twitter api rate cappining
        try:
            hh=tweets['store'][x]['tweet_text']
            print ('tweet#['+str(x)+'] = '+hh)
            yy=hh.split(' ')
            print ("inside hashtaggy bit of retrietwets ")
            print (yy)
            #global le
            le=len(yy)
            ck=0
            i=0
           
            while i<le:
                at=yy[i].find('#')
                if at==0:
                    oo=yy[i]
                    oo=oo.replace(":","")
                    oo=oo.replace('...','')
                    oo=oo.replace('?','')
                    if i<(le-1) and x==0 and ck==0 and yy[i]!=searchTerm : ###
                        ck=1
                        print ('hashtag BANG')
                        hashtags = open('hashtags.txt', 'a') ###
                        hashtags.write('\"'+oo+'\"')
                        print ('oo= '+oo)
                        hashtags.close()
                    else:
                        if yy[i]!=searchTerm:
                            saveHashtags(yy[i])
                            print (yy[i])
                            print ('i = '+str(i))
                            ck=ck+1                   
                i=i+1
            print ('length of jj[] = '+str(le) )
            print('#########')
            x=x+1
        except:
            # This except is closing the hashtags file
            hashtags = open('hashtags.txt', 'a')
            hashtags.write(']')
            hashtags.close()
            l=x
            print ('returned '+str(l)+' tweets')
            break
    print ('------------- hashtags processed -----------------')
    x=0
    
    urls = open('urls.txt', 'w')
    urls.write('[')
    urls.close()
    while x<150: # not dynamic, but x can never be more than 100 anyway due to twitter api rate cappining
        try:
            ttt=tweets['store'][x]['tweet_text'] ### duplicated?
            print ('tweet URL['+str(x)+'] = '+ttt)
            tweeties=ttt.split(' ')
            print (tweeties)
            global lenu
            lenu=len(tweeties)
            cku=0 ## check first char
            iu=0 ## check counter
            while iu<lenu:
                # add in here the term array creation function
                atu=tweeties[iu].find('http')
                if atu==0:
                    oo=tweeties[iu]
                    oo=oo.replace(":","")
                    oo=oo.replace("...","")
                    oo=oo.replace("?","")
                    if iu<(lenu-1) and x==0 and cku==0:
                        cku=1
                        print ('BANG URLs')
                        urls = open('urls.txt', 'a')
                        urls.write('\"'+oo+'\"')
                        print ('oo= '+oo)
                        urls.close()
                    else:
                        saveURLs(tweeties[iu])
                        print (tweeties[iu])
                        print ('iu = '+str(iu))
                        cku=cku+1     ### redundant?               
                iu=iu+1
            print ('length of tweeties[] = '+str(lenu) )
            print('#########')
            x=x+1
        except:
            print (' end of url checks - closing urls.tet...')
            urls = open('urls.txt', 'a')
            urls.write(']')
            urls.close()
            l=x
            print ('returned '+str(l)+' tweets')
            break
    print ('------------- usernames processed -----------------')
    x=0
    retrieveArray(stopwordsURL)
    print ('results at beginning of words ()')
    print (results)
    lenSW=len(results)
    xSW=0
    print ('>>>>>>><<<<<<<<<<<<<<<<<<')
    words = open('words.txt', 'w')
    words.write('[')
    words.close()
    while x<150: # not dynamic, but x can never be more than 100 anyway due to twitter api rate cappining
        try:
            sad=tweets['store'][x]['tweet_text'] ### duplicated?
            print ('word ['+str(x)+'] = '+sad)
            wordies=sad.split(' ')
            print (wordies)
            global lenw
            lenw=len(wordies)
            ckw=0 ## check first char
            iw=0 ## check counter
            while iw<lenw:
                # add in here the term array creation function
                atw=wordies[iw].find('#')
                atwu=wordies[iw].find('@')
                atwh=wordies[iw].find('http')
                global stopcheck
                if wordies[iw] in results:
                    print ('wordies[iw] is a stopword --  '+wordies[iw])
                    stopcheck = 1
                else:
                    stopcheck=0
                    print ('wordies[iw] is NOT a stopword --  '+wordies[iw])
                if atw!=0 and atwu!=0 and atwh!=0 and stopcheck==0:
                    oo=wordies[iw]
                    oo=oo.replace(":","")
                    oo=oo.replace("...","")
                    oo=oo.replace("?","")
                    oo=oo.replace('\"','')
                    oo=oo.replace(',','')
                    if iw<(lenw-1) and x==0 and ckw==0:
                        ckw=1
                        print ('BANG words')
                        usernames = open('words.txt', 'a')
                        wordArchive = open ('wordArchive.csv','a')
                        now = datetime.datetime.now()
                        warchiveDate=str(str(now.year)+" "+str(now.month)+" "+str(now.day)+" "+str(now.hour)+" "+str(now.minute))
                        print (now.year)
                        print ('warchiveDate = ' +warchiveDate)   
                        usernames.write(oo)
                        print ('oo= '+oo)
                        usernames.close()
                        wordArchive.close()
                    else:
                        saveWords(wordies[iw])
                        print (wordies[iw])
                        print ('iw = '+str(iw))
                        ckw=ckw+1     ### redundant?
                    
                iw=iw+1
            print ('length of wordies[] = '+str(lenw) )
            print('#########')
            x=x+1
        except:
            print (' end of word checks - closing words.tet...')
            words = open('words.txt', 'a')
            words.write(']')
            words.close()
            l=x
            print ('returned '+str(l)+' tweets')
            break
    print ('------------- words processed -----------------')
    
    savedTweets.close()
    
    #saveTermsRowCSV ()
    
# ------------- end retrieve data ---------------------------
# ------------- end admin ad functions etc ------------------


# -----------------------------------------------------------
# ------------- the business starts here---------------------
# -----------------------------------------------------------

retrieveTweetIdJS()

loadAdmin (adminURL) #load admin settings from google sheet
retrieveArray(stopwordsURL) #load stopwords from stopwords google sheet

search_tweets(searchTerm,tweetNum) # execute the twitter API search using the admin settings loaded


def keeplooping():  # define the loop and what it executes (rate is set by loaded setting: 'harvestPeriod' 
   
    loadAdmin (adminURL) #load admin settings from google sheet
    search_tweets(searchTerm,tweetNum)
    Timer(int(harvestPeriod), keeplooping).start()
    Timer(int(harvestPeriod)*.3, retrieveTweetStore).start()
    

keeplooping() # initiates the loop

# -----------------------------------------------------------
# ----------------- end busines -----------------------------


#search_tweets(searchTerm,searchType,tweetNum)
print ('-------99999999  end   9999-------')
print ('searchTerm = ')
print (searchTerm)
print ('searchType = ')
print (searchType)
print ('tweetNum')
print (tweetNum)
print ('harvestPeriod')
print (harvestPeriod)
print ('introText')
print (introText)
print ('text2')
print (text2)


print ('---- stopwords ------------')

    


