from calendar import week
import sched
from turtle import back, home
import numpy as np
import random
from datetime import datetime
import pandas as pd

df = pd.DataFrame(columns=["ExperimentID", "Method", "Solution", "CostFunctionValue","Duration"])

'''matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),
                (2,1),(2,3),(2,4),(2,5),(2,6),
                (3,1),(3,2),(3,4),(3,5),(3,6),
                (4,1),(4,2),(4,3),(4,5),(4,6),
                (5,1),(5,2),(5,3),(5,4),(5,6),
                (6,1),(6,2),(6,3),(6,4),(6,5)]'''

'''matrix_cost = np.array([[0,745,665,929,605,521],
                        [745,0,80,337,1090,315],
                        [665,80,0,380,1020,257],
                        [929,337,380,0,1380,408],
                        [605,1090,1020,1380,0,1010], 
                        [521,315,257,408,1010,0]])'''

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

def fix_repeated_matches(hs):
    for team in range(1,number_of_teams+1):
        week_repeated = []
        team_repeated = []
        team_option = []
        week_replacement_options = []
        for index in range(0,number_of_teams):
            hs_index = [abs(x) for x in hs[index]]
            if hs_index.count(team) > 1:
                hs_index = np.array(hs_index)
                team_problem = team
                week_repeated += list(np.where(hs_index == team)[0])
                team_repeated.append(index)
            elif (hs_index.count(team) == 0) and (team - index)!=1:
                week_replacement_options.append(list(np.array(hs_index)[week_repeated]))
                team_option.append(index)
        if team_repeated or team_option:
            for rep_team in team_repeated:
                break_out_flag = False
                for rep_week in week_repeated:
                    for rep_team_option in team_option:
                        hs_index_ = [abs(x) for x in hs[rep_team]]
                        if (abs(hs[rep_team_option][rep_week]) not in hs_index_) or (abs(hs[rep_team_option][rep_week])>team_problem):
                            break_out_flag = True
                            hs[rep_team][rep_week], hs[rep_team_option][rep_week] = hs[rep_team_option][rep_week], hs[rep_team][rep_week]
                            team_repeated.remove(rep_team)
                            week_repeated.remove(rep_week)
                            team_option.remove(rep_team_option)
                            break
                    if break_out_flag:
                        break
    return hs

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

    home_away_table = hs.copy()

    for i in range(home_away_table.shape[0]):
        for j in range(home_away_table.shape[1]):
            home_away_table[i][j]/=int(abs(home_away_table[i][j]))

    rep_home = 0
    for team_index in range(home_away_table.shape[0]):
        my_list = home_away_table[team_index].tolist()
        rep_home += len([[-1,-1,-1] for index in range(len(my_list)) if my_list[index : index + len([-1,-1,-1])] == [-1,-1,-1]])
        rep_home += len([[1,1,1] for index in range(len(my_list)) if my_list[index : index + len([1,1,1])] == [1,1,1]])
    return rep_home, array_cost, cost_matrix

def calculate_repeated_matches_penalty(hs: np.array):
    penalty = 0
    for team_schedule in range(hs.shape[0]):
        hs_ = list(hs[team_schedule])
        hs_ =  [abs(ele) for ele in hs_]
        my_dict = {i:hs_.count(i) for i in hs_}
        for value in my_dict.values():
            if value > 2:
                penalty+=value
    return penalty

def calculate_multiple_matches_week_penalty(hs: np.array):
    penalty = 0
    for week_schedule in range(hs.shape[1]):
        hs_ = list(hs[:,week_schedule])
        hs_ =  [abs(ele) for ele in hs_]
        my_dict = {i:hs_.count(i) for i in hs_}
        for value in my_dict.values():
            if value > 2:
                penalty += value
    return penalty

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

def evaluation_function(cost_array: list, seq_penalty: int, rep_penalty : int, mult_penalty: int):
    fs = sum(cost_array) + 1.5*sum(cost_array)*(seq_penalty) + 4*sum(cost_array)*(rep_penalty + mult_penalty)
    return fs

