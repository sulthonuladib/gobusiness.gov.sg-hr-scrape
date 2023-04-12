from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = 'https://www.gobusiness.gov.sg'
main_page_url = base_url + '/browse-all-solutions-human-resource-solutions/human-resource-management-system--hrms-'

def get_main_page():
    print('Getting Main Page', main_page_url)
    page = requests.get(main_page_url)
    return page.text

def get_sub_page_url(page):
    print('Getting URL List from Main Page Solution List')
    urls = []
    soup = BeautifulSoup(page, 'lxml')
    endpoints = soup.find('table').find_all('a', href=True)
    for endpoint in endpoints:
        urls.append(base_url + endpoint['href'])

    return urls

def get_table_headers(url):
    headers = []

    sub_page = requests.get(url)
    soup = BeautifulSoup(sub_page.text, 'lxml')
    table = soup.find('table')
    for i in table.find_all('th'):
        title = i.text
        headers.append(title)

    return headers

def extract_table_content(urls, dataframe):
    for url in urls:
        print('Extracting table on', url)
        sub_page = requests.get(url)
        soup = BeautifulSoup(sub_page.text, 'lxml')
        table = soup.find('table')
        for j in table.find_all('tr')[1:]:
           row_data = j.find_all('td')
           row = [i.text for i in row_data]
           last_row = row_data[len(row_data) - 1].find('a', href=True)['href']
           row[len(row) - 1] = base_url + last_row
           length = len(dataframe)
           dataframe.loc[length] = row

def main():
    page = get_main_page()
    sub_page_urls = get_sub_page_url(page)
    headers = get_table_headers(sub_page_urls[0])

    dataframe = pd.DataFrame(columns = headers)
    content = extract_table_content(sub_page_urls, dataframe)

    dataframe.to_csv('hr_data.csv', index=False)

main()
