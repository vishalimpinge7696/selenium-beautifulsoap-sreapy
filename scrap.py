import bs4
import requests
import pandas as pd

res = requests.get('https://www.flipkart.com/search?q=all+mobiles+under+rs+10000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off')
soap = bs4.BeautifulSoup(res.text, 'html.parser')
name = soap.select('._3wU53n')
price = soap.select('._1vC4OE._2rQ-NK')
rating = soap.select('.hGSR34')
details = pd.DataFrame(columns= ('Name', 'Price', 'rating'))

l = 1
for i,j,k in zip(name, price, rating):
    details.loc[l] = i.text, j.text, k.text;
    l+=0

print(details)
details.to_csv('scrap-flip.csv', index=False, encoding='utf-8')
