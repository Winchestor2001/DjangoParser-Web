import requests
from bs4 import BeautifulSoup as bs
# import lxml
from random import randint
from time import sleep, time
from fake_useragent import FakeUserAgent

from .models import Work
from datetime import datetime, timedelta
from googletrans import Translator

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
    

def dj_24freelance_parser():
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
                date = datetime.strptime(date['content'], "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d")
                Work.objects.create(
                    platform='24freelance',

                    title_ru=trans(title.text.strip(), 'ru'),
                    title_en=trans(title.text.strip(), 'en'),
                    title_de=trans(title.text.strip(), 'de'),

                    description_ru=trans(description, 'ru'),
                    description_en=trans(description, 'en'),
                    description_de=trans(description, 'de'),

                    buyer_ru=trans(buyer, 'ru'),
                    buyer_en=trans(buyer, 'en'),
                    buyer_de=trans(buyer, 'de'),

                    category_ru=trans(category.text.strip(), 'ru'),
                    category_en=trans(category.text.strip(), 'en'),
                    category_de=trans(category.text.strip(), 'de'),

                    date=date,
                    url=main_url + title.find('a')['href'],

                    location_ru = trans('Россия', 'ru'),
                    location_en = trans('Россия', 'en'),
                    location_de = trans('Россия', 'de'),
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
                if title.text.strip() and desctiption.text.strip():
                    date = date.text.strip().replace("Listed:", "").strip()
                    new_date = datetime.strptime(str(date), "%d.%m.%Y")
                    Work.objects.create(
                        platform='freelancermap',

                        title_ru=trans(title.text.strip(), 'ru'),
                        title_en=trans(title.text.strip(), 'en'),
                        title_de=trans(title.text.strip(), 'de'),

                        description_ru=trans(desctiption.text.strip(), 'ru'),
                        description_en=trans(desctiption.text.strip(), 'en'),
                        description_de=trans(desctiption.text.strip(), 'de'),

                        date=new_date,
                        url='https://www.freelancermap.com' + title['href'],

                        location_ru = trans(location.text.strip(), 'ru'),
                        location_en = trans(location.text.strip(), 'en'),
                        location_de = trans(location.text.strip(), 'de'),
                )
        except Exception as ex:
            print(ex)
            continue
        r.close()


def freelancer_parser():
    for page in range(1, 50):
        try:
            url = f'https://www.freelancer.com/jobs/{page}/?results=100'
            r = requests.get(url, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'JobSearchCard-primary-heading-link'})
            dates = soup.find_all(attrs={'class': 'JobSearchCard-primary-heading-days'})
            descriptions = soup.find_all(attrs={'class': 'JobSearchCard-primary-description'})

            for title, desctiption in zip(titles, descriptions):
                if title.text.strip() and desctiption.text.strip():
                    Work.objects.create(
                            platform='freelancer',

                            title_ru=trans(title.text.strip(), 'ru'),
                            title_en=trans(title.text.strip(), 'en'),
                            title_de=trans(title.text.strip(), 'de'),

                            description_ru=trans(desctiption.text.strip(), 'ru'),
                            description_en=trans(desctiption.text.strip(), 'en'),
                            description_de=trans(desctiption.text.strip(), 'de'),

                            date=datetime.now() - timedelta(days=6),
                            url='https://www.freelancer.com' + title['href'],

                            location_ru = trans('Australia', 'ru'),
                            location_en = trans('Australia', 'en'),
                            location_de = trans('Australia', 'de'),
                    )
            r.close()
        except:
            pass


def flexjobs_parser():
    for page in range(1, 35):
        try:
            url = f'https://www.flexjobs.com/remote-jobs/account-management?page={page}'
            link = url.format(page)
            r = requests.get(link, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'job-title job-link'})
            dates = soup.find_all(attrs={'class': 'job-age'})
            descriptions = soup.find_all(attrs={'class': 'job-description'})
            locations = soup.find_all(attrs={'class': 'job-locations'})

            for title, date, desctiption, location in zip(titles, dates, descriptions, locations):
                if title.text.strip() and desctiption.text.strip():
                    Work.objects.create(
                        platform='flexjobs',

                        title_ru=trans(title.text.strip(), 'ru'),
                        title_en=trans(title.text.strip(), 'en'),
                        title_de=trans(title.text.strip(), 'de'),

                        description_ru=trans(desctiption.text.strip(), 'ru'),
                        description_en=trans(desctiption.text.strip(), 'en'),
                        description_de=trans(desctiption.text.strip(), 'de'),

                        date=flexjobs_date(date.text.strip().replace("Listed:", "").strip()),
                        url='https://www.flexjobs.com' + title['href'],

                        location_ru = trans(location.text.strip(), 'ru'),
                        location_en = trans(location.text.strip(), 'en'),
                        location_de = trans(location.text.strip(), 'de'),
                )
        except:
            pass


