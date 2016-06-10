import logging
import sqlite3

from selenium import webdriver

SITE_URL = 'http://www.inc.com/inc5000/list/2015/'

conn = sqlite3.connect('scrap.db')

logging.basicConfig(level=logging.INFO)


def main():
    logging.info('Starting application...')

    db_clean()

    driver = webdriver.PhantomJS()

    driver.set_window_size(1920, 1080 * 10)

    driver.get(SITE_URL)

    min_page = int(
        driver.find_element_by_css_selector(
            '#page_tuner > div.gold.box.num-l'
        ).text
    )

    max_page = int(
        driver.find_element_by_css_selector(
            '#page_tuner > div.gold.box.num-r'
        ).text
    )

    next_page_e = driver.find_element_by_css_selector(
        '#page_tuner > div.fa.gold.box.arrow-r'
    )

    more_e = driver.find_element_by_css_selector(
        '#list_headers > div.more'
    )

    logging.info('Starting parse...')

    for page in range(min_page, max_page + 1):
        logging.info('Parsing page %d.', page)

        rows = driver.find_elements_by_css_selector(
            '#right > table > tbody > tr'
        )

        companies = []

        for row in rows:
            if row.text:
                company = {}

                company['rank'] = int(row.find_element_by_css_selector(
                    'td.c1'
                ).text)

                company['name'] = row.find_element_by_css_selector(
                    'td.c2'
                ).text

                company['growth'] = row.find_element_by_css_selector(
                    'td.c3'
                ).text

                company['revenue'] = row.find_element_by_css_selector(
                    'td.c4'
                ).text

                company['industry'] = row.find_element_by_css_selector(
                    'td.c5'
                ).text

                more_e.click()

                company['state'] = row.find_element_by_css_selector(
                    'td.c6'
                ).text

                more_e.click()

                company['metro_area'] = row.find_element_by_css_selector(
                    'td.c7'
                ).text

                more_e.click()

                company['years'] = int(row.find_element_by_css_selector(
                    'td.c9'
                ).text)

                more_e.click()

                companies.append(company)

                logging.info('Parsed: ' + str(company))

        logging.info(
            'Page has been parsed. %d records were found on page %d',
            len(companies),
            page
        )

        db_save(companies)

        next_page_e.click()

    driver.close()


def db_save(companies):
    logging.info('Saving page to database...')

    c = conn.cursor()

    for company in companies:
        c.execute(
            'INSERT INTO companies VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )',
            [
                company['rank'], company['name'], company['growth'],
                company['revenue'], company['industry'], company['state'],
                company['metro_area'], company['years']
            ]
        )

        conn.commit()


def db_clean():
    logging.info('Preparing database...')

    c = conn.cursor()

    c.execute(
        'DROP TABLE IF EXISTS companies'
    )

    c.execute(
        'CREATE TABLE IF NOT EXISTS companies ( '
        'rank INT, name TEXT, growth TEXT, '
        'revenue TEXT, industry TEXT, state TEXT, '
        'metro_area TEXT, years INT '
        ')'
    )

if __name__ == '__main__':
    main()
