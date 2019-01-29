'''
DEFINITIONS:
song: [bpm, key, mood, energy, ... , property]
mix: abs(song_a - song_b) = [bpm_diff, key_diff, mood_diff, energy_diff, ... , prop_diff]
dj_style: [bpm_diff, key_diff, mood_diff, energy_diff, ... , prop_diff]
transition(section_a, section_b, length): 
[bpm_trans_expr, key_trans_expr, mood_trans_expr, energy_trans_expr, ... , prop_trans_expr]
goal: ([ideal_bpm, ideal_key, ideal_mood, ideal_energy, ... , ideal_prop], time)
goals: [goal_0, goal_1, goal_2, ... , goal_N]

things to account for:
    1. ensuring progress is made to the goal with every song (not too little or too much
    based on the time)
        a. set min/mix progress heuristics

DANGER ZONE (it's messy):

generate_mix(song_list, transitions, dj_style, goals):
    set_list = list(len(song_list))
    trans_list = list(len(song_list) - 1) 
    curr = find song in song_list s.t. min(abs(goal - song))
    set_list.add(first)
    // find the best mix and transition from curr to next given goal
    for goal in goals:
        ideal = goal[0]
        time_to_goal = goal[1]
        // find all reasonable mixes within dj_style:
        // compute mixes = X_1 ... X_N from all abs(curr - song_b)
        // collect CROSS_PRODUCT(transitions, mixes)
            for each length s.t. length < time_to_goal
                for each section_a in song_a and section_b in song_b:
                    if len(section_a) == len(section_b) == length
                    // collect R_1 ... R_N results = (mix, t(section_a, section_b, length))
        // select results within a threshold (how will it be measure, sum(props) or prop-by-prop basis?)
            threshold(acceptable difference, abs(R - dj_style)) 
        // examine the end song for each result
        // compare the end song to the ideal song
            ideal - song_b 
        // look at current song
            ideal - curr
        // ensure that the song_b approaches from the right direction... (check earlier?)
        // ensure that song_b satisfies "min/max progress" to the goal (check earlier?)
        // choose the ideal pairing of curr, t(section_a, section_b, length), song_b

'''