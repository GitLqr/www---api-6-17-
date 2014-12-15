# created by hualai.deng , 2013-04-01
########################################################################
# configure the url route
urls = (
    ('/hello', 'interface.hello.hello'),
    ('/mymem', 'interface.mymem.Main'),
    ('/update', 'interface.update.Main'),
    ('/updatedb', 'interface.updatedb.Updatedb'),
    ('/login', 'interface.login.Login'),
    ('/get_data', 'interface.get_data.GetData'),
    ('/getAreaList', 'interface.getAreaList.getAreaList'),
    ('/getCategory', 'interface.getCategory.getCategory'),
    ('/getFeedList', 'interface.getFeedList.clsGetFeedList', 'user_id=10', 'begin_time=343423', 'count=20'),
    ('/getUserFeedList', 'interface.getFeedList.clsGetUserFeedList', 'user_id=10', 'begin_time=343423', 'count=20'),
    ('/getFeedContent', 'interface.getFeedContent.clsGetFeedContent', 'feedid=10'),
    ('/getNovelChapterContent', 'interface.getNovelChapterContent.clsGetNovelChapterContent', 'feedid=10'),
    ('/addSubscription', 'interface.addSubscription.addSubscription', 'user_id=""', 'feedid=""', 'op=""'),
    ('/addSub_test', 'interface.Subscription.clsSubscription', 'user_id=""', 'feedid=""', 'op=""'),
    ('/getFeedInfo', 'interface.getFeedInfo.clsGetFeedInfo', 'feedid=10'),
    ('/recvLog', 'interface.recvLog.recvLog', 'umid=""', 'uid=""', 'longitude=""', 
                'latitude=""', 'altitude=""', 'accuracy=""', 'provider=""', 
                'action=""', 'stamp=""', 'cur_page=""', 'card_id=""', 'resource_id=""', 'duration=""'),
    ('/getChannel', 'interface.getChannel.getChannel', 'method=""', 'type=""', 
                'topic=""', 'page=""', 'num=""', 'lastTime=""', 'key=""', 'videoid=""',),
    ('/actionRecord', 'interface.actionRecord.clsActionRecord'),
    ('/subscription', 'interface.Subscription.clsSubscription', 'user_id=""', 'feedid=""', 'op=""'),
    ('/getFrontpage', 'interface.getFrontpage.clsGetFrontpage', 'user_id=""', 'feedid=""', 'op=""'),
    ('/getCard', 'interface.getCard.clsGetCard', 'user_id=""', 'feedid=""', 'op=""'),
)


#########################################################################
# methods
#########################################################################
# return urls map
def getUrlsMap ():
    global urls
    urlsMap = []
    for urlInfo in urls:
        urlsMap.append( urlInfo[0] )
        urlsMap.append( urlInfo[1] )

    return urlsMap
        
    
########################################################################
# test
if __name__ == "__main__" :
    print str(urls)
