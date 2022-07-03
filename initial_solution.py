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
cost_matrix = np.zeros((number_of_teams,2*number_of_weeks))
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

def add_second_tournament_round(heuristic_schedule: np.array):
    second_round = -1*heuristic_schedule
    full_heuristic_schedule = np.concatenate((heuristic_schedule, second_round), axis=1)
    return full_heuristic_schedule

def calculate_sequence_matches_penalty(hs: np.array):
    for team in range(hs.shape[0]):
        dist = 0
        origin_loc = 'home'
        origin_loc_index = team
        for d1 in range(hs.shape[1]):
            if hs[team][d1]>0:
                next_loc = 'home'
                if origin_loc != next_loc:
                    dist += matrix_cost[origin_loc_index][team]
                    cost_matrix[team][d1] = matrix_cost[origin_loc_index][team]
                    origin_loc_index = team
                    origin_loc = next_loc
            elif hs[team][d1] < 0:
                next_loc = 'away'
                if (origin_loc != next_loc) or (origin_loc == next_loc == 'away'):
                    dist += matrix_cost[origin_loc_index][int(abs(hs[team][d1]))-1]
                    cost_matrix[team][d1] = matrix_cost[origin_loc_index][int(abs(hs[team][d1]))-1]
                    origin_loc_index = int(abs(hs[team][d1]))-1
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
    return rep_home, array_cost

def pick_home_away_teams(costs_: np.array, hs : np.array):
    round1 = costs_[:,:number_of_weeks]
    round2 = costs_[:,number_of_weeks:]
    matches_costs = round1 + round2

    max_cost = np.unravel_index(np.argmax(matches_costs, axis=None), matches_costs.shape)
    team_home_index = max_cost[0]
    week_round1 = max_cost[1]
    week_round2 = week_round1 + number_of_weeks
    
    team_away_index = int(abs(hs[team_home_index][week_round1]) - 1)
    team_home = team_home_index + 1
    team_away = team_away_index + 1

    return matches_costs, team_home, team_home_index, team_away, team_away_index, week_round1, week_round2

def evaluation_function(cost_array: list, seq_penalty: int):
    fs = sum(cost_array)# + 1000*seq_penalty
    return fs

def vnd_swap_homes(hs_: np.array, home_index, away_index, w1, w2):
    '''precisa de uma função anterior para decidir o team_home e away para trocar, encontrar rodada que se encontram no primeiro e segundo turno, fazer a troca'''
    #print(f'home_index: {home_index}\naway_index: {away_index}\nweek of round 1: {w1}\nweek of round 2: {w2}\n')
    hs = hs_.copy()
    hs[home_index][w1], hs[home_index][w2] = hs[home_index][w2], hs[home_index][w1]
    hs[away_index][w1], hs[away_index][w2] = hs[away_index][w2], hs[away_index][w1]
    return hs

def vnd_swap_rounds(hs_ : np.array, cm_: np.array, nw):
    hs = hs_.copy()
    w1 = cm_[:,:nw].sum(axis=0).argmax()
    w2 = cm_[:,:nw].sum(axis=0).argsort()[-2]
    hs[:,w1], hs[:,w2] = hs[:,w2], hs[:,w1]
    return hs

def vnd_explorer(fhs_: np.array):
    best_fhs = fhs_
    best_seq_penalty, best_array_cost = calculate_sequence_matches_penalty(hs=best_fhs)
    best_fs = evaluation_function(cost_array=best_array_cost, seq_penalty=best_seq_penalty)
    print(f'Solution 01:\n{best_fhs}')
    print(best_seq_penalty)
    print(best_array_cost)
    print(best_fs)

    for i in range(1000):
        matches_cost, team_home, team_home_index, team_away, team_away_index, week_r1, week_r2 = pick_home_away_teams(cost_matrix, hs=best_fhs)
        fhs_swaped_homes = vnd_swap_homes(hs_= best_fhs, home_index = team_home_index, away_index = team_away_index, w1 = week_r1, w2=week_r2)
        seq_penalty, array_cost = calculate_sequence_matches_penalty(hs=fhs_swaped_homes)
        fs = evaluation_function(cost_array=array_cost, seq_penalty=seq_penalty)
        if fs<best_fs:
            print(f'Found a better solution swapping homes: From {best_fs} to {fs}')
            best_fs = fs
            best_fhs = fhs_swaped_homes
            best_seq_penalty = seq_penalty
            best_array_cost = array_cost
        i += 1
    
    for i in range(1000):
        fhs_swaped_rounds = vnd_swap_rounds(hs_ = best_fhs, cm_ = cost_matrix, nw=number_of_weeks)
        seq_penalty = calculate_sequence_matches_penalty(hs=fhs_swaped_rounds)
        fs = evaluation_function(cost_array=array_cost, seq_penalty=seq_penalty)
        if fs<best_fs:
            print(f'Found a better solution swapping rounds: From {best_fs} to {fs}')
            best_fs = fs
            best_fhs = fhs_swaped_homes
            best_seq_penalty = seq_penalty
            best_array_cost = array_cost
        i += 1
    return best_fs, best_fhs, best_seq_penalty, best_array_cost

#### First solution
heuristic_schedule = heuristic_solution(all_matches_list = matches_list,number_of_teams=number_of_teams, number_of_weeks=number_of_weeks)
full_heuristic_schedule = add_second_tournament_round(heuristic_schedule=heuristic_schedule)

best_fs, best_fhs, best_seq_penalty, best_array_cost = vnd_explorer(fhs_ = full_heuristic_schedule)

print(f'Final Solution:\n{best_fhs}')
print(best_seq_penalty)
print(best_array_cost)
print(best_fs)

#np.savetxt(f'./solutions/heuristic_schedule_teams-{number_of_teams}_seqpenalty-{seq_penalty}_cost-{int(fs)}.csv', heuristic_schedule, delimiter=",")