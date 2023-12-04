import requests
from bs4 import BeautifulSoup
import json
import time

no_of_pages = 10000
URL = f'https://instante.justice.md/ro/hotaririle-instantei?Instance=All&Numarul_dosarului=&Denumirea_dosarului=&date=&Tematica_dosarului=&Tipul_dosarului=All&items_per_page={no_of_pages}&page='

list_of_instances = {}
try:
    j = 0
    i = 0
    start_i = time.perf_counter()
    for i in range(100):
        start = time.perf_counter()
        r = requests.get(URL + str(i))
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find("table").find("tbody").find_all('tr')
        column_names = ["Instante Judecatoresti", "Numarul Dosarului", "Denumirea Dosarului", "Data pronuntarii", "Data inregistrarii", "Data publicarii", "Tipul Dosarului", "Tematica Dosarului", "Judecator"]
        for row in rows:
            columns = row.find_all("td")
            dic = {name: column.text.strip() for name, column in zip(column_names, columns)}
            dic["PDF"] = "https://instante.justice.md/ro/" + columns[-1].a["href"]
            print(j)
            list_of_instances[j] = dic
            j += 1
        end = time.perf_counter()
        print("this batch: ", end - start)
        print("total: ", end - start_i)

    #can only be stopped by keyboardinterrupt, or other errors
except KeyboardInterrupt:
    json_string = json.dumps(list_of_instances, indent=4, ensure_ascii=False)
    with open('./../DB/db_instante.json', 'w', encoding='utf-8') as f:
        f.write(json_string)