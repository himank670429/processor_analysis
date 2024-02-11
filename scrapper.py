from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# global data
data = {
    "number" : {},
    "generation" : {},
    "launch_date" : {},
    "series" : {},
    "status" : {},
    "core_count" : {},
    "max_freq" : {},
    "base_freq" : {},
    "cache" : {},
    "TDP" : {}
}
row_count = 0

def get_cpu_data(url, missing_info : list):
    global data, row_count
    spec_sheet = urlopen(url)
    spec_soup = BeautifulSoup(spec_sheet, 'html.parser')

    divs = list(spec_soup.select('.tech-section-row'))
    divs_len = len(divs)
    data['generation'][f'{row_count}'] = divs[0].select_one('.tech-data').get_text().strip().split('th')[0]
    current_div_index = 0
    while len(missing_info) != 0 and current_div_index < divs_len:
        # get the values if they match
        current_div = divs[current_div_index]

        if 'number' in missing_info and current_div.select_one(".tech-label span").get_text() == 'Processor Number':
            data['number'][f'{row_count}'] = current_div.select_one('.tech-data span').get_text().strip()
            missing_info.remove('number')

        if 'max_freq' in missing_info and current_div.select_one(".tech-label span").get_text() in ["Max Trubo Frequency", "Performance-core Max Turbo Frequency"]:
            data['max_freq'][f'{row_count}'] = current_div.select_one('.tech-data span').get_text()
            missing_info.remove('max_freq')

        if 'base_freq' in missing_info and current_div.select_one(".tech-label span").get_text() in ['Performance-core Base Frequency', 'Processor Base Frequency', "Efficient-core Max Turbo Frequency", 'Configurable TDP-up Base Frequency']:
            data['base_freq'][f'{row_count}'] = current_div.select_one('.tech-data span').get_text().strip()
            missing_info.remove('base_freq')

        if 'TDP' in missing_info and current_div.select_one(".tech-label span").get_text() in ['Processor Base Power', 'Description','Configurable TDP-up', 'Configurable TDP-down']:
            data['TDP'][f'{row_count}'] = current_div.select_one('.tech-data span').get_text().strip()
            missing_info.remove('TDP')

        if 'architecture' in missing_info and current_div.select_one(".tech-label span").get_text() in ['Instruction Set']:
            data['architecture'][f'{row_count}'] = current_div.select_one('.tech-data span').get_text().strip()
            missing_info.remove('architecture')
        
        current_div_index += 1
    
    if 'max_freq' in missing_info:
        data['max_freq'] = data['base_freq']

def main():
    global data, row_count
    # urls
    urls = [f'https://www.intel.in/content/www/in/en/products/details/processors/core/i{i}/products.html' for i in [3,5,7,9]]

    # base url
    base_url = 'https://www.intel.in'

    # opening file
    for url in urls:
        html = urlopen(url)
        main_soup = BeautifulSoup(html, 'html.parser')

        # Main Table
        table = main_soup.select('table.table.table-sorter.sorting')[0].findChild('tbody')

        # get the data from the table
        rows = table.findChildren('tr')
        for tr in rows:
            row_data = tr.findChildren('td')
            link = row_data[0].find_next('a').attrs['href']
            print(row_data)
            status, date, no_of_cores, max_freq, base_freq, cache, TDP = row_data[1:8]
            data['status'][f'{row_count}'] = status.get_text().strip()
            data['launch_date'][f'{row_count}'] = date.get_text().strip()
            data['core_count'][f'{row_count}'] = no_of_cores.get_text().strip()
            data['max_freq'][f'{row_count}'] = max_freq.get_text().strip()
            data['base_freq'][f'{row_count}'] = base_freq.get_text().strip()
            data['TDP'][f'{row_count}'] = TDP.get_text().strip()
            data['cache'][f'{row_count}'] = cache.get_text().strip()
            data['series'][f'{row_count}'] = f'i{url[-15]}'
            
            # figure out what data is missing
            missing_info = ['number']
            if not max_freq.get_text().strip(): missing_info.append('max_freq')
            if not base_freq.get_text().strip(): missing_info.append('base_freq')
            if not TDP.get_text().strip(): missing_info.append('TDP')

            # get the rest of the data from link
            print(f"fetching url : {base_url}{link}")
            get_cpu_data(base_url+link, missing_info)
            print('data fetched success fully!!')
            print()
            # increment row count
            row_count += 1

if __name__ == "__main__":
    main()
    # output the data to a parquet file
    df = pd.DataFrame(data)
    df.to_csv('cpu.csv')