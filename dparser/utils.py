import requests
from bs4 import BeautifulSoup as bs
# import lxml
from random import randint
from time import sleep, time
from fake_useragent import FakeUserAgent

from .models import Work
from datetime import datetime, timedelta

main_url = 'https://24freelance.pro'
category_routes = [
    {'Разработка для WEB': 'https://24freelance.pro/projects/razrabotka-dlya-web/'},
    {'Разработка программ': 'https://24freelance.pro/projects/razrabotka-po/'},
    {'Разработка мобильных приложений': 'https://24freelance.pro/projects/razrabotka-mobilnyh-prilozhenij/'},
    {'Администрирование': 'https://24freelance.pro/projects/administrirovanie/'},
    {'Дизайн и Мультимедиа': 'https://24freelance.pro/projects/dizajn-i-multimedia/'},
    {'Фотография': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'3D графика': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'Тексты и Перевод': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'Обучение и Консультации': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'Инжиниринг. Чертежи': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'Реклама и Маркетинг': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'SMM и SEO продвижение': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
    {'Другое Разное': 'https://24freelance.pro/projects/fotografiya-photo-rabota-s-fotografiyami/'},
]

ua = FakeUserAgent()
agent = {
    'User-agent': f'{ua.random}'
}
    

def _24freelance_parser():
    for url in category_routes:
        key = [i for i in url.keys()]
        url = url[key[0]]
        # print(f"\n******{key[0]}******\n")
        r = requests.get(url, headers=agent)
        soup = bs(r.content, 'html.parser')
        titles = soup.find_all('h2', attrs={'class': 'title'})
        categories = soup.find_all('span', attrs={'itemprop': 'articleSection'})
        descriptions = soup.find_all('div', attrs={'class': 'description'})
        dates = soup.find_all('div', attrs={'class': 'date'})
        for title, category, description, date in zip(titles, categories, descriptions, dates):
            if len(title.text.strip()) > 3:
                r2 = requests.get(main_url + title.find('a')['href'])
                soup2 = bs(r2.content, 'html.parser')
                description = soup2.find('div', attrs={'class': 'description clear'}).text.strip()
                buyer = soup2.find('div', attrs={'class': 'middle'}).find('h2').text.strip()
                Work.objects.create(
                    platform='24freelance',
                    title=title.text.strip(),
                    description=description,
                    buyer=buyer,
                    category=category.text.strip(),
                    date=date.text.strip(),
                    url=main_url + title.find('a')['href'],
                    location = 'Россия'
                )

                r2.close()
        r.close()


def freelancermap_parser():
    for page in range(1, 50):
        try:
            link = f"https://www.freelancermap.com/it-projects.html?pagenr={page}"
            r = requests.get(link, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'project-title'})
            dates = soup.find_all(attrs={'class': 'created-date'})
            descriptions = soup.find_all(attrs={'class': 'description'})
            locations = soup.find_all(attrs={'class': 'project-location'})
            for title, date, desctiption, location in zip(titles, dates, descriptions, locations):
                if len(title.text.strip()) > 3 and len(desctiption.text.strip()) > 5:
                    Work.objects.create(
                        platform='freelancermap',
                        title=title.text.strip(),
                        description=desctiption.text.strip(),
                        date=date.text.strip().replace("Listed:", "").strip(),
                        url='https://www.freelancermap.com' + title['href'],
                        location = location.text.strip(),
                        work_lang='de'
                )
        except:
            continue
        r.close()


def freelancer_parser():
    try:
        url = 'https://www.freelancer.com/jobs/?results=100'
        r = requests.get(url, headers=agent)
        soup = bs(r.content, 'html.parser')
        titles = soup.find_all(attrs={'class': 'JobSearchCard-primary-heading-link'})
        dates = soup.find_all(attrs={'class': 'JobSearchCard-primary-heading-days'})
        descriptions = soup.find_all(attrs={'class': 'JobSearchCard-primary-description'})

        for title, date, desctiption in zip(titles, dates, descriptions):
            if len(title.text.strip()) > 3 and len(desctiption.text.strip()) > 5:
                Work.objects.create(
                        platform='freelancer',
                        title=title.text.strip(),
                        description=desctiption.text.strip(),
                        date=date.text.strip(),
                        url='https://www.freelancer.com' + title['href'],
                        location = 'Australia',
                        work_lang='en'
                )
        r.close()
    except:
        pass


def flexjobs_parser():
    for page in range(1, 35):
        try:
            url = 'https://www.flexjobs.com/remote-jobs/account-management?page={}'
            link = url.format(page)
            r = requests.get(link, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'job-title job-link'})
            dates = soup.find_all(attrs={'class': 'job-age'})
            descriptions = soup.find_all(attrs={'class': 'job-description'})
            locations = soup.find_all(attrs={'class': 'job-locations'})

            for title, date, desctiption, location in zip(titles, dates, descriptions, locations):
                if len(title.text.strip()) > 3 and len(desctiption.text.strip()) > 5:
                    Work.objects.create(
                        platform='flexjobs',
                        title=title.text.strip(),
                        description=desctiption.text.strip(),
                        date=date.text.strip().replace("Listed:", "").strip(),
                        url='https://www.flexjobs.com' + title['href'],
                        location = location.text.strip(),
                        work_lang='en'
                )
        except:
            pass


def fl_parser():
    try:
        url = 'https://www.fl.ru/projects/?kind=5'
        r = requests.get(url, headers=agent)
        soup = bs(r.content, 'html.parser')
        titles = soup.find_all(attrs={'class': 'b-post__link'})
        descriptions = soup.find_all(attrs={'class': 'b-post__txt'})
        locations = 'Россия'
        for title, desctiption in zip(titles, descriptions):
            if len(title.text.strip()) > 3 and len(desctiption.text.strip()) > 5:
                Work.objects.create(
                        platform='fl',
                        title=title.text.strip(),
                        description=desctiption.text.strip(),
                        url='https://www.flexjobs.com' + title['href'],
                        location = locations,
                )
    except Exception as ex:
        pass



