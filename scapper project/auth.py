import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def get_auth_session(url):
    session = requests.Session()
    login_url = urljoin(url, 'wp-login.php')
    session.get(login_url)
    csrf_token = session.cookies['wordpress_test_cookie'].split('|')[1].split(';')[0]

    username = input('Enter your username: ')
    password = input('Enter your password: ')

    login_payload = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'testcookie': '1',
        'redirect_to': urljoin(url, 'wp-admin/'),
        'csrf_token': csrf_token
    }

    session.post(
        login_url,
        data=login_payload,
        headers=dict(referer=login_url)
    )

    return session


def get_subdirectories(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('/') and urlparse(url).hostname in href:
            yield href
            yield from get_subdirectories(session, href)


def check_files(session, url, keyword):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and urlparse(url).hostname in href:
            if href.endswith('.txt'):
                txt_url = urljoin(url, href)
                txt_response = session.get(txt_url)
                if keyword in txt_response.text:
                    yield txt_url
            elif '.' not in href.split('/')[-1]:
                yield from check_files(session, href, keyword)


def scrape(keyword, url):
    session = get_auth_session(url)
    base_url = urlparse(url).scheme + '://' + urlparse(url).hostname

    for url in check_files(session, url, keyword):
        yield url

    for subdirectory in get_subdirectories(session, url):
        for txt_file in check_files(session, subdirectory, keyword):
            yield txt_file
