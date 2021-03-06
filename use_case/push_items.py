from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import uuid
import time
import decimal

#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

orders_table = dynamodb.Table('Orders')
sec_table = dynamodb.Table('Securities')

with open("securities.json") as json_file:
    securities = json.load(json_file, parse_float = decimal.Decimal)
    for security in securities:
        Symbol = security['Symbol']
        ProductType = security['ProductType']
        SubscriptionEnabled = bool(security['SubscriptionEnabled'])
        TradingEnabled = bool(security['TradingEnabled'])
        Description = security['Description']
        Risk = security['Risk']

        print("Adding security:", Symbol)

        sec_table.put_item(
           Item={
               'Symbol': Symbol,
               'ProductType': ProductType,
               'SubscriptionEnabled': SubscriptionEnabled,
               'TradingEnabled':TradingEnabled,
               'Description':Description,
               'Risk':Risk
            }
        )

with open("orders.json") as json_file:
    orders = json.load(json_file, parse_float = decimal.Decimal)
    for order in orders:
        NewOrderId = str(uuid.uuid4().hex) #int(order['NewOrderId'])
        TransactionTime = str(time.time()) #order['TransactionTime']
        ClientOrderId = int(order['ClientOrderId'])
        Status = order['Status']
        Details = order['Details']

        print("Adding order:", NewOrderId, TransactionTime)

        orders_table.put_item(
           Item={
               'NewOrderId': NewOrderId,
               'TransactionTime': TransactionTime,
               'ClientOrderId': ClientOrderId,
               'Status':Status,
               'Details':Details
            }
        )
