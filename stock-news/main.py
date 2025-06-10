import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STOCK_NAME = str(input("Please enter the name of the Stock\n"))
COMPANY_NAME = str(input("Please enter the name of the Company\n"))
wanted_percentage = int(input("Enter minimum positive or negative change to send an email:\n"))

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#NEWS_API = "Put your API key here" https://newsapi.org/
#STOCK_API = "Put your stocks API key here" https://www.alphavantage.co/support/#api-key
#APP_KEY =  Put your gmail app password  to this section

STOCK_PARAMS = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API

}

Connection = smtplib.SMTP("smtp.gmail.com")
Connection.starttls()
Connection.login(password=APP_KEY,user="") # Put the sender email to here.





response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_data = yesterday_data["4. close"]



two_days_ago_data = data_list[1]
two_days_ago_closing = two_days_ago_data["4. close"]




difference = abs(float(yesterday_closing_data)-float(two_days_ago_closing))
difference_arrow = float(yesterday_closing_data)-float(two_days_ago_closing)

Arrow = None
if difference_arrow > 0:
    Arrow = "🔺"
else:
    Arrow = "🔻"

percentage = (difference / float(yesterday_closing_data)) * 100


if percentage > wanted_percentage:
    news_params = {
        "apiKEY" : NEWS_API,
        "qInTitle" : COMPANY_NAME,
    }
    news_respond = requests.get(NEWS_ENDPOINT, params=news_params)
    articles =  news_respond.json()["articles"]


try:
    articles_first_three = articles[:3]








    formatted_articles = [f"Subject:{article['title']}. \n\nBrief: {article['description']}" for article in articles_first_three]

    print(formatted_articles)

    for articles in formatted_articles:
        msg = MIMEMultipart()
        msg["From"] = "" # The sender email
        msg["To"] = "" # The receiver email
        msg["Subject"] = f"{Arrow}{"{:.2f}".format(percentage)} {COMPANY_NAME} Stock Alert"

        msg.attach(MIMEText(articles, "plain", "utf-8"))

        Connection.sendmail(
            from_addr="", # The sender email
            to_addrs="", # The receiver email
            msg=msg.as_string()
        )
except NameError:
    print("No need to send email")
Connection.quit()

