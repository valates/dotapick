from constantNames import SORT_INPUTS

""" Sorts the heroes not prunes stored in the list HEROESLEFT. Uses
    the contents dictionary HEROADVMAP which contains the % advantage
    each hero in list PICKEDHEROES has against the hero in HEROESLEFT.
    Sorts based on the string specifier SORTOPTION. """


def perform_sort(heroes_left, hero_adv_map, picked_heroes, sort_option):
    if ((sort_option == SORT_INPUTS[-1]) or (len(picked_heroes) == 0)):
        picked_header = ''
        for hero in picked_heroes:
            picked_header += '{:>20}'.format(hero)
        print('{:<20}'.format("Hero") + picked_header)
        full_output = ''
        for hero in heroes_left:
            hero_display = '{:<20}'.format(hero)
            adv_stats = ''
            for adv in hero_adv_map[hero]:
                adv_stats += '{:>20}'.format(adv)
            full_output += (hero_display + adv_stats + '\n')
        print(full_output)
        return full_output
    else:
        sort_values = []
        for hero in heroes_left:
            hero_advantages = hero_adv_map[hero]
            hero_tuple = (hero, hero_advantages)
            sort_values.append(hero_tuple)
        if (sort_option in SORT_INPUTS[:2]):
            sum_list = []
            for entry in sort_values:
                entry_name = entry[0]
                entry_list = entry[1]
                entry_sum = 0
                for value in entry_list:
                        entry_sum += value
                if (sort_option == SORT_INPUTS[1]):
                        entry_sum /= len(picked_heroes)
                sum_tuple = (entry_name, entry_sum)
                sum_list.append(sum_tuple)
            sum_list = sorted(sum_list, key=lambda cur_sum: cur_sum[1],
                              reverse=True)
            full_output = ''
            for sum_entry in sum_list:
                hero_display = '{:<20}'.format(sum_entry[0]) + '\t\t \
                                ' + '{0:.2f}'.format(sum_entry[1])
                full_output += (hero_display + '\n')
            print(full_output)
            return full_output
        else:
            if (sort_option in SORT_INPUTS[2:]):
                sort_option = int(sort_option)
                if (sort_option <= len(picked_heroes)):
                    sort_values = sorted(sort_values, key=lambda cur_list: (cur_list[1])[(sort_option - 1)], reverse=True)
                    picked_header = ''
                    for hero in picked_heroes:
                        picked_header += '{:>20}'.format(hero)
                    print('{:<20}'.format("Hero") + picked_header)
                    for sort_entry in sort_values:
                        hero_display = '{:<20}'.format(sort_entry[0])
                        adv_stats = ''
                        for adv in sort_entry[1]:
                            adv_stats += '{:>20}'.format(adv)
                        print(hero_display + adv_stats)
                else:
                    print("Insufficient number of picked heroes to sort by \
                           column '" + str(sort_option) + "'")
            else:
                print("Invalid sorting column '" + sort_option + "'")