def vnd_swap_homes(hs_: np.array, home_index, away_index, w1):
    hs = hs_.copy()
    w2 = w1 + number_of_weeks
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
    init_fhs = fhs_
    init_seq_penalty, init_array_cost, init_cost_matrix = calculate_sequence_matches_penalty(hs=init_fhs)
    init_repeat_penalty = calculate_repeated_matches_penalty(hs=init_fhs)
    init_multiple_penalty = calculate_multiple_matches_week_penalty(hs=init_fhs)
    init_fs = evaluation_function(cost_array=init_array_cost, seq_penalty=init_seq_penalty, rep_penalty = init_repeat_penalty, mult_penalty = init_multiple_penalty)

    for i in range(100):
        matches_cost, team_home, team_home_index, team_away, team_away_index, week_r1, week_r2 = pick_home_away_teams(costs_= init_cost_matrix, hs=init_fhs)
        fhs_swaped_homes = vnd_swap_homes(hs_= init_fhs, home_index = team_home_index, away_index = team_away_index, w1 = week_r1)
        seq_penalty, array_cost, cost_matrix = calculate_sequence_matches_penalty(hs=fhs_swaped_homes)
        repeat_penalty = calculate_repeated_matches_penalty(hs=fhs_swaped_homes)
        multiple_penalty = calculate_multiple_matches_week_penalty(hs=fhs_swaped_homes)
        fs = evaluation_function(cost_array=array_cost, seq_penalty=seq_penalty, rep_penalty = repeat_penalty, mult_penalty = multiple_penalty)
        if fs<init_fs:
            #print(f'Found a better solution swapping homes: From {best_fs} to {fs}')
            init_fs = fs
            init_fhs = fhs_swaped_homes
            init_seq_penalty = seq_penalty
            init_array_cost = array_cost
            init_cost_matrix = cost_matrix
        else:
            week_r1 = random.randint(0,number_of_weeks-1)
            team_home_index = random.randint(0,number_of_teams-1)
            week_r2 = week_r1 + number_of_weeks
            team_away_index = int(abs(init_fhs[team_home_index, week_r1])) - 1
            fhs_swaped_homes = vnd_swap_homes(hs_= init_fhs, home_index = team_home_index, away_index = team_away_index, w1 = week_r1)
            seq_penalty, array_cost, cost_matrix = calculate_sequence_matches_penalty(hs=fhs_swaped_homes)
            repeat_penalty = calculate_repeated_matches_penalty(hs=fhs_swaped_homes)
            multiple_penalty = calculate_multiple_matches_week_penalty(hs=fhs_swaped_homes)
            fs = evaluation_function(cost_array=array_cost, seq_penalty=seq_penalty, rep_penalty = repeat_penalty, mult_penalty = multiple_penalty)
        i += 1
    for i in range(100):
        fhs_swaped_rounds = vnd_swap_rounds(hs_= best_fhs, cm_= cost_matrix, nw=number_of_weeks)
        seq_penalty, array_cost, cost_matrix = calculate_sequence_matches_penalty(hs=fhs_swaped_rounds)
        fs = evaluation_function(cost_array=array_cost, seq_penalty=seq_penalty)
        if fs<best_fs:
            print(f'Found a better solution swapping rounds: From {best_fs} to {fs}')
            init_fs = fs
            init_fhs = fhs_swaped_homes
            init_seq_penalty = seq_penalty
            init_array_cost = array_cost
            init_cost_matrix = cost_matrix
        i += 1
    return init_fs, init_fhs, init_seq_penalty, init_array_cost, init_cost_matrix

def iterated_local_search(fhs_: np.array, n_restarts: int):
    #s0 <- initial_solution
    initial_solution = fhs_ 
    initial_seq_penalty, initial_array_cost, initial_cost_matrix = calculate_sequence_matches_penalty(hs=initial_solution)
    repeat_penalty = calculate_repeated_matches_penalty(hs=full_heuristic_schedule)
    multiple_penalty = calculate_multiple_matches_week_penalty(hs=full_heuristic_schedule)
    initial_fs = evaluation_function(cost_array=initial_array_cost, seq_penalty=initial_seq_penalty, rep_penalty = repeat_penalty, mult_penalty = multiple_penalty)
    #s <- local_search(s0)
    best_fs, best_fhs, best_seq_penalty, best_array_cost, best_cost_matrix = vnd_explorer(fhs_ = initial_solution)
    #iter <- 0
    i = 0
    for i in range(n_restarts):
        i += 1 #i <- i + 1
        pert_fhs = vnd_swap_homes(hs_= best_fhs, home_index= random.randint(0,number_of_teams-1), away_index= random.randint(0,number_of_teams-1), 
                                    w1 = random.randint(0,number_of_weeks-1)) #s’ <- perturbation(s, historics)
        next_fs, next_fhs, next_seq_penalty, next_array_cost, next_cost_matrix = vnd_explorer(fhs_ = pert_fhs) #s’’ <- local_search(s’)
        if next_fs < best_fs: #s <- acceptance_criteria(s, s’’)
            print(f'Found a better solution on iteration {i}! found_fs:{next_fs}, previous_fs:{best_fs}')
            best_fs = next_fs
            best_fhs = next_fhs
            best_seq_penalty = next_seq_penalty
            best_array_cost = next_array_cost
            best_cost_matrix = next_cost_matrix
    return best_fs, best_fhs, best_seq_penalty, best_array_cost, best_cost_matrix

