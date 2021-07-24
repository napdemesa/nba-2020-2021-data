from bs4 import BeautifulSoup

import time
import requests
import pandas as pd


def get_player_page_yuh(url):
    players = []
    players_urls = []
    team_page = requests.get(url)
    soup = BeautifulSoup(team_page.text, 'lxml')
    team_players_table = soup.find('table', class_='sortable stats_table').find('tbody')
    player_list = team_players_table.find_all('a', href=True)

    for player in player_list:
        if '/friv/' not in player['href']:
            players.append(player.text)
            players_urls.append(f"https://www.basketball-reference.com{player['href'][:-5]}/gamelog/2021")

    return players, players_urls


def get_player_regular_season_stats(player_season_url):
    #player_season_stats = {'player': []}
    try:
        player_season_page = requests.get(player_season_url)
    except Exception as e:
        print('Couldn\'t grab player URL...')
    soup = BeautifulSoup(player_season_page.text, 'lxml')
    try:
        player_season_table = soup.find('table', class_='row_summable sortable stats_table')
        table_summary = player_season_table.find_all('tr')
    except Exception as e:
        print('Couldn\'t find player data for this season...')
        return ''
    #for game in table_summary[1:]:
    #    if game.has_attr('class') and game['class'][0] == 'thead':
    #        continue
    #    else:
    #        game = list(game)
    #        if game[-1].text in ('Inactive', 'Did Not Dress', 'Did Not Play'):
    #            print('Player did not play... Skipping...')
    #            continue
    #        else:
    #            print('Getting player game stats...')
    ##            player_season_stats['player'].append(player_name)
    #            for stat in game:
    #                if stat.get('data-stat') not in player_season_stats:
    #                    player_season_stats[stat.get('data-stat')] = []
    #                    player_season_stats[stat.get('data-stat')].append(stat.text)
    #                else:
    #                    player_season_stats[stat.get('data-stat')].append(stat.text)

    print('Fetched game stats...')
    return table_summary


def parse_player_data(table_summary, player_name):
    player_season_stats = {'player': []}

    for game in table_summary[1:]:
        if game.has_attr('class') and game['class'][0] == 'thead':
            continue
        else:
            game = list(game)
            if game[-1].text in ('Inactive', 'Did Not Dress', 'Did Not Play'):
                print('Player did not play... Skipping...')
                continue
            else:
                print('Getting player game stats...')
                player_season_stats['player'].append(player_name)
                for stat in game:
                    if stat.get('data-stat') not in player_season_stats:
                        player_season_stats[stat.get('data-stat')] = []
                        player_season_stats[stat.get('data-stat')].append(stat.text)
                    else:
                        player_season_stats[stat.get('data-stat')].append(stat.text)

    return player_season_stats


def write_to_csv(player_season_stats):
    try:
        print('Writting to csv...')
        df = pd.DataFrame(player_season_stats)
        df.to_csv('../data/2020_2021_nba_season_player_stats.csv', mode='a', header=True)
    except Exception as e:
        print('Could not write to csv...')
        print(e)
    return


def main():
    basketball_team_urls = [
        'https://www.basketball-reference.com/teams/ATL/2021.html',
        'https://www.basketball-reference.com/teams/BOS/2021.html',
        'https://www.basketball-reference.com/teams/BRK/2021.html',
        'https://www.basketball-reference.com/teams/CHO/2021.html',
        'https://www.basketball-reference.com/teams/CHI/2021.html',
        'https://www.basketball-reference.com/teams/CLE/2021.html',
        'https://www.basketball-reference.com/teams/DAL/2021.html',
        'https://www.basketball-reference.com/teams/DEN/2021.html',
        'https://www.basketball-reference.com/teams/DET/2021.html',
        'https://www.basketball-reference.com/teams/GSW/2021.html',
        'https://www.basketball-reference.com/teams/HOU/2021.html',
        'https://www.basketball-reference.com/teams/IND/2021.html',
        'https://www.basketball-reference.com/teams/LAC/2021.html',
        'https://www.basketball-reference.com/teams/LAL/2021.html',
        'https://www.basketball-reference.com/teams/MEM/2021.html',
        'https://www.basketball-reference.com/teams/MIA/2021.html',
        'https://www.basketball-reference.com/teams/MIL/2021.html',
        'https://www.basketball-reference.com/teams/MIN/2021.html',
        'https://www.basketball-reference.com/teams/NOP/2021.html',
        'https://www.basketball-reference.com/teams/NYK/2021.html',
        'https://www.basketball-reference.com/teams/OKC/2021.html',
        'https://www.basketball-reference.com/teams/ORL/2021.html',
        'https://www.basketball-reference.com/teams/PHI/2021.html',
        'https://www.basketball-reference.com/teams/PHO/2021.html',
        'https://www.basketball-reference.com/teams/POR/2021.html',
        'https://www.basketball-reference.com/teams/SAC/2021.html',
        'https://www.basketball-reference.com/teams/SAS/2021.html',
        'https://www.basketball-reference.com/teams/TOR/2021.html',
        'https://www.basketball-reference.com/teams/UTA/2021.html',
        'https://www.basketball-reference.com/teams/WAS/2021.html'
    ]

    for team_url in basketball_team_urls:
        print(f'Getting data for team_url: {team_url}')
        players, player_urls = get_player_page_yuh(team_url)
        for idx, player in enumerate(players):
            print(f'Getting data on player: {player}; Player URL: {player_urls[idx]}')
            table_summary = get_player_regular_season_stats(player_urls[idx])
            if table_summary == '':
                continue
            else:
                player_season_stats = parse_player_data(table_summary, player)
                write_to_csv(player_season_stats)
                print('Successfully wrote to csv!')


if __name__=='__main__':
    main()