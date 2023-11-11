from dotenv import load_dotenv
load_dotenv()
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import client_data
import util_function

uri = f'mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@discordbotdatabase.bpx5wpk.mongodb.net/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def mongoConnect():
    try:
        client.admin.command('ping')
        print("Connection Established!")
    except Exception as e:
        print(e)

async def checkOwner(SECRET_KEY: str):
    db = client["user"]
    collection = db["data"]

    data = collection.find_one({'secretkey': SECRET_KEY})
    if data is None:
        return {'status': 400, 'message': 'Key not found!'}
    elif data['expdate'] == '' or data['status'] == False or util_function.expired(data['expdate']):
        return {'status': 400, 'message': 'Bot is inactive!'}
    else: return {'status': 200, 'message': 'Bot is active and ready to use!'}
    
async def getPresence(SECRET_KEY: str):
    db = client["user"]
    collection = db["data"]

    CHECK = list(collection.find({
        "database": "User Data"
    }))

    RESULTS = CHECK[0].get('user_data')

    checkResult = []
    for i in RESULTS:
        if SECRET_KEY == i.get('secretkey'):
            checkResult.append(i)
            
    if len(checkResult) < 1:
        response = {
            'status': 400,
            'message': 'Null'
        }
        return response
    else:
        msg = checkResult[0].get('data').get('presence')
        response = {
            'status': 200,
            'message': msg
        }
        return response
    
def getbotinfo():
    db = client[f'user_{client_data.SECRET_KEY}']
    data = db[f'data']

    bot = data.find_one({'discordtoken': client_data.TOKEN})
    if bot is None:
        raise ValueError('Bot is not in the databases!')
    else:
        {'status': 200, 'data': bot}

async def addProduct(productName: str, productId: str, productPrice: int, roleid):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']

    query = {
        'productName': productName,
        'productId': productId,
        'productPrice': productPrice,
        'roleId': roleid
    }
    try:
        queryCheck = collection.find_one({
            'database': 'User Product',
        })
        if queryCheck is None:
            collection.insert_one({
                'database': 'User Product',
                'productlist': [query]
            })
        elif any(d.get('productId') == productId for d in queryCheck.get('productlist')):
            return f'Product ID is already exist in databases!'
        else:
            modified = queryCheck
            modified.get('productlist').append(query)
            update = {
                "$set": {
                    "productlist": modified.get('productlist')
                }
            }
            collection.update_one({'database': 'User Product'}, update)
        return 'Product successfully added to databases!'
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return f'Error occurred, Please contact support!'

async def addProductLisen(productPrice: int, roleid):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'productlisen']

    data = collection.find_one({'database': 'User Product'})
    if data is None:
        query = {
            'database': 'User Product',
            'productlist': [{
                'productName': 'Lisensi Radar Bot',
                'productId': 'botlisen',
                'productPrice': productPrice,
                'roleId': roleid
            }]
        }
        collection.insert_one(query)
        return f'Success add product to databases!'
    else:
        return f'Product already exist in databases!'
    