for experiment_id in range(0, 10):
    
    matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),
                (2,1),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),
                (3,1),(3,2),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),
                (4,1),(4,2),(4,3),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),
                (5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(5,10),
                (6,1),(6,2),(6,3),(6,4),(6,5),(6,7),(6,8),(6,9),(6,10),
                (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,8),(7,9),(7,10),
                (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,9),(8,10),
                (9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,10),
                (10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9)]

    matrix_cost = np.array([[0,745,665,929,605,521,370,587,467,670],
    [745,0,80,337,1090,315,567,712,871,741],
    [665,80,0,380,1020,257,501,664,808,697],
    [929,337,380,0,1380,408,622,646,878,732],
    [605,1090,1020,1380,0,1010,957,1190,1060,1270],
    [521,315,257,408,1010,0,253,410,557,451],
    [370,567,501,622,957,253,0,250,311,325],
    [587,712,664,646,1190,410,250,0,260,86],
    [467,871,808,878,1060,557,311,260,0,328],
    [670,741,697,732,1270,451,325,86,328,0]])

    number_of_teams = matrix_cost.shape[1]
    number_of_weeks = int(((2*number_of_teams) - 2)/2)
    array_cost = np.zeros(number_of_teams)
    backup = []
    cost_matrix = np.zeros((number_of_teams,2*number_of_weeks))
    random.shuffle(matches_list)

    #### Heuristic
    start_heu = datetime.now()
    hs = heuristic_solution(all_matches_list = matches_list,number_of_teams=number_of_teams, number_of_weeks=number_of_weeks)
    heuristic_schedule = fix_repeated_matches(hs)
    full_heuristic_schedule = add_second_tournament_round(heuristic_schedule=heuristic_schedule)
    init_seq_penalty, init_array_cost, init_cost_matrix = calculate_sequence_matches_penalty(hs=full_heuristic_schedule)
    repeat_penalty = calculate_repeated_matches_penalty(hs=full_heuristic_schedule)
    multiple_penalty = calculate_multiple_matches_week_penalty(hs=full_heuristic_schedule)
    init_fs = evaluation_function(cost_array=init_array_cost, seq_penalty=init_seq_penalty, rep_penalty = repeat_penalty, mult_penalty = multiple_penalty)

    best_fs, best_fhs, best_seq_penalty, best_array_cost, best_cost_matrix = vnd_explorer(fhs_ = full_heuristic_schedule)

    end_heu = datetime.now()
    duration_heu = end_heu - start_heu
    duration_heu_sec = duration_heu.total_seconds()

    print(f'Initial Solution:\n{full_heuristic_schedule}')
    print(init_seq_penalty)
    print(init_array_cost)
    print(init_fs)

    print(f'Final Solution (Heuristic):\n{best_fhs}')
    print(best_seq_penalty)
    print(best_array_cost)
    print(best_fs)
    heu_ = [experiment_id, 'Heuristic', best_fs, sum(best_array_cost), duration_heu_sec]
    heu_series = pd.Series(heu_, index = df.columns)
    np.savetxt(f'./solutions/Heuristic_{experiment_id}_{number_of_teams}.csv', best_fhs, delimiter=",")
    
    #### Meta-Heuristic
    
    start_ils = datetime.now()
    ils_fs, ils_fhs, ils_seq_penalty, ils_array_cost, ils_cost_matrix = iterated_local_search(fhs_ = full_heuristic_schedule, n_restarts = number_of_teams*number_of_weeks*5)
    end_ils = datetime.now()
    duration_ils = end_ils - start_ils
    duration_ils_sec = duration_ils.total_seconds()

    print(f'Final Solution (ILS):\n{ils_fhs}')
    print(ils_seq_penalty)
    print(ils_array_cost)
    print(ils_fs)

    ils_ = [experiment_id, 'ILS', ils_fs, sum(ils_array_cost), duration_ils_sec]
    ils_series = pd.Series(ils_, index = df.columns)


    df = df.append(ils_series, ignore_index=True)
    df = df.append(heu_series, ignore_index=True)

    np.savetxt(f'./solutions/ILS_{experiment_id}_{number_of_teams}.csv', ils_fhs, delimiter=",")

    experiment_id += 1

df.to_csv(f'./solutions/experiment_results_{number_of_teams}.csv')