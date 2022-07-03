from calendar import week
import sched
from turtle import back, home
import numpy as np
import random

matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),
                (2,1),(2,3),(2,4),(2,5),(2,6),
                (3,1),(3,2),(3,4),(3,5),(3,6),
                (4,1),(4,2),(4,3),(4,5),(4,6),
                (5,1),(5,2),(5,3),(5,4),(5,6),
                (6,1),(6,2),(6,3),(6,4),(6,5)]

#matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),
#                (2,1),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),
#                (3,1),(3,2),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),
#                (4,1),(4,2),(4,3),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),
#                (5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(5,10),
#                (6,1),(6,2),(6,3),(6,4),(6,5),(6,7),(6,8),(6,9),(6,10),
#                (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,8),(7,9),(7,10),
#                (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,9),(8,10),
#                (9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,10),
#                (10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9)]

matrix_cost = np.array([[0,745,665,929,605,521],
                        [745,0,80,337,1090,315],
                        [665,80,0,380,1020,257],
                        [929,337,380,0,1380,408],
                        [605,1090,1020,1380,0,1010], 
                        [521,315,257,408,1010,0]])
'''matrix_cost = np.array([[0,745,665,929,605,521,370,587,467,670],
[745,0,80,337,1090,315,567,712,871,741],
[665,80,0,380,1020,257,501,664,808,697],
[929,337,380,0,1380,408,622,646,878,732],
[605,1090,1020,1380,0,1010,957,1190,1060,1270],
[521,315,257,408,1010,0,253,410,557,451],
[370,567,501,622,957,253,0,250,311,325],
[587,712,664,646,1190,410,250,0,260,86],
[467,871,808,878,1060,557,311,260,0,328],
[670,741,697,732,1270,451,325,86,328,0]])'''
number_of_teams = 6
number_of_weeks = int(((2*number_of_teams) - 2)/2)
array_cost = np.zeros(number_of_teams)
backup = []
random.shuffle(matches_list)

def heuristic_solution(all_matches_list: list, number_of_weeks: int, number_of_teams: int):
    schedule = np.zeros([number_of_weeks, number_of_teams])
    for week_index in range(len(schedule[0])-1):
        for team_index in range(len(schedule[1])):
            match_index = 0
            while schedule[week_index][team_index] == 0:
                if match_index >= len(all_matches_list):
                    match1 = (np.argwhere(schedule[week_index]==0)[0][0]+1,np.argwhere(schedule[week_index]==0)[1][0]+1)
                    match2 = (np.argwhere(schedule[week_index]==0)[1][0]+1,np.argwhere(schedule[week_index]==0)[0][0]+1)
                    #print(match1)
                    #print(match2)
                    #print(backup)
                    #print(schedule)
                    #print(week_index, team_index)
                    if match1 in backup:
                        team_away = match1[1]
                        team_home = match1[0]
                        #print(f'match01:{match1}\n{schedule}')
                        schedule[week_index][team_index] = team_away
                        schedule[week_index][team_away-1] = -team_home
                        #print(f'match01:{match1}\n{schedule}')
                    elif match2 in backup:
                        team_away = match2[0]
                        team_home = match2[1]
                        #print(f'match01:{match1}\n{schedule}')
                        schedule[week_index][team_index] = -team_away
                        schedule[week_index][team_away-1] = team_home
                        #print(f'match02:{match2}\n{schedule}')
                    #print(all_matches_list)
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

def calculate_sequence_matches_penalty(heuristic_schedule: np.array):
    for team in range(heuristic_schedule.shape[0]):
        dist = 0
        origin_loc = 'home'
        origin_loc_index = team
        for d1 in range(heuristic_schedule.shape[1]):
            if heuristic_schedule[team][d1]>0:
                next_loc = 'home'
                if origin_loc != next_loc:
                    dist += matrix_cost[origin_loc_index][team]
                    origin_loc_index = team
                    origin_loc = next_loc
            elif heuristic_schedule[team][d1] < 0:
                next_loc = 'away'
                if (origin_loc != next_loc) or (origin_loc == next_loc == 'away'):
                    dist += matrix_cost[origin_loc_index][int(abs(heuristic_schedule[team][d1]))-1]
                    origin_loc_index = int(abs(heuristic_schedule[team][d1]))-1
                    origin_loc = next_loc
        array_cost[team] = dist

    home_away_table = heuristic_schedule.copy()

    for i in range(home_away_table.shape[0]):
        for j in range(home_away_table.shape[1]):
            home_away_table[i][j]/=int(abs(home_away_table[i][j]))

    rep_home = 0
    for team_index in range(home_away_table.shape[0]):
        my_list = home_away_table[team_index].tolist()
        rep_home += len([[-1,-1,-1] for index in range(len(my_list)) if my_list[index : index + len([-1,-1,-1])] == [-1,-1,-1]])
        rep_home += len([[1,1,1] for index in range(len(my_list)) if my_list[index : index + len([1,1,1])] == [1,1,1]])
    return rep_home

heuristic_schedule = heuristic_solution(all_matches_list = matches_list,number_of_teams=number_of_teams, number_of_weeks=number_of_weeks)
print(f'Solution Example:\n{heuristic_schedule}')
seq_penalty = calculate_sequence_matches_penalty(heuristic_schedule=heuristic_schedule)

def evaluation_function(cost_array: list, seq_penalty: int):
    fs = sum(cost_array) + 1000*seq_penalty
    return fs

fs = evaluation_function(cost_array=array_cost,seq_penalty=seq_penalty)

print(seq_penalty)
print(array_cost)
print(fs)
np.savetxt(f'./solutions/heuristic_schedule_{number_of_teams}_{int(sum(array_cost))}.csv', heuristic_schedule, delimiter=",")