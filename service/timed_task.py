#!/usr/bin/python
#-*- coding:utf-8 -*-
import time

from pymongo import Connection
from bson.objectid import ObjectId
connection = Connection('localhost', 27017)
db = connection.publicBus
collectionBusRouter = db.busRouter

from bus import Bus
bus = Bus()

from bus_routers import Routers

def updateItem(name, direction):
  detail = bus.query_router_details(r, direction)
  collectionBusRouter.update({
    'name': name,
    'direction': direction
  }, {
    '$set': {
      'detail': detail
    }
  }, upsert  = True)
for r in Routers:
  try:
    updateItem(r, '0')
    updateItem(r, '1')
    print r
  except:
    print '执行——' + r + '，方向：' + direction + '——失败' 
  time.sleep(10)