def fl_parser():
    for page in range(1, 50):
        try:
            url = f'https://www.fl.ru/projects/?page={page}&kind=5'
            r = requests.get(url, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'b-post__link'})
            descriptions = soup.find_all(attrs={'class': 'b-post__txt'})
            date = datetime.now() - timedelta(days=randint(1, 5))
            locations = 'Россия'
            for title, description in zip(titles, descriptions):
                if title.text.strip() and description.text.strip() != 'Исполнитель определён':
                    Work.objects.create(
                            platform='fl',

                            title_ru=trans(title.text.strip(), 'ru'),
                            title_en=trans(title.text.strip(), 'en'),
                            title_de=trans(title.text.strip(), 'de'),

                            description_ru=trans(description.text.strip(), 'ru'),
                            description_en=trans(description.text.strip(), 'en'),
                            description_de=trans(description.text.strip(), 'de'),

                            url='https://www.flexjobs.com' + title['href'],

                            location_ru = trans(locations, 'ru'),
                            location_en = trans(locations, 'en'),
                            location_de = trans(locations, 'de'),

                            date=date
                    )
        except Exception as ex:
            print(ex)


def weblancer_parser():
    for page in range(1, 50):
        try:
            link = f"https://www.weblancer.net/jobs/?page={page}"
            r = requests.get(link, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'title'})
            dates = soup.find_all(attrs={'class': 'col-sm-4 text-sm-end'})
            descriptions = soup.find_all(attrs={'class': 'text_field text-inline'})
            categories = soup.find_all(attrs={'class': 'col-sm-8 text-muted dot_divided text_field d-sm-flex'})
            for title, date, desctiption, category in zip(titles, dates, descriptions, categories):
                if title.text.strip() and desctiption.text.strip() and category:
                    url = title.find('a')['href']
                    Work.objects.create(
                        platform='weblancer',

                        title_ru=trans(title.text.strip(), 'ru'),
                        title_en=trans(title.text.strip(), 'en'),
                        title_de=trans(title.text.strip(), 'de'),

                        description_ru=trans(desctiption.text.strip(), 'ru'),
                        description_en=trans(desctiption.text.strip(), 'en'),
                        description_de=trans(desctiption.text.strip(), 'de'),

                        category_ru=trans(category.text.strip(), 'ru'),
                        category_en=trans(category.text.strip(), 'en'),
                        category_de=trans(category.text.strip(), 'de'),

                        url='https://www.weblancer.net' + url,
                        date=weblancer_date(date.text.strip()),
                )
        except:
            continue
        r.close()


def theprotocol_parser():
    for page in range(1, 50):
        try:
            link = f"https://www.projects2bid.com/freelance-jobs/page/{page}/?sort=new-old"
            r = requests.get(link, headers=agent)
            soup = bs(r.content, 'html.parser')
            titles = soup.find_all(attrs={'class': 'fr-right-details2'})
            locations = soup.find_all(attrs={'class': 'fr-right-list'})
            categories = soup.find_all(attrs={'class': 'fr-right-product'})
            descriptions = soup.find_all(attrs={'class': 'fr-right-index'})
            for title, description, location, category in zip(titles, descriptions, locations, categories):
                description = None if description.text is None else description.text.strip()
                if len(title.text.strip()) > 3 and description and category.text.strip() and location:
                    url = title.find('a')['href']
                    loca = location.find('ul').find_all('span')[-1].text.strip()
                    location = 'None' if 'Received' in loca else loca
                    Work.objects.create(
                        platform='projects2bid',

                        title_ru=trans(title.text.strip(), 'ru'),
                        title_en=trans(title.text.strip(), 'en'),
                        title_de=trans(title.text.strip(), 'de'),

                        description_ru=trans(description, 'ru'),
                        description_en=trans(description, 'en'),
                        description_de=trans(description, 'de'),

                        category_ru=trans(category.text.strip(), 'ru'),
                        category_en=trans(category.text.strip(), 'en'),
                        category_de=trans(category.text.strip(), 'de'),

                        url=url,
                        date = datetime.now(),

                        location_ru = trans(location, 'ru'),
                        location_en = trans(location, 'en'),
                        location_de = trans(location, 'de'),
                )
        except Exception as ex:
            print(ex)
            continue
        r.close()



def trans(text, lang):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    return translation.text


def weblancer_date(date: str):
    date_split = date.split()
    if date_split[1] in ['недели', 'неделю']:
        new_date = datetime.now() - timedelta(weeks=int(date_split[0]))
        return new_date

    elif date_split[1] in ['день', 'дня']:
        new_date = datetime.now() - timedelta(days=int(date_split[0]))
        return new_date

    elif date_split[1] in ['секунд', 'минуту', 'минуты', 'час', 'часа']:
        return datetime.now()
    else:
        new_date = datetime.now()
        return new_date


def flexjobs_date(date: str):
    if 'Today' in date:
        return datetime.now()

    if 'Yesterday' in date:
        new_date = datetime.now() - timedelta(days=1)
        return new_date

    date_split = date.split()
    if date_split[1] == 'days':
        new_date = datetime.now() - timedelta(days=int(date_split[0]))
        return new_date

    elif date_split[0] == '30+':
        new_date = datetime.now() - timedelta(days=30)
        return new_date
    else:
        new_date = datetime.now()
        return new_date

