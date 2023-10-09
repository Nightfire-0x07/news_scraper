import requests
from bs4 import BeautifulSoup, SoupStrainer

def check_dupes(old_list):
    unique_list = []
    for item in old_list:
        if item not in unique_list:
            unique_list.append(item)
    return(unique_list) 

def pull_article(source_list):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 uacq'}
    site_map = []
    i = 0
    for s in source_list:
        i = i + 1
        response = requests.get(s, headers=headers)
        file = open(r"site/"+ str(i) + ".html", "w+")
        text_list = []
        for text in BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer('p')):
            if 'p style' in text:
                text_list.remove(text)
            else:
                text_list.append(text)
        for text in text_list:
            file.writelines(str(text))
            file.close

parser = 'html.parser'
url_list = ['https://www.bleepingcomputer.com/']#'https://thehackernews.com/']
#,'https://www.malwarebytes.com/blog/category/news']

headers = {'user-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian'}

for url in url_list:
    news_list = []
    fixed_list = []
    response = requests.get(url, headers=headers)
    for link in BeautifulSoup(response.content, parser, parse_only=SoupStrainer('a')):
        if link.has_attr("href"):
            news_list.append((link['href']))

    if url == 'https://www.bleepingcomputer.com/':
        for n in news_list:
            if "security" not in n:
                try:
                    news_list.remove(n)
                except:
                    None
            else:
              fixed_list.append(n.strip())

        for item in fixed_list:
            if fixed_list.count(item) > 1 or "forums/index" in item or "offer/deals" in item or "security/page" in item:
                fixed_list.remove(item)

    if url == 'https://thehackernews.com/':
        #block_list = ["thn.news", "searchlabel", "javascript:void", "about-us", "careers", "advertising", "submit-news", "facebook", "instagram", "twitter", "linkedin", "youtube", "deals.thehackernews"]
        block_list = ["facebook", "twitter", "youtube"]
        for n in news_list:
            for b in block_list:
                if b in n:
                    blockword_hit = True

            if blockword_hit != True:
                fixed_list.append(n)
    fixed_list = check_dupes(fixed_list)
    pull_article(fixed_list)
    title_list = []

    if url == 'https://www.bleepingcomputer.com/':
        print("<h1> Bleeping Computer </h1>")
        for f in fixed_list:
            formatted_domain = f.replace('https://www.bleepingcomputer.com/news/security/','')
            formatted_title = formatted_domain.replace('-',' ')
            formatted_title = formatted_title.replace('/', '')
            title_list.append(formatted_title)
            print("<a href=" + f + " target='_blank' style='text-decoration:none !important;'>")
            print("<h2>" + formatted_title + "</h2></a>")
    if url == 'https://thehackernews.com/':
        print("<h1> Hacker News </h1>")
        for f in fixed_list:
            formatted_domain = f.replace('https://thehackernews.com/','')
            formatted_title = formatted_domain.replace('-', ' ')
            formatted_title = formatted_title.replace('/', '')
            formatted_title = formatted_title.replace('.html', '')
            formatted_title = formatted_title[6:]
            title_list.append(formatted_title)
            print("<a href=" + f + " target='_blank' style='text-decoration:none !important;'>")
            print("<h2>" + formatted_title + "</h2></a>")
#    if url == 'https://www.malwarebytes.com/blog/category/news':
#        for f in fixed_list:
#            print(f)
