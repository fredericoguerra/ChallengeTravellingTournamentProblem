from heuristic_solution_demo import heuristic_solution
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

schedule_ = np.array([
 [ 2.,  3.,  4.,  5.,  6.],
 [-1.,  4.,  3.,  6.,  5.],
 [ 4., -1., -2., -4., -4.],
 [-3., -2., -1.,  3.,  3.],
 [ 6., -6., -6., -1., -2.],
 [-5.,  5.,  5., -2., -1.]])
 
schedule_fixed = fix_repeated_matches(hs=schedule_)