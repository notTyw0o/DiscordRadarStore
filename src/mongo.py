
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import client_data

uri = f'mongodb+srv://{client_data.MONGO_USER}:{client_data.MONGO_PASSWORD}@discordbotdatabase.bpx5wpk.mongodb.net/?retryWrites=true&w=majority'

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
            'message': 'Bot is inactive, Please contact the owner!'
        }
        return response
    else:
        response = {
            'status': 200,
            'message': 'Bot is active and ready to use!'
        }
        return response
    
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
    
async def addProduct(productName: str, productId: str, productPrice: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']

    query = {
        'productName': productName,
        'productId': productId,
        'productPrice': productPrice,
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
            print(i)
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

