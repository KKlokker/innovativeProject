import datetime
import cv2
import easyocr
import API.DBConnector as DBConnector

def extractText(path):
    # load image from path
    img = cv2.imread(path)
    # convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # convert grayscale image to binary image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # find text using EasyOCR
    reader = easyocr.Reader(['da'])
    result = reader.readtext(thresh)
    # return result
    return result

def extractItemsFromText(text):
    # Find text with currency in it
    availableCurrencies = ["kr", "€", "$", "£"]
    usedCurrency = None
    AllItems = []
    for textLine in text:
        for currency in availableCurrencies:
            if currency in textLine[1]:
                # Find all text with roughly the same y coordinate
                y = textLine[0][0][1]
                items = []
                for textLine2 in text:
                    if abs(textLine2[0][0][1] - y) < 50 and textLine != textLine2:
                        items.append(textLine2)
                # Find the item with the lowest x coordinate
                x = 10000000
                itemWithLowestX = None
                for item in items:
                    if item[0][0][0] < x:
                        x = item[0][0][0]
                        itemWithLowestX = item
                quantity = itemWithLowestX[1]
                # Extract only numbers from quantity
                quantity = "".join([char for char in quantity if char.isdigit()])
                if quantity == "":
                    break

                price = textLine[1]
                price = "".join([char for char in price if char.isdigit() or char == "." or char == ","])
                if price == "":
                    break
                # Remove last character if it is a comma or period
                if price[-1] == "." or price[-1] == ",":
                    price = price[:-1]
                # Replace comma with period
                price = price.replace(",", ".")


                # set the remaining items as item names
                itemNames = []
                for item in items:
                    if item != itemWithLowestX and item != textLine:
                        itemNames.append(item[1])
                itemName = " ".join(itemNames)
                if itemName == "":
                    break
                
                AllItems.append({
                    "itemName": itemName,
                    "quantity": quantity,
                    "price": price
                })
                usedCurrency = currency
                break
    return { "items": AllItems, "currency": usedCurrency }

def saveReceiptToDB(imgPath, userId, groupId):
    receptInfo = extractItemsFromText(extractText(imgPath))
    db = DBConnector.DBConnector()
    date = datetime.datetime.now()
    currency = receptInfo["currency"]
    # create receipt
    query = 'INSERT INTO public.receipttable("userwhomadeitid", "attachedgroupid", "dateofcreation", "currencytype") VALUES(%s, %s, %s, %s) RETURNING id'
    params = (userId, groupId, date, currency)
    result = db.fetch(query, params)
    receiptId = result[0][0]
    # create items
    for item in receptInfo["items"]:
        itemPrice = float(item["price"]) / int(item["quantity"])
        for i in range(int(item["quantity"])):
            query = 'INSERT INTO public.itemtable("scanningid", "itemname", "price", "userid") VALUES(%s, %s, %s, %s)'
            params = (receiptId, item["itemName"], itemPrice, userId)
            db.execute(query, params)

if __name__ == "__main__":
    saveReceiptToDB("receipt.jpg")