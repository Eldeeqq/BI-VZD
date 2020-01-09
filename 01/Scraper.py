import os.path as path

from scrapers import old, new


def _check_files():
    if not path.exists('data/results.csv'):
        with open('data/summary.csv', 'w') as f:
            f.write(';'.join(['rok', 'hlasy', 'zpracovano', 'zpracovano_procenta',
                              'zastupitelstva', 'zvolena_zastupitelstva', 'volici',
                              'vydane_obalky', 'ucast_procenta', 'odevzdane_obalky',
                              'platne_hlasy']) + '\n')

    if not path.exists('data/party_votes.csv'):
        with open('data/party_votes.csv', 'w') as f:
            f.write(';'.join(['rok', 'por_c_strany', 'strana', 'hlasy', 'hlasy_procenta',
                              'zastupitele', 'zastupitele_procenta']) + '\n')

    if not path.exists('data/candidates.csv'):
        with open('data/candidates.csv', 'w') as f:
            f.write(';'.join(['rok', 'strana_id', 'strana', 'poradove_cislo', 'jmeno',
                              'tituly', 'vek', 'navrhovana_str', 'prislusnost', 'hlasy',
                              'hlasy_procenta', 'poradi', 'mandat']) + '\n')


def scrape(city):
    _check_files()
    print("Scraping results...")
    old.scrape(city)
    new.scrape(city)
    print("Scraping done!")


if __name__ == "__main__":
    scrape(city='Plzeň')
