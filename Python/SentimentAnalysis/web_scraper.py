from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


# This script is to scrape the reviews from rottentomatoes.com

movie_names = ['mad_max_fury_road', 'inside_out_2015', 'moonlight_2016', 'get_out', 'justice_league_2017', 'wonder', 'thor_ragnarok_2017', 'daddys_home_2', 'last_airbender', 'pirates_of_the_caribbean_dead_men_tell_no_tales', 'baywatch_2017', 'the_mummy_2017', 'the_dark_tower_2017', 'transformers_the_last_knight_2017', 'the_emoji_movie']
prefix = 'https://www.rottentomatoes.com/m/'
parts = '/reviews/?page='
end = '&sort='
#https://www.rottentomatoes.com/m/wonder/reviews/?page=2&sort=

for movie in movie_names:
    for i in range(1, 15):
        url = prefix + movie + parts + str(i) + end
        print(url)
        
        try:
            uClient = uReq(url)
    
            page_html = uClient.read()
    
            uClient.close()
    
            page_soup = soup(page_html, "html.parser")
    
    
            a = page_soup.find_all(class_='review_icon')
            b = page_soup.find_all(class_ = 'the_review')
            d = {}
    
            for i in range(len(b)):
                d[b[i].string] = a[i]
    
            bad_review = open('bad.txt', 'a+')
            good_review = open('good.txt', 'a+')
    		
            try:
                for k, v in d.items():
                    if 'fresh' in str(v):
                        good_review.write(k + '\n')
                    elif 'rotten' in str(v):
                        bad_review.write(k + '\n')
                    else:
                        raise 'wrong value!'
            except:
                print("Exception: write to file. Continue.")
    
            bad_review.close()
            good_review.close()
        except:
            print("URL error, continue with next iteration.")

