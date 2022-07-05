import numpy as np

backup = []

matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),
                (2,1),(2,3),(2,4),(2,5),(2,6),
                (3,1),(3,2),(3,4),(3,5),(3,6),
                (4,1),(4,2),(4,3),(4,5),(4,6),
                (5,1),(5,2),(5,3),(5,4),(5,6),
                (6,1),(6,2),(6,3),(6,4),(6,5)]

matrix_cost = np.array([[0,745,665,929,605,521],
                        [745,0,80,337,1090,315],
                        [665,80,0,380,1020,257],
                        [929,337,380,0,1380,408],
                        [605,1090,1020,1380,0,1010], 
                        [521,315,257,408,1010,0]])

number_of_teams = matrix_cost.shape[1]
number_of_weeks = int(((2*number_of_teams) - 2)/2)

def heuristic_solution(all_matches_list: list, number_of_weeks: int, number_of_teams: int):
    schedule = np.zeros([number_of_weeks, number_of_teams])
    for week_index in range(len(schedule[0])-1):
        for team_index in range(len(schedule[1])):
            match_index = 0
            while schedule[week_index][team_index] == 0:
                if match_index >= len(all_matches_list):
                    match1 = (np.argwhere(schedule[week_index]==0)[0][0]+1,np.argwhere(schedule[week_index]==0)[1][0]+1)
                    match2 = (np.argwhere(schedule[week_index]==0)[1][0]+1,np.argwhere(schedule[week_index]==0)[0][0]+1)
                    if match1 in backup:
                        team_away = match1[1]
                        team_home = match1[0]
                        schedule[week_index][team_index] = team_away
                        schedule[week_index][team_away-1] = -team_home
                    elif match2 in backup:
                        team_away = match2[0]
                        team_home = match2[1]
                        schedule[week_index][team_index] = -team_away
                        schedule[week_index][team_away-1] = team_home
                elif all_matches_list[match_index][0]-1==team_index and schedule[week_index][all_matches_list[match_index][1] - 1]==0:
                    team_away = all_matches_list[match_index][1]
                    team_home = all_matches_list[match_index][0]
                    schedule[week_index][team_index] = team_away
                    schedule[week_index][team_away - 1] = -team_home
                    all_matches_list.remove(all_matches_list[match_index])
                    all_matches_list.remove((team_away,team_home))
                    backup.append((team_away,team_home))
                elif all_matches_list[match_index][1]-1==team_index and schedule[week_index][all_matches_list[match_index][0] - 1] ==0:
                    team_away = all_matches_list[match_index][1]
                    team_home = all_matches_list[match_index][0]
                    schedule[week_index][team_index] = -team_home
                    schedule[week_index][team_home - 1] = team_away
                    all_matches_list.remove(all_matches_list[match_index])
                    all_matches_list.remove((team_away,team_home))
                    backup.append((team_away,team_home))
                else:
                    match_index += 1
    schedule = schedule.T
    return(schedule)

schedule_ = heuristic_solution(all_matches_list=matches_list, number_of_teams=number_of_teams, number_of_weeks=number_of_weeks)
print(schedule_)