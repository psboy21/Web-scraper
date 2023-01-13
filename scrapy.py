from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import smtplib,ssl
from datetime import date
import db
#also do this program for multiple products given by user

app = Flask(__name__)
@app.route("/check-price")
def scrapy():
    items = []
    # Get all data from DB - name, url, threshold, receiver_email
    items_db_data = db.collection.find_one()
    url = items_db_data['url']
    thres_price = items_db_data['threshold price']
    
    # urls = ["https://www.amazon.in/ASIAN-Future-01-White-Running-Shoes/dp/B09YHGRQ12/ref=sr_1_1_sspa?crid=26AVV2P3ZTVL0&keywords=shoes%2Bfor%2Bmen&qid=1671602441&sprefix=shoes%2Caps%2C418&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1&psc=1"
    # , "https://www.amazon.in/Reebok-Future-Stride-Shoes-8-DV8404/dp/B07N9BQ12B/ref=sr_1_3?crid=2WZIKIAE50OUL&keywords=reebok+shoes+for+men&qid=1671951887&sprefix=reebok+%2Caps%2C264&sr=8-3"
    # , "https://www.amazon.in/Reebok-Mens-Flat-Grey-Edgility/dp/B09DYHM7TM/ref=sr_1_1?crid=2WZIKIAE50OUL&keywords=reebok%2Bshoes%2Bfor%2Bmen&qid=1671951887&sprefix=reebok%2B%2Caps%2C264&sr=8-1&th=1&psc=1"]
#    for url in urls:
    item_dict = {}
    headers = { 'User-Agent': 'My User Agent 1.0', 'From': 'personal@domain.com'  # This is another valid field
          }
    r = requests.get(url, headers=headers)
    htmlC = r.content
    soup = BeautifulSoup(htmlC,'html.parser')
    price = soup.find('span', class_="a-offscreen").get_text()
    price = price.strip()[1:]
    price = price.replace(",","")
    name  = soup.find(id="productTitle", class_="a-size-large product-title-word-break").get_text()
#      l[price] = type(price)
    item_dict['name'] = name
    item_dict['price'] = int(float(price))
    item_dict['date'] = date.today()
    items.append(item_dict)
    db.collection_daily.insert_one({"name":name,"price":price,"date":date.today().strftime("%d/%m/%Y")}) #sice we cannot store datetime type in database so we hav to convert it to string
    if(price<thres_price):
        send_mail()
    return items        
#We pass the results of our parsing along with the return statement to make them available on the HTML template.
@app.route("/",methods=['GET'])
def callfunc():
    items = scrapy()
    return render_template('index.html', price_dict=items)

def send_mail():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    items_db_data = db.collection.find_one()
    email = items_db_data['email']
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "priyanshu21082singh@gmail.com"  # Enter your address
    receiver_email = email                          # Enter receiver address
    password = os.getenv('PASS')                 #While this works when running on your system ,you will not get an error when you deploy and run on a remote server 
     #Heroku have their own ways of dealing with confidential information and environment variables.
    message = """hoorah!
    the price of the product is below your threshold price 
    now you can buy the product"""
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@app.route("/format", methods=['GET'])
def page():
    return render_template("form.html")

@app.route("/submit", methods=['POST'])
def submit_form():
#    print(request.form['price'])
    db.collection.insert_one({"url": request.form['url'] , "name":request.form['name'], "threshold price":request.form['price'], "email":request.form['email']})
    return "Succes"
    # return render_template("form.html")
#DO WE NEED TO MANUALLY CLOSE DATABASE CONNECTION 
#import db
#test to insert data to the data base
# @app.route("/test")
# def test():
#     db.collection.insert_one({"name": "John"})
#     return "Connected to the data base!"


# items_db_data = db.collection.find()
# for x in items_db_data:
#     print(x['url'])
#     print(x)

if __name__ == "__main__":
    print("Server Started!! ")
    app.run(debug=True)

