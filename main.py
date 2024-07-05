from parsel import Selector
import requests


def get_links(url: str) -> dict[str, str]:
    response = requests.get(url)
    selector = Selector(text=response.text)

    links_of_class = selector.css(".flex-order-1 a::attr(href)").getall()

    return {
        "followers": links_of_class[1],
        "following": links_of_class[2]}


def get_usernames(url: str) -> list[str]:
    response = requests.get(url)
    selector = Selector(text=response.text)
    txt_next_page = selector.css("a[rel='nofollow']::text").get()
    secondary_names_list = list()

    while txt_next_page == "Next":
        response = requests.get(url)
        selector = Selector(text=response.text)

        secondary_names = selector.css(
            ".d-inline-block.no-underline.mb-1::attr(href)").getall()

        secondary_names_list.extend(secondary_names)

        div_pages = selector.css(".pagination a::attr(href)").getall()

        if (len(div_pages) == 1):
            url = selector.css(".pagination a::attr(href)").getall()[0]
            txt_next_page = selector.css(".pagination a::text").getall()[0]
        else:
            url = selector.css(".pagination a::attr(href)").getall()[1]
            txt_next_page = selector.css(".pagination a::text").getall()[1]

    return secondary_names_list


def get_following_not_follower(url: str) -> list[str]:
    links = get_links(url=url)
    not_follower_list = list()

    followers = get_usernames(url=links["followers"])
    following = get_usernames(url=links["following"])

    for f in following:
        analyse = followers.count(f)
        if analyse == 0:
            not_follower_list.append(f)

    return not_follower_list


# RUN
# modify "url_to_analyse" to see who you follow that doesn't follow you.
url_to_analyse = "https://github.com/moisesfdasilva"
list_following_not_follower = get_following_not_follower(url=url_to_analyse)
print(len(list_following_not_follower))
print(list_following_not_follower)
