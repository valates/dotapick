import requests
from constantNames import HEROES_LIST, ADV_PICKLE_NAME
from shorthand import form_shorthands
from pickleSerializers import save_obj
from htmlOperators import html_searcher, html_search_all

""" Pulls public match data from dotabuff.com for each existing hero. For each
    hero, gets the advantage every other hero has against that hero and stores
    it in a serialized dictionary. """


def pull_dotabuff():
    hero_len = len(HEROES_LIST)
    hero_adv_dict = {}
    data_start = "<table class=\"sortable\">"
    data_end = "</table>"
    adv_start = "<td class=\"cell-xlarge\">"
    adv_cutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
    i = 1
    for hero in HEROES_LIST:
        url = hero.replace(" ", "-")
        url = url.lower()
        url = url.replace("'", "")
        url = "http://www.dotabuff.com/heroes/" + url + "/matchups"
        response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        url_text = response.text
        search_block = html_searcher(data_start, data_end, url_text, False, True)[0]
        advantages = html_search_all(adv_start, adv_cutoff, search_block)
        adv_block = []
        for entry in advantages:
            entry_name = entry[:-5]
            entry_name = entry_name.replace("1", "")
            entry_percent = entry[-5:-1]
            if (entry_name[-1] == '-'):
                entry_name = entry_name[:-1]
                entry_percent = '-' + entry_percent
            entry_tuple = (entry_name, entry_percent)
            adv_block.append(entry_tuple)
        hero_adv_dict[hero] = adv_block
        print('{:<20}'.format(hero) + "\t" + str(i) + "/" + str(hero_len))
        i += 1
    save_obj(hero_adv_dict, ADV_PICKLE_NAME)
    form_shorthands()
