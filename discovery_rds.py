#coding=UTF-8
#Auther：xwjr.com
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
import json

ID = 'ID'
Secret = 'Secret'
RegionId = 'cn-shenzhen'

clt = client.AcsClient(ID,Secret,RegionId)


DBInstanceIdList = []
DBInstanceIdDict = {}
ZabbixDataDict = {}
def GetRdsList():
    PageNumberStep = 1
    while 1:  //添加循环
        RdsRequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        RdsRequest.set_PageSize(100)    //设置当前page页显示实例数量为100
        RdsRequest.set_accept_format('json')
        RdsRequest.set_PageNumber(PageNumberStep)     //查询指定page的数据库实例
        RdsInfo = clt.do_action_with_exception(RdsRequest)
        RdsInfoList = (json.loads(RdsInfo))['Items']['DBInstance']
        PageNumberStep += 1

        # print len(RdsInfoList)
        if len(RdsInfoList) == 0:
            break

        for RdsInfoJson in RdsInfoList:
            DBInstanceIdDict = {}
            try:
                DBInstanceIdDict["{#DBINSTANCEID}"] = RdsInfoJson['DBInstanceId']
                DBInstanceIdDict["{#DBINSTANCEDESCRIPTION}"] = RdsInfoJson['DBInstanceDescription']
                DBInstanceIdList.append(DBInstanceIdDict)
                # print DBInstanceIdDict
            except Exception, e:
                print Exception, ":", e
                print "Please check the RDS alias !Alias must not be the same as DBInstanceId！！！"



GetRdsList()
ZabbixDataDict['data'] = DBInstanceIdList
print json.dumps(ZabbixDataDict)
