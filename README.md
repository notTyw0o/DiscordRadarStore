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