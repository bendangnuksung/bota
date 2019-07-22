import re, requests
from bs4 import BeautifulSoup as bs

url = 'https://www.dotabuff.com/heroes/trends'
r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
html = r.text

soup = bs(html, "html.parser")
print([item["data-value"] for item in soup.find_all() if "data-value" in item.attrs])
exit()
# tab = soup.find("table", {"class":"sortable r-tab-enabled"})
tab = str(tab)
print(tab)
# headers = re.findall(r'<th[^>]*>([^<]+)', tab)
# print(headers)
rows = re.findall(r'<td>(?:<a[^>]*>)?([^<]+)', tab)
print(rows)
