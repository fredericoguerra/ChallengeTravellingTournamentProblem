import numpy as np

def add_second_tournament_round(heuristic_schedule: np.array):
    second_round = -1*heuristic_schedule
    full_heuristic_schedule = np.concatenate((heuristic_schedule, second_round), axis=1)
    return full_heuristic_schedule

heuristic_schedule = np.array(
    [[ 2.,  3.,  4.,  5.,  6.],
    [-1.,  4.,  3.,  6.,  5.],
    [-5., -1., -2., -4., -4.],
    [ 6., -2., -1.,  3.,  3.],
    [ 4., -6., -6., -1., -2.],
    [-3.,  5.,  5., -2., -1.]]
    )

full_heuristic_schedule = add_second_tournament_round(heuristic_schedule=heuristic_schedule)
print(full_heuristic_schedule)