async def removeproduct(productId: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']
    stock = db[f'stock']

    query = collection.find_one({'database': 'User Product'})
    
    if query is None:
        return 'Not found!'
    else:
        for index, data in enumerate(query.get('productlist')):
            if data.get('productId') == productId:
                query.get('productlist').pop(index)
                break
        update = {
            "$set": {
                "productlist": query.get('productlist')
            }
        }
        collection.update_one({'database': 'User Product'}, update)
        stock.find_one_and_delete({'productId': productId})
        return 'Remove product success!'
    
async def setprice(productId: str, newPrice: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']

    query = collection.find_one({'database': 'User Product'})
    
    if query is None:
        return 'Not found!'
    else:
        totalfound = 0
        for index, data in enumerate(query.get('productlist')):
            if data.get('productId') == productId:
                data['productPrice'] = newPrice
                totalfound = totalfound + 1
        update = {
            "$set": {
                "productlist": query.get('productlist')
            }
        }
        collection.update_one({'database': 'User Product'}, update)
        if totalfound == 0:
            return f'Product not found in the database!'
        else:
            return 'New price has been set!'
        
async def addstock(productId: str, productdetails: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']
    stock = db[f'stock']

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:
        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': [productdetails]
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.append(productdetails)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'

async def addstocklisen(amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']
    stock = db[f'stocklisen']

    productId = 'botlisen'
    productdetails = 'xx'

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:
        newstock = []
        for i in range(amount):
            newstock.append(productdetails)

        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': [productdetails]
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.extend(newstock)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'

async def showstock(productId: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None or len(data.get('stock')) == 0:
        return f'No stock found in the databases!'
    else:
        message = ''
        for index, stock in enumerate(data.get('stock')):
            message = message + stock + ' - Index ' + str(index) + '\n'

        return f'{message}'

async def removestock(productId: str, index: int, isAll: bool):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None:
        return f'Nothing to delete!'
    elif isAll:
        update = {
                "$set": {
                    "stock": []
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove all stocks available!'
    else:
        data.get('stock').pop(index)
        modified = data.get('stock')
        update = {
                "$set": {
                    "stock": modified
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove stocks on index {index}'
    
async def removestocklisen(productId: str, index: int, isAll: bool):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stocklisen']
    data = stock.find_one({'productId': productId})
    if data is None:
        return f'Nothing to delete!'
    elif isAll:
        update = {
                "$set": {
                    "stock": []
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove all stocks available!'
    else:
        data.get('stock').pop(index)
        modified = data.get('stock')
        update = {
                "$set": {
                    "stock": modified
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove stocks on index {index}'
    
async def takestock(productId: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None:
        return {'status': 400, 'message': 'Product ID not found!'}
    elif len(data.get('stock')) == 0:
        return {'status': 400, 'message': 'There is not available stock for that Product ID'}
    elif len(data.get('stock')) < amount:
        return {'status': 400, 'message': 'Insufficient amount of product'}
    elif len(data.get('stock')) >= amount:
        message = ''
        for i in range(amount):
            message = message + data.get('stock').pop(0) + '\n'
        update = {
                "$set": {
                    "stock": data.get('stock')
                }
            }
        stock.update_one({'productId': productId}, update)
        return {'status': 200, 'message': message}
    else:
        return {'status': 400, 'message': 'Internal server error!'}
    
async def register(discordid: str, growid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    discordid = str(discordid)

    data = user.find_one({'discordid': discordid})
    dupecheck = user.find_one({'growid': growid})
    if data is None and dupecheck is None:
        query = {
            'database': 'User Customer Database',
            'discordid': discordid,
            'growid': growid,
            'worldlock': {'currency': 'wl', 'balance': 0},
            'rupiah': {'currency': 'rp', 'balance': 0}
        }
        user.insert_one(query)
        return f'Successfully register {growid}!'
    elif dupecheck is not None:
        return f'Grow ID is already registered!'
    else:
        update = {
                "$set": {
                    "growid": growid
                }
            }
        oldgrow = data.get('growid')
        user.update_one({'discordid': discordid}, update)
        return f'Successfully set from {oldgrow} to {growid}'
    
async def info(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    data = user.find_one({'discordid': discordid})
    if data is None:
        return {'status': 400, 'message': 'Youre not registered yet!'}
    else:
        return {
            'status': 200,
            'message': 'Success fetch data!',
            'growid': data.get('growid'),
            'worldlock': data.get('worldlock'),
            'rupiah': data.get('rupiah')
        }
    
async def addtemplate():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    print()
    if data is None:
        query = {
            'database': 'User Assets',
            'bannerurl': 'https://cdn.discordapp.com/attachments/1166767160878698628/1167104315261980743/standard.gif?ex=654ce998&is=653a7498&hm=a82e5dab07f1cd87999964cee579bec1e1b43c69257336ba15b7d3bdd0852bcb&',
            'sticker_1': '<a:Siren:1167137117453959270> ',
            'sticker_2': '<a:arrow4:1167148754772693012>',
            'sticker_3': '<:money1:1167148958053838949>',
            'sticker_4': '<:wl:1167146128622506134>',
            'sticker_5': '<a:darkbluecrown:1167155192773488710>'
        }
        assets.insert_one(query)
        return f'Success added template to databases!'
    else:
        return f'Template already exist in databases!'
    
async def changeassets(assetsid: str, value: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return f'Assets not found!'
    elif assetsid in ['bannerurl', 'sticker_1', 'sticker_2', 'sticker_3', 'sticker_4', 'sticker_5']:
        update = {
                "$set": {
                    assetsid: value
                }
            }
        assets.update_one({'database': 'User Assets'}, update)
        return f'Change template success!'
    else:
        return f'Assets ID is incorrect!'

async def getassets():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return {'status': 400, 'message': 'Assets not found!'}
    else:
        return {
            'status': 200,
            'assets': {
                'bannerurl': data.get('bannerurl'),
                'sticker_1': data.get('sticker_1'),
                'sticker_2': data.get('sticker_2'),
                'sticker_3': data.get('sticker_3'),
                'sticker_4': data.get('sticker_4'),
                'sticker_5': data.get('sticker_5')
            }
        }
async def showassets():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return {'status': 400, 'message': 'Nothing to show!'}
    else:
        return {'status': 200, 'assets': [
            {
                'code': 'bannerurl',
                'value': data.get('bannerurl')
            },
            {
                'code': 'sticker_1',
                'value': data.get('sticker_1')
            },
            {
                'code': 'sticker_2',
                'value': data.get('sticker_2')
            },
            {
                'code': 'sticker_3',
                'value': data.get('sticker_3')
            },
            {
                'code': 'sticker_4',
                'value': data.get('sticker_4')
            },
            {
                'code': 'sticker_5',
                'value': data.get('sticker_5')
            },
        ]}
    
async def give(discordid: str, type: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    discordid = str(discordid)

    data =  user.find_one({'discordid': discordid})
    if data is None:
        return f'User not registered!'
    else:
        if type not in ['worldlock', 'rupiah']:
            return f'Type value must be "worldlock" or "rupiah"!'
        else:
            data[type]['balance'] = data[type]['balance'] + amount
            update = {
                "$set": {
                    type: data[type]
                }
            }
            user.update_one({'discordid': discordid}, update)
            if '-' in str(amount):
                return f'Success remove {str(amount).replace("-", "")} {type} from <@{discordid}>'
            else:
                return f'Success add {amount} {type} to <@{discordid}>'
            
async def setwebhook(webhookurl: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    webhook = db[f'webhook']

    data = webhook.find_one({'database': 'User Webhook'})
    if data is None:
        query = {
            'database': 'User Webhook',
            'webhookurl': webhookurl
        }
        webhook.insert_one(query)
        return f'Success set webhook to databases!'
    else:
        update = {
                "$set": {
                    'webhookurl': webhookurl
                }
            }
        webhook.update_one({'database': 'User Webhook'}, update)
        return f'Success set new webhook to databases!'
    
async def setdeposit(world: str, owner: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    deposit = db[f'deposit']

    data = deposit.find_one({'database': 'User Deposit'})
    if data is None:
        query = {
            'database': 'User Deposit',
            'world': world,
            'owner': owner
        }
        deposit.insert_one(query)
        return f'Success set deposit info to databases!'
    else:
        update = {
                "$set": {
                    'world': world,
                    'owner': owner
                }
            }
        deposit.update_one({'database': 'User Deposit'}, update)
        return f'Success set new deposit info to databases!'
    
async def getdeposit():
    db = client[f'user_{client_data.SECRET_KEY}']
    deposit = db[f'deposit']

    data = deposit.find_one({'database': 'User Deposit'})
    if data is None:
        return {'status': 400, 'message': 'Deposit info is not found!'}
    else:
        return {'status': 200, 'data': data}

async def checktotalstock(productid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productid})
    totalstock = 0
    if data is None:
        pass
    else:
        totalstock = int(len(data.get('stock')))
    return totalstock

async def checktotalstocklisen():
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stocklisen']

    data = stock.find_one({'productId': 'botlisen'})
    totalstock = 0
    if data is None:
        pass
    else:
        totalstock = int(len(data.get('stock')))
    return totalstock

async def checkstocklisen():
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']
    
    data = product.find_one({'database': 'User Product'})
    if data is None:
        return {'status': 400, 'message': 'Product is not found!'}
    else:
        array = data.get('productlist')
        for index, data in enumerate(array):
            stock = await checktotalstocklisen()
            data['totalstock'] = stock
        return {'status': 200, 'data': array}
        

async def checkstock():
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']

    productdata = product.find_one({'database': 'User Product'})
    if productdata is None:
        return {'status': 400, 'message': 'Product is not found!'}
    else:
        array = productdata.get('productlist')
        for index, data in enumerate(array):
            stock = await checktotalstock(data['productId'])
            data['totalstock'] = stock
        return {'status': 200, 'data': array}
    
async def isOrder(productid: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']

    productdata = product.find_one({'database': 'User Product'})
    stockcheck = await checktotalstock(productid)
    if productdata is None:
        return {'status': 400, 'message': 'Product not been set!'}
    elif productdata is not None and stockcheck >= amount:
        array = productdata.get('productlist')
        count = 0
        price = 0
        
        for data in array:
            if data['productId'] == productid:
                count = count + 1
                object = data
                break
            else:
                pass
        if count == 0:
            return {'status': 400, 'message': 'Product code is invalid'}
        else:
            return {'status': 200, 'message': 'Processing order..\n Bot will sent product via Direct Messages!', 'productdata': object}
    else:
        return {'status': 400, 'message': 'Insufficient Stock!'}

async def isOrderlisen(productid: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']

    productdata = product.find_one({'database': 'User Product'})
    stockcheck = await checktotalstocklisen()
    if productdata is None:
        return {'status': 400, 'message': 'Product not been set!'}
    elif productdata is not None and stockcheck >= amount:
        array = productdata.get('productlist')
        count = 0
        price = 0
        
        for data in array:
            if data['productId'] == productid:
                count = count + 1
                object = data
                break
            else:
                pass
        if count == 0:
            return {'status': 400, 'message': 'Product code is invalid'}
        else:
            return {'status': 200, 'message': 'Processing order..\n Bot will sent product via Direct Messages!', 'productdata': object}
    else:
        return {'status': 400, 'message': 'Insufficient Stock!'}
        
async def setorderstate(state: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    states = db[f'states']

    data = states.find_one({'database': 'User State'})
    if data is None:
        query = {
            'database': 'User State',
            'state': state
        }
        states.insert_one(query)
        return f'Success create new state DB!'
    else:
        update = {
            "$set": {
                'state': state,
            }
        }
        states.update_one({'database': 'User State'}, update)
        return f'Success change state!'
    
async def checkstate():
    db = client[f'user_{client_data.SECRET_KEY}']
    states = db[f'states']

    data = states.find_one({'database': 'User State'})
    if data is None:
        return {'status': 400, 'message': 'State not found, please set it first!'}
    else:
        if data['state'] == "False":
            return {'status': 200, 'state': data['state']}
        else:
            return {'status': 400, 'message': 'Bot is still processing order, please wait for a moment!'}
        
async def setpresence(presence: str):
    db = client[f'user']
    selectpresence = db[f'data']

    data = selectpresence.find_one({'discordtoken': client_data.TOKEN})
    if data is None:
        return f'Data not found!'
    else:
        update = {
            "$set": {
                'presence': presence,
            }
        }
        selectpresence.update_one({'discordtoken': client_data.TOKEN}, update)
        return f'Success change presence, please restart your bot to apply!'
    
async def addstockbulk(productId: str, productdetails: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']
    stock = db[f'stock']

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:

        sets_of_data = productdetails.split(',')
        array = []
        for data_set in sets_of_data:
            dictionary = {data_set}
            
            array.append(dictionary)

        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': sets_of_data
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.extend(sets_of_data)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'

async def setchannelhistory(channelid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    channel = db[f'channelhistory']

    data = channel.find_one({'database': 'User Channel History'})
    if data is None:
        query = {
            'database': 'User Channel History',
            'channelid': channelid
        }
        channel.insert_one(query)
        return f'Success set channel history to databases!'
    else:
        update = {
            "$set": {
                'channelid': channelid,
            }
        }
        channel.update_one({'database': 'User Channel History'}, update)
        return f'Success change channel history!'
    
async def getchannelhistory():
    db = client[f'user_{client_data.SECRET_KEY}']
    channel = db[f'channelhistory']

    data = channel.find_one({'database': 'User Channel History'})
    if data is None:
        return {'status': 400, 'message': 'Channel history not found!'}
    else:
        return {'status': 200, 'data': data['channelid']}
    
async def addlogs(logged):
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        query = {
            'database': 'User Logs',
            'logs': [logged]
        }
        logs.insert_one(query)
        return f'Success create new logs DB!'
    else:
        logsArray = data.get('logs')
        logsArray.append(logged)
        update = {
            "$set": {
                'logs': logsArray,
            }
        }
        logs.update_one({'database': 'User Logs'}, update)
        return f'Success add logs!'
    
async def showlogs():
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        return {'status': 400, 'message': 'Logs not found!'}
    else:
        return {'status': 200, 'data': data['logs']}
    
async def deletelogs():
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        return {'status': 400, 'message': 'Logs not found!'}
    else:
        update = {
            "$set": {
                'logs': [],
            }
        }
        logs.update_one({'database': 'User Logs'}, update)
        return {'status': 200, 'message': 'Success delete logs!'}

async def claim(secretkey: str, license: str):
    db = client[f'user']
    bot = db[f'data']

    data = bot.find_one({'secretkey': secretkey})
    if data is None:
        return {'status': 400, 'message': 'Secret key not found!'}
    else:
        if license in data['license'] and data['status'] == False:
            data['license'].remove(license)
            expdate = util_function.getonemonth()
            update = {
                "$set": {
                    "license": data['license'],
                    "expdate": expdate,
                    "status": True
                }
            }
            bot.update_one({'secretkey': secretkey}, update)
            return {'status': 200, 'message': f'Success, bot will expired on {expdate}'}
        elif license in data['license'] and data['status'] == True:
            data['license'].remove(license)
            expdate = util_function.addonemonth(data['expdate'])
            update = {
                "$set": {
                    "license": data['license'],
                    "expdate": expdate,
                    "status": True
                }
            }
            bot.update_one({'secretkey': secretkey}, update)
            return {'status': 200, 'message': f'Success, bot will expired on {expdate}'}
        else:
            return {'status': 400, 'message': f'License is not valid!'}
        
async def registerbot(discordtoken: str, discordid: str, license, secretkey: str):
    db = client[f'user']
    user = db[f'data']

    data = user.find_one({'discordtoken': discordtoken})
    secretcheck = user.find_one({'secretkey': secretkey})
    if data is None and secretcheck is None:
        query = {
            'database': 'User Data',
            'discordid': discordid,
            'discordtoken': discordtoken,
            'secretkey': secretkey,
            'presence': 'Hello World!',
            'license': [license],
            'expdate': '',
            'status': False
        }
        user.insert_one(query)
        return {'status': 200, 'message': 'Success, check direct message to get your details!'}
    elif data is not None and data['secretkey'] == secretkey:
        oldarray = data['license']
        newarray = oldarray.append(license)
        update = {
                "$set": {
                    "license": data['license']
                }
            }
        user.update_one({'discordtoken': discordtoken}, update)
        return {'status': 200, 'message': 'Success, check direct message to get your details!'}
    elif data is not None and data['secretkey'] != secretkey:
        return {'status': 400, 'message': 'Wrong secretkey for that Token!'}
    elif secretcheck is not None:
        return {'status': 400, 'message': 'Secretkey already exist, use another password!'}

async def checksecret(SECRET_KEY: str):
    db = client["user"]
    collection = db["data"]

    data = collection.count_documents({'secretkey': SECRET_KEY})
    if data == 1:
        return {'status': 200, 'message': 'Authorized!'}
    elif data == 0:
        return {'status': 400, 'message': 'Unauthorized!'}
    else:
        return {'status': 400, 'message': 'Error occured!'}
    
async def addip(ip: str):
    db = client[f'user']
    listipwhitelist = db[f'ip']

    filter ={'database': 'IP Whitelist'}

    data = listipwhitelist.find_one(filter)
    if data is None:
        query = {
            'database': 'IP Whitelist',
            'ip': [ip]
        }
        listipwhitelist.insert_one(query)
        return 'Success add IP to whitelist!'
    else:
        oldarray = data['ip']
        newarray = oldarray.append(ip)
        update = {
                "$set": {
                    "ip": data['ip']
                }
            }
        listipwhitelist.update_one(filter, update)
        return 'Success add new IP to whitelist!'