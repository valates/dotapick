import requests
from constantNames import HEROES_LIST, ADV_PICKLE_NAME, OVERALL_PICKLE_NAME, BRACKET_PICKLE_NAME
from shorthand import form_shorthands
from pickleSerializers import save_obj
from htmlOperators import html_searcher, html_search_all

""" Pulls public match data from dotabuff.com for each existing hero. For each
    hero, gets the advantage every other hero has against that hero and stores
    it in a serialized dictionary. """


def pull_dotabuff():
    hero_len = len(HEROES_LIST)
    hero_adv_dict = {}
    hero_winrate_dict = {}
    data_start = "<table class=\"sortable\">"
    data_end = "</table>"
    adv_start = "<td class=\"cell-xlarge\">"
    adv_cutoff = "<div class=\"bar bar-default\"><div class=\"segment segment-advantage\""
    winrate_start = "</dt></dl><dl><dd>"
    winrate_end = "</span></dd>"
    i = 1
    for hero in HEROES_LIST:
        url = hero.replace(" ", "-")
        url = url.lower()
        url = url.replace("'", "")
        url = "http://www.dotabuff.com/heroes/" + url
        response = requests.get(url + "/matchups", headers={'User-agent': 'your bot 0.1'})
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

        response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        url_text = response.text
        winrate = html_searcher(winrate_start, winrate_end, url_text, False, False)[0]
        hero_winrate_dict[hero] = float(winrate[:-1])
        print('{:<20}'.format(hero) + "\t" + str(i) + "/" + str(hero_len))
        i += 1
    save_obj(hero_adv_dict, ADV_PICKLE_NAME)
    save_obj(hero_winrate_dict, OVERALL_PICKLE_NAME)
    form_shorthands()
    print('\n\n')


def get_meta():
    meta_data = {}
    data_start = '<table class="sortable no-arrows r-tab-enabled">'
    data_end = "</table>"
    row_start = '<a href="/heroes/'
    row_end = '</div></div></td></tr>'
    url = "http://www.dotabuff.com/heroes/meta"
    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
    url_text = response.text
    search_block = html_searcher(data_start, data_end, url_text, False, True)[0]
    rows = html_search_all(row_start, row_end, search_block)
    rows = [row.split('%') for row in rows]
    rows = [[row[0], float(row[1]), float(row[3]), float(row[5]), float(row[7]), float(row[9])] for row in rows]
    for hero in HEROES_LIST:
        #need to have a less algorithmically horrendous solution
        for row in rows:
            if hero in row[0]:
                meta_data[hero] = row[1:]
                break
    save_obj(meta_data, BRACKET_PICKLE_NAME)
