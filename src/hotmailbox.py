import requests
import client_data

async def getbalance():
    response = requests.get(f'https://api.hotmailbox.me/user/balance?apikey={client_data.HOTMAIL_API}')
    if response.status_code == 200:
        response = {
            'status': 200,
            'message': 'Success fetching data!',
            'data': response.json()
        }
    else:
        response = {
            'status': 400,
            'message': 'Error fetching data!'
        }
    return response

async def getstockemail():
    response = requests.get(f'https://api.hotmailbox.me/mail/currentstock')
    if response.status_code == 200:
        data = response.json()
        data = data['Data']
        data.pop(2)
        data.pop(4)
        newData = []
        code = 1
        for datas in data:
            if datas['MailCode'] in ['HOTMAIL', 'OUTLOOK']:
                price = 1
            elif datas['MailCode'] in ['HOTMAIL.TRUSTED', 'OUTLOOK.TRUSTED']:
                price = 7
            elif datas['MailCode'] in ['HOTMAIL.PVA', 'OUTLOOK.PVA']:
                price = 10
            query = {
                'productName': f'{datas["MailName"]} {datas["LiveTime"]}',
                'productId': code,
                'productPrice': price,
                'totalstock': datas['Instock']
            }
            code += 1
            newData.append(query)
        response = {
            'status': 200,
            'message': 'Success fetching data!',
            'data': newData[:6]
        }
    else:
        response = {
            'status': 400,
            'message': 'Error fetching data!'
        }
    return response

async def order(code, amount, totalprice):
    

    URL = f'https://api.hotmailbox.me/mail/buy?apikey={client_data.HOTMAIL_API}&mailcode={code}&quantity={amount}'
    response = requests.get(URL)
    data = response.json()
    if data['Code'] == 0:
        return {'status': 200, 'message': 'Success!', 'totalprice': totalprice, 'data': data['Data']}
    elif data['Code'] == 1:
        return {'status': 400, 'message': 'Error to put an order!'}
    else:
        return {'status': 400, 'message': 'Internal server error!'}