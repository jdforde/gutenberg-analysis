import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time

def main():
    total_time = time.time()
    BASE_URL = 'https://www.gutenberg.org/ebooks/'
    TEXT_BASE_URL = 'https://www.gutenberg.org'
    titles = [] #Ensures no repeat titles 
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
    NUM_GUTENBERG = 100 #Number of books on gutenberg, is like 60,000 or something


    for i in range(1, NUM_GUTENBERG): #By calculations, it will take 22 hours to do the entire thing. Think about threadpoolexecutor
        try:
            start_time = time.time()

            page = BeautifulSoup(requests.get(BASE_URL + str(i)).text, 'html.parser')

            #Find Author and Title
            heading = page.find('h1', {'itemprop': 'name'}).text
            if page.find('a', {'typeof': 'pgterms:agent'}): 
                author = heading[heading.rfind('by')+3:]
                title = heading[:heading.rfind('by')-1:]
            else:
                author = 'NA'
                title = heading
            
            if title in titles:
                continue
            
            #Cleaner implementation?
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
            book = BeautifulSoup(requests.get(TEXT_BASE_URL + book_url).text, 'html.parser').get_text()


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
            
            df_dict['Title'].append(title)
            df_dict['Author'].append(author)
            df_dict['Subject1'].append(subject1)
            df_dict['Subject2'].append(subject2)
            df_dict['Subject3'].append(subject3)
            df_dict['Num_Downloads'].append(int(downloads))
            df_dict['Word_Count'].append(int(word_count))
            df_dict['Language'].append(language)
            df_dict['Release_Date'].append(release_date)

            print('Writing book {} titled {} to dataframe. Finished in {:.2f} seconds'.format(i, title, time.time() - start_time))

        except Exception as e:
            print('ERROR: Some error occured while handling book {}. More info - {}'.format(i, e))

    df = pd.DataFrame(df_dict)
    df.to_csv('gutenburg.csv')
    print('Finished entire program in {:.2f} seconds'.format(time.time() - total_time))


if __name__ == '__main__':
    main()