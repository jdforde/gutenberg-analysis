from multiprocessing.connection import Connection
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://www.gutenberg.org/ebooks/'
TEXT_BASE_URL = 'https://www.gutenberg.org'
df_dict = {
    'Title' : [],
    'Author' : [],
    'Subject1': [],
    'Subject2': [],
    'Subject3' : [],
    'Num_Downloads': [],
    'Word_Count': [],
    'Language' : [],
    'Release_Date' : []
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def scrape_book(i, s):
    try:
        start_time = time.time()

        page = BeautifulSoup(s.get(BASE_URL + str(i), timeout=20, headers=headers).text, 'html.parser')

        #Find Author and Title
        heading = page.find('h1', {'itemprop': 'name'}).text
        if page.find('a', {'typeof': 'pgterms:agent'}): 
            author = heading[heading.rfind('by')+3:]
            title = heading[:heading.rfind('by')-1:]
        else:
            author = 'NA'
            title = heading
    
        
        #Cleaner implementation?
        subject = ['NA', 'NA', 'NA'] #idea
        subjects = page.find_all('a', {'class':'block'})
        if (len(subjects) >= 3):
            subject1 = subjects[0].text
            subject2 = subjects[1].text
            subject3 = subjects[2].text
        elif (len(subjects) == 2):
            subject1 = subjects[0].text
            subject2 = subjects[1].text
            subject3 = 'NA'
        elif (len(subjects) == 1):
            subject1 = subjects[0].text
            subject2 = 'NA'
            subject3 = 'NA'
        else:
            subject1 = 'NA'
            subject2 = 'NA'
            subject3 = 'NA'  

        subject1 = subject1.replace('\n', '')    
        subject2 = subject2.replace('\n', '')   
        subject3 = subject3.replace('\n', '')   

        downloads = page.find('td', {'itemprop' : 'interactionCount'}).text.split(' ')[0]

        release_date = datetime.strptime(page.find('td', {'itemprop': 'datePublished'}).text, "%b %d, %Y")

        language = page.find('tr', {'property': 'dcterms:language'}).find('td').text
        
        book_url = page.find('a', {'title': 'Download'})['href']

        
 
        book = BeautifulSoup(s.get(TEXT_BASE_URL + book_url, timeout=20, headers=headers).text, 'html.parser').get_text()


        #This implementation is not great. Need a better way to distinguish header and footer
        word_count = 0

        for line in book.split('\n'):
            if '***' in line and 'start' in line.lower():
                word_count = 0
            if '***' in line and 'end' in line.lower():
                break

            for word in line.split(' '):
                if word.strip() != '':
                    word_count +=1
        
        
        
        print('Finished scraping book {} titled {}. Finished in {:.2f} seconds from process start to end'.format(i, title, time.time() - start_time))
        return [title, author, subject1, subject2, subject3, int(downloads), int(word_count), language, release_date]

    except Exception as e:
        print('ERROR: Some error occured on book {}. Dumping output: {}'.format(i, e))


def main():
    total_time = time.time()
    s = requests.Session()
    GUTENBERG_RANGE = range(1, 10000)
    MAX_WORKERS = 5000

    futures = []
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(GUTENBERG_RANGE))) as executor:
        for i in GUTENBERG_RANGE:
            future = executor.submit(scrape_book, i, s)
            futures.append(future)
    
    for row in futures:
        if row.result() and len(row.result()) >= 9:
            df_dict['Title'].append(row.result()[0])
            df_dict['Author'].append(row.result()[1])
            df_dict['Subject1'].append(row.result()[2])
            df_dict['Subject2'].append(row.result()[3])
            df_dict['Subject3'].append(row.result()[4])
            df_dict['Num_Downloads'].append(row.result()[5])
            df_dict['Word_Count'].append(row.result()[6])
            df_dict['Language'].append(row.result()[7])
            df_dict['Release_Date'].append(row.result()[8])

    
    df = pd.DataFrame(df_dict)
    df.to_csv('gutenburg.csv')
    print('Finished entire program in {:.2f} seconds'.format(time.time() - total_time))


if __name__ == '__main__':
    main()