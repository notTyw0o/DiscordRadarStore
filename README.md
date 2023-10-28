**__DOCUMENTATION FOR RADARBOT__**

__Getting Started__
After your register process is completed, try use
```
-> /check *no args
```
Bot should giving response "...Bot is ready to use"
If still response the opposite try contact support for further assistance

__Adding Products__
You can add your products using
```
/addproduct *productname, productid, productprice
```
_Note_
_This command can only be used to the registered Discord ID_

__Remove Products__
You can remove your updated products using
```
/removeproduct *productid
```
It's only remove one time, so if you have duplicates Product ID, use this command twice.
This command also deletes all stock available that attached to the Product ID
_Note: _
_it will still response "Success" even if the Product ID is not exist!_
_This command can only be used to the registered Discord ID_

__Set Price__
To set a new price to your product, you can simply use
```
/setprice *productid, newprice
```
This command only change the price of ur current price.
It will response "..Not found!" if the product is not existed
_Note_
_This command can only be used to the registered Discord ID_

__Add Stock__
After you put a product of course you need to update your stocks too, to update your stocks you can simply use
```
/addstock *productid, productdetails
```
_productdetails_ variable is the variable that bot will send to the customer. So update it carefully
```
ex:
/addstock rdp 192.168.1.1:admin:password123
/addstock cid AHAY123:password123
/addstock lisensinuron ZXCDSAFE1543
```
_Note_
_This command can only be used to the registered Discord ID_

__Show Stock__
To show all stock based on its Product ID you can simply use
```
/showstock *productid
```
_Note_
_This command can only be used to the registered Discord ID_

__Remove Stock__
To remove an existing stock in the databases, you can simply use
```
/removestock *productid: required, index: int, optional
```
If you want to remove all stocks exist in the databases you can just leave _index_ arguments to empty, but by filling _index_ arguments means you want only to delete the stock on specific index

_Note_
_This command can only be used to the registered Discord ID_

__Send Product__
To send product manually to target User ID, you can simply use
```
/send *discordid, productid, amount
```
The product stock will not deleted if the discord id is invalid.

_Note_
_This command can only be used to the registered Discord ID_

__Adding Templates Assets__
You need to add templates first before you can custom all the templates.
Try to use this command below
```
/addassets
```
If templates existed already in the databases it will not write dupes.

_Note_
_This command can only be used to the registered Discord ID_

__Show Templates Assets__
After you added the template assets, now you can see every assets that are in the databases. Try to use this command below!
```
/showassets
```
It will send embed containing the assetsid and the value of it!

_Note_
_This command can only be used to the registered Discord ID_

__Change Templates Assets__
After you added the template assets, now you can freely change all the assets that are in the databases. Try to use this command below!
```
/changeassets *assetsid, value
```
The assetsid needs to be valid for this command to work, otherwise it just showing error and show nothing!

_Note_
_This command can only be used to the registered Discord ID_

__Give amount of balance__
To give certain amount of balance try to use this command below!
```
/give *discordid, type: 'worldlock' or 'rupiah', amount
```
If you want to remove balance just add "-" in the amount, ex: -100

_Note_
_This command can only be used to the registered Discord ID_

__Deploy Menu__
You need to deploy menu for your customer can use this bot commnads, try to use
```
/deploy
```
It will deploy commands menu, so your customer do not need to create ticket to order things!

_Note_
_This command can only be used to the registered Discord ID_