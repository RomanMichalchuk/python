import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import random

def fetch_keyword_data(domain, session):
    url = f"https://www.bukvarix.com/site/?q={domain}&region=gmsk&v=cloud"
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        report_header = soup.find('div', class_='report-header')
        if report_header:
            header_text = report_header.find('h2').get_text()
            keywords_count = int(header_text.split('найдено ключевых слов:')[1].split()[0])
        else:
            keywords_count = 0

        script = soup.find('script', string=re.compile('var word_list = new Array'))
        keywords_list = ""
        if script:
            # print("Script content:", script.string)  # Логирование содержимого скрипта
            words = re.findall(r'text:"([^"]*)"', script.string)
            keywords_list = ', '.join(words)
            # print("Extracted words:", words)  # Вывод лога извлеченных слов
        # else:
            # print("No script tag found matching the criteria.")

        return keywords_count, keywords_list
    except Exception as e:
        print(f"Error processing domain {domain}: {e}")
        return 0, ""

def main():
    file_path = 'Check1.xlsx'  # Путь к файлу Excel для результатов
    txt_file_path = 'E:/Folder/Dom15.txt'  # Путь к текстовому файлу с доменами

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        domains = [line.strip() for line in file if line.strip()]

    results_df = pd.DataFrame(columns=['Domain', 'Keyword Count', 'Keywords List'])
    total_domains = len(domains)

    with requests.Session() as session:
        for i, domain in enumerate(domains):
            keyword_count, keywords_list = fetch_keyword_data(domain, session)
            new_row = pd.DataFrame({
                'Domain': [domain],
                'Keyword Count': [keyword_count],
                'Keywords List': [keywords_list]
            })
            results_df = pd.concat([results_df, new_row], ignore_index=True)

            # Добавление рандомной паузы от 3 до 7 секунд
            time.sleep(random.randint(3, 7))

            print(f"Progress: {((i + 1) / total_domains) * 100:.2f}% Complete")

    results_df.to_excel(file_path, index=False)
    print("Data has been successfully written to Excel.")

if __name__ == '__main__':
    main()
