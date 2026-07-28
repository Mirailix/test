import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com/'

response = requests.get(url)

if response.status_code == 200:
    print("Сайт загружен!\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    quotes_blocks = soup.find_all('div', class_='quote')
    
    for block in quotes_blocks:

        text = block.find('span', class_='text').text
        
        author = block.find('small', class_='author').text
        
        print(f"{text}")
        print(f"(c) {author}")  
        print("-" * 30)
        
else:
    print(f" Сайт вернул код: {response.status_code}")