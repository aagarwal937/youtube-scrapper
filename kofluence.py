from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv

# init session
session = HTMLSession()


def get_video_info(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(sleep=1)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    result = {}
    # video views (converted to integer)
    result["views"] = int(''.join([ c for c in soup.find("span", attrs={"class": "view-count"}).text if c.isdigit() ]))
    # date published
    result["date_published"] = soup.find("div", {"id": "date"}).text[1:]
    # number of likes
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    result["likes"] = int(''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ]))
    # number of dislikes
    result["dislikes"] = int(''.join([ c for c in text_yt_formatted_strings[1].attrs.get("aria-label") if c.isdigit() ]))

    # channel details
    channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
    # channel URL
    channel_url = f"https://www.youtube.com{channel_tag['href']}"
    # number of subscribers as str
    channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
    result['channel'] = {'url': channel_url, 'subscribers': channel_subscribers}
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Video Data Extractor")
    parser.add_argument("url", help="URL of the YouTube video")

    args = parser.parse_args()
    # parse the video URL from command line
    url = args.url

    data = get_video_info(url)

    # print in nice format
    print(f"Views: {data['views']}")
    print(f"Published at: {data['date_published']}")
    print(f"Likes: {data['likes']}")
    print(f"Dislikes: {data['dislikes']}")
    print(f"Channel URL: {data['channel']['url']}")
    print(f"Channel Subscribers: {data['channel']['subscribers']}")

    with open('updated.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(["views" ,
                         "date_published",
                         "likes",
                         "dislikes",
                         "channel url",
                         "channel subscribers"])
