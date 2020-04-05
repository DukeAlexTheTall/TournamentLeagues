import pandas as pd
from glob import glob

def menu_1st_level():
    print ("""...MENU...
           (1) Choose a tournament:
           
           avaible tournaments: %s\n""" % (tournament_names))
    
    input_tournament = input("Your input (file_name.csv) --> ")
    if input_tournament in tournament_names:
        menu_2nd_level(input_tournament)
    else:
        print ("ERROR! You typed wrong name.")
        menu_1st_level()

def menu_2nd_level(tournament):
    print ("""...MENU...
              (1) Show all matches of a team;
              (2) Show matches played on a given date;
              (3) Show the ranking table;
              (4) <-- go back""")
    usr_input = int(input("Choose otption number --> "))

    df = pd.read_csv(tournament, usecols=['Date', 'Home', 'Away', 'HG', 'AG', 'Res'])

    if usr_input == 1:
        input_team = input("Type the team name --> ")
        if input_team in (list(df.Home.values) or list(df.Away.values)):
            show_matches(input_team, df)
        else:
            print ("ERROR! This team name doesn't exist.")
            menu_2nd_level(tournament)
    
    elif usr_input == 2:
        input_date = input("Type the date (format: dd/mm/yyyy) --> ")
        if input_date in list(df.Date.values):
            matches_on_date(input_date, df)
        else:
            print ("ERROR! This date is incorrect.")
            menu_2nd_level(tournament)
    
    elif usr_input == 3:
        tournament_league = pd.DataFrame(columns=['Team', 'Games', 'Wins', 'Draws', 'Losses', 'GD', 'Pts'])
        for team in set(df.Home.values):
            current_team = df[df['Home']==team]
            current_team_away = df[df['Away']==team]
            current_team['Pts'] = current_team['Res'].apply(pointer_home)
            current_team_away['Pts'] = current_team_away['Res'].apply(pointer_away)
            team_info = league_data(team, current_team, current_team_away)
            tournament_league = pd.concat([tournament_league, team_info])
        tournament_rank = ranking_by_GD(tournament_league)
        print (tournament_rank)
   
    elif usr_input == 4:
        menu_1st_level()

def show_matches(team, df_input):
    th = df_input[df_input['Home']==team]
    ta = df_input[df_input['Away']==team]
    result = pd.concat([th, ta])
    print (result)
    input("Type ANY key to display menu!")
    menu_2nd_level(df_input)

def matches_on_date(date, df_input):
    match = df_input[df_input['Date']==date]
    print(match)
    input("Type ANY key to display menu!")
    menu_2nd_level(df_input)

def pointer_home(res):
    if res=='A':
        res = 0
    elif res=='H':
        res = 3
    elif res=='D':
        res = 1
    return res

def pointer_away(res):
    if res=='A':
        res = 3
    elif res=='H':
        res = 0
    elif res=='D':
        res = 1
    return res

def league_data(team_name, team_home, team_away):
    games = team_home.Home.count() + team_away.Away.count()
    wins_home, wins_away = team_home[team_home['Res'] == 'H'], team_away[team_away['Res'] == 'A']
    wins = wins_home.Res.count() + wins_away.Res.count()
    draws_home, draws_away = team_home[team_home["Res"] == 'D'], team_away[team_away["Res"] == 'D']
    draws = draws_home.Res.count() + draws_away.Res.count()
    losses_home, losses_away = team_home[team_home['Res'] == 'A'], team_away[team_away['Res'] == 'H']
    losses = losses_home.Res.count() + losses_away.Res.count()
    gd = wins - losses
    pts = team_home.Pts.sum() + team_away.Pts.sum()
    tmp_df = pd.DataFrame({"Team":[team_name], "Games":[games], "Wins":[wins], "Draws":[draws], "Losses":[losses], "GD":[gd], "Pts":[pts]})
    return (tmp_df)

def ranking_by_GD(data):
    data = data.sort_values(['Pts', 'GD'], ascending=(False, False))
    data = data.reset_index(drop=True)
    data.index += 1
    data.index.name = 'Rank'
    duplicate = data[data.duplicate(['GD', 'Pts'])]
    return data

tournament_names = glob('*.csv')
menu_1st_level()

