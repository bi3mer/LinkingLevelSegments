from collections import deque

def build_link(start, end, config, max_fitness_calculations=1_000):
    start_and_end_viable = config.level_is_valid(start + end)
    start_and_end_playable = config.get_percent_playable(start + end) == 1.0
    if start_and_end_viable and start_and_end_playable:
        return []

    if config.link_distance_dependent and \
       not start_and_end_viable and \
       not start_and_end_playable:
        return []

    output = config.link_keys
    queue = deque([[o] for o in output])

    fitness_calculations = 0
    while fitness_calculations < max_fitness_calculations:
        current_path = queue.popleft()
        NEW_LEVEL = start + current_path + end
        if config.level_is_valid(NEW_LEVEL):
            if config.get_percent_playable(NEW_LEVEL) == 1.0:
                return current_path
            else:
                fitness_calculations += 1

        for new_column in output:
            queue.append(current_path + [new_column])

    return None