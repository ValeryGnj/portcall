import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib

headers = {
    'authority': 'portcall.marinet.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'tzo=-60; PHPSESSID=7ddc006a73f03e5368ad6109c662b600',
    'dnt': '1',
    'referer': 'https://portcall.marinet.ru/seaport.php?Section=wa&Mode=wa&Action=formwaterarea&ID=105900',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

def get_html(url):

    session = requests.Session()

    # HOST = 'https://portcall.marinet.ru/index.php'

    link = 'https://portcall.marinet.ru/index.php'

    header = {'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    data = {"UserName": "aps-kd",
            "PswEncoded": "508389",
            "System": "seaport",
            "Hres":	"",
            "Vres":	"",
            "FullScr": "false",
            "Mode":	"login",
            "EnterComUID": "f444a58d-9bbe-3191-1015-a0c248f95186",
            "login":	"aps-kd",
            "password": "508389",
            }

    response = session.post(link, data=data, headers=header).text
    url = 'https://portcall.marinet.ru/seaport.php?Section=wa&Mode=wa&Action=formwaterarea&ID=105900'
    r = session.get(url, headers=header)
    return r.text


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([data['num'],
                        data['familyname'],
                        data['name'],
                        data['patronicname'],
                        data['rank'],
                        data['rank_by_cert'],
                        data['cert_num'],
                        data['natanality'],
                        data['date_of_berth'],
                        data['place_of_birth'],
                        data['type_doc'],
                        data['num_doc']])

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_="t_muster muster").find_all('tr')

    for tr in trs[1:]:
        crew_member = tr.find_all('td', class_="muster")
        num = crew_member[0].text
        familyname = crew_member[1].text
        name = crew_member[2].text
        patronicname = crew_member[3].text
        rank = crew_member[4].text
        rank_by_cert = crew_member[5].text
        cert_num = crew_member[6].text
        natanality = crew_member[7].text
        date_of_berth = crew_member[8].text
        place_of_birth = crew_member[9].text
        type_doc = crew_member[10].text
        num_doc = crew_member[11].text

        data = {'num': num,
                'familyname': familyname,
                'name': name,
                'patronicname': patronicname,
                'rank': rank,
                'rank_by_cert': rank_by_cert, 
                'cert_num': cert_num,
                'natanality': natanality,
                'date_of_berth': date_of_berth,
                'place_of_birth': place_of_birth,
                'type_doc': type_doc,
                'num_doc': num_doc}

        write_csv(data)

def main():
    url = 'https://portcall.marinet.ru/seaport.php?Section=wa&Mode=wa&Action=formwaterarea&ID=105900'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()

    #print(num, familyname, name,patronicname, rank_by_cert, cert_num, natanality, date_of_berth, place_of_birth, type_doc, num_doc)
    #for td in tds:
    #  name = crew_member[1].text  print(td.text)