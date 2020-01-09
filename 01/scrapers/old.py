import pandas as pd
import requests
from lxml import etree

_old_uri = 'https://www.volby.cz/pls/kv2002/kv12?xjazyk=CZ&xid=0'
_old_candidates = 'https://www.volby.cz/pls/kv2002/kv22?xjazyk=CZ&xid=0&xv=11'
_old_base = 'https://www.volby.cz/pls/kv2002/'
_ns = {"re": "http://exslt.org/regular-expressions"}
_parser = etree.HTMLParser()


def format_candidates(df):
    df.columns = df.columns.droplevel(0)
    if 'Mandát' in df.columns:
        df['mandate'] = [True if x == '*' else False for x in df['Mandát']]
        df = df.drop(columns='Mandát')
    else:
        df = df.insert(loc=len(df.columns) - 1, column='mandate', value=0)
    return df


def download_city(city: str):
    html = requests.get(_old_uri).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td[re:match(., "^{0}")]'.format(city), namespaces=_ns)[0] \
        .getparent().getchildren()[0].find('a').attrib['href']
    html = requests.get(_old_base + href).text
    href = etree.fromstring(html, parser=_parser).xpath('.//a[re:match(., "^3$")]', namespaces=_ns)[0].attrib['href']
    dfs = pd.read_html(_old_base + href, flavor='html5lib')

    for x in [5, 6, 8, 9]:
        dfs[0][dfs[0].columns[x]] = dfs[0][dfs[0].columns[x]].str.replace("\s", '')

    dfs[0].insert(0, 'year', 2002)
    dfs[0].to_csv('data/summary.csv', index=False, header=False, sep=';', mode='a')

    dfs[1][dfs[1].columns[1]] = dfs[1][dfs[1].columns[1]].str.replace("\s", '')
    dfs[1].insert(0, 'id', range(1, len(dfs[1]) + 1))
    dfs[1].insert(0, 'year', 2002)
    dfs[1].to_csv('data/party_votes.csv', index=False, header=False, sep=';', mode='a')


def download_city_candidates(city: str):
    html = requests.get(_old_candidates).text
    href = etree.fromstring(html, parser=_parser) \
        .xpath('.//td[re:match(., "^{0}") and not (@colspan)]'.format(city), namespaces=_ns)[0] \
        .getnext().find('a').attrib['href']

    html = requests.get(_old_base + href).text
    href = etree.fromstring(html, parser=_parser) \
        .xpath('.//td[re:match(., "^3$")]', namespaces=_ns)[0].getparent().getchildren()[0].find('a').attrib['href']

    html = requests.get(_old_base + href).text
    href = etree.fromstring(html, parser=_parser).xpath('.//td/a')[0].attrib['href']
    df = pd.read_html(_old_base + href, flavor='html5lib')[0]
    df = format_candidates(df)
    df['abs.'] = df['abs.'].str.replace("\s", '')
    df.insert(0, 'year', 2002)
    df.to_csv('data/candidates.csv', index=False, header=False, sep=';', mode='a')


def scrape(city: str):
    print('Scraping 2002', end=' ')
    download_city(city)
    download_city_candidates(city)
    print('✓')


if __name__ == "__main__":
    city = 'Plzeň'
    download_city(city)
    download_city_candidates(city)
