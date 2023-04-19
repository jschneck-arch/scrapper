from scrapper import scrape

if __name__ == '__main__':
    keyword = input('Enter the keyword: ')
    url = input('Enter the URL: ')
    username = input('Enter the username (leave blank for public sites): ')
    password = input('Enter the password (leave blank for public sites): ')

    urls = list(scrape(keyword, url, username=username, password=password))

    if urls:
        print(f'Found {len(urls)} URLs:')
        for url in urls:
            print(url)
    else:
        print('No URLs found.')
