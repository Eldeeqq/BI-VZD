import pandas as pd
import requests
from lxml import etree

_base = 'https://www.volby.cz/pls/kv{0}/'
_uri = 'https://www.volby.cz/pls/kv{0}/kv12?xjazyk=CZ&xid=0'
_candidates = 'https://www.volby.cz/pls/kv{0}/kv22?xjazyk=CZ&xid=0&xv=11'
_years = [2006, 2010, 2014, 2018]
_ns = {"re": "http://exslt.org/regular-expressions"}
_parser = etree.HTMLParser()


def download_city(city: str, year: int):
    base = _base.format(year)
    html = requests.get(_uri.format(year)).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td[re:match(., "^{0}")]'.format(city), namespaces=_ns)[0] \
        .getnext().find('a').attrib['href']

    html = requests.get(base + href).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td[re:match(., "^{0}$")]'.format(city), namespaces=_ns)[0] \
        .getprevious().find('a').attrib['href']

    dfs = pd.read_html(requests.get(base + href).text, decimal=',', thousands='.')

    dfs[0].columns = dfs[0].columns.droplevel(0)
    for x in [5, 6, 8, 9]:
        dfs[0][dfs[0].columns[x]] = dfs[0][dfs[0].columns[x]].str.replace("\s", '')
    cols = dfs[0].columns.values.tolist()
    dfs[0] = dfs[0][[cols[x] for x in [2, 3, 4, 0, 1, 5, 6, 7, 8, 9]]]
    dfs[0].insert(0, 'year', year)
    dfs[0].to_csv('data/summary.csv', index=False, header=False, sep=';', mode='a')

    dfs[1].columns = dfs[1].columns.droplevel(0)
    dfs[1] = dfs[1].drop(columns=dfs[1].columns[4:5])
    dfs[1] = dfs[1][dfs[1].columns[:-1]]
    for x in [2]:
        dfs[1][dfs[1].columns[x]] = dfs[1][dfs[1].columns[x]].str.replace("\s", '')

    dfs[1] = dfs[1].drop(columns=dfs[1].columns[4:5])
    cols = dfs[1].columns.values.tolist()
    dfs[1] = dfs[1][[cols[x] for x in [0, 1, 2, 3, 5, 4]]]
    dfs[1].insert(0, 'year', year)
    dfs[1].to_csv('data/party_votes.csv', index=False, header=False, sep=';', mode='a')


def download_city_candidates(city: str, year: int):
    base = _base.format(year)
    html = requests.get(_candidates.format(year)).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td[re:match(., "^{0}")]'.format(city), namespaces=_ns)[0] \
        .getnext().find('a').attrib['href']
    html = requests.get(base + href).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td[re:match(., "^{0}$")]'.format(city), namespaces=_ns)[0] \
        .getprevious().find('a').attrib['href']
    html = requests.get(base + href).text
    href = etree.fromstring(html, parser=_parser).findall('.//td/a')[0].attrib['href']
    df = pd.read_html(requests.get(base + href).text, decimal=',', thousands='.')[0]
    df.columns = df.columns.droplevel(0)
    df[df.columns[7]] = df[df.columns[7]].str.replace("\s", '')

    if 'Mandát' in df.columns:
        df['mandate'] = [True if x == '*' else False for x in df['Mandát']]
        df = df.drop(columns='Mandát')
    else:
        df = df.insert(loc=len(df.columns) - 1, column='mandate', value=0)

    df.insert(4, 'tituly',
              df[df.columns[3]].apply(lambda x: x[x.find(' ', x.find(' ') + 1) + 1:] if x.count(' ') >= 2 else None))
    df.insert(0, 'year', year)
    df.to_csv('data/candidates.csv', index=False, header=False, sep=';', mode='a')


def scrape(city: str):
    for x in _years:
        print(f"Scraping {x}", end=' ')
        download_city(city, x)
        download_city_candidates(city, x)
        print("✓")


if __name__ == "__main__":
    a = scrape('Plzeň')
