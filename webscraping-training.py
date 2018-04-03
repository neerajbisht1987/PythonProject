import urllib2
from selenium import webdriver

moneycontrol = "http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap.html"
moneycontrol = "http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/small-and-mid-cap.html"
wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
prefix = "http://www.moneycontrol.com"

urldict = {}
rankdict = {}
equity_count = {}
browser = webdriver.Chrome("/Users/bishtnee/Downloads/chromedriver")
browser.get(moneycontrol)
page = browser.page_source
browser.close()
browser.quit()
# page=urllib2.urlopen(moneycontrol)
from bs4 import BeautifulSoup

soup = BeautifulSoup(page, "html.parser")
import pdb

table = soup.html.body.find('table', {'class': 'gry_t thdata'}).tbody
mutual_fund_scheme_index = 0
rank_index = 0;
# print table.prettify()
for row in table.find_all('tr'):
    index = 0
    for col in row.find_all('th'):
        if col.a and col.a.span and col.a.span.strong:
            if col.a.span.strong.string == 'Crisil Rank':
                rank_index = index
            if col.a.span.strong.string == 'Mutual Fund Scheme':
                mutual_fund_scheme_index = index
            index = index + 1
    break
print 'rank_index:', rank_index
print 'mutual_fund_scheme_index:', mutual_fund_scheme_index
# pdb.set_trace()
for row in table.find_all('tr'):
    # print row
    col = row.find_all('td')
    if row.find('table'):
        tablebody = row.find('table').tbody
        if tablebody:
            col = tablebody.find_all('td')
            if col:
                if col[rank_index].a.string == 'Rank 1' or col[rank_index].a.string == 'Rank 2' and col[
                    mutual_fund_scheme_index].span.string.find('Direct') != -1:
                    urldict[col[mutual_fund_scheme_index].span.string] = col[mutual_fund_scheme_index].span['href']
                    rankdict[col[mutual_fund_scheme_index].span.string] = col[rank_index].a.string
            # print col
    elif col and col[0].find('a'):
        if col[rank_index].a.string == 'Rank 1' or col[rank_index].a.string == 'Rank 2' and col[
            mutual_fund_scheme_index].a.string.find('Direct') != -1:
            urldict[col[mutual_fund_scheme_index].a.string] = col[mutual_fund_scheme_index].a['href']
            rankdict[col[mutual_fund_scheme_index].a.string] = col[rank_index].a.string;
# pdb.set_trace()
portfolio_add = set()
for (urlname, urladd) in urldict.items():
    browser = webdriver.Chrome("/Users/bishtnee/Downloads/chromedriver")
    url = prefix + urladd
    browser.get(url)
    page = browser.page_source
    browser.close()
    browser.quit()
    soup = BeautifulSoup(page, "html.parser")
    acct = soup.find_all('ul', {'class': 'acCONT'})
    if acct:
        li = acct[4].find_all('li')
        if li:
            recurl = li[1].a['href']
            portfolio_add.add(recurl)

for add in portfolio_add:
    url = prefix + add
    browser = webdriver.Chrome("/Users/bishtnee/Downloads/chromedriver")
    browser.get(url)
    page = browser.page_source
    browser.close()
    browser.quit()
    soup = BeautifulSoup(page, "html.parser")
    # table[@class='tblporhd']
    equity_index = 0
    qty_index = 0
    table = soup.html.body.find('table', {'class': 'tblporhd'}).tbody
    for row in table.find_all('tr'):
        index = 0
        for col in row.find_all('th'):
            if col and col.string and col.string.strip() == 'Equity':
                equity_index = index
            if col and col.string and col.string.strip() == 'Qty':
                qty_index = index
            index = index + 1
        break
    for row in table.find_all('tr'):
        col = row.find_all('td')
        if col:
            eq = col[equity_index].string.strip()
            if eq in equity_count:
                equity_count[eq] = equity_count[eq] + 1
            else:
                equity_count[eq] = 1
            qty = col[qty_index].string
        # print eq ,",",qty
pdb.set_trace()
for (eq, num) in equity_count.items():
    print eq, ",", num
