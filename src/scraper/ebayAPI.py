'''
Created on Jan 11, 2019

@author: mark
'''
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

try:
    api = Connection(appid='MarkAlta-scraper-SBX-8393cab7d-aa86d044', config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

except ConnectionError as e:
    print(e)
    print(e.response.dict())
    
https://www.ebay.com/sch/37905/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27+antiquities+%27
https://www.ebay.com/sch/91101/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27+antiquities+%27