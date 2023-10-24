
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
            'message': 'Your data is not registered, Please contact the owner!'
        }
        return response
    else:
        response = {
            'status': 200,
            'message': 'Your data is registered, Bot is ready to use!'
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

        



    
