from collections import deque

def build_link(start, end, config, max_fitness_calculations=1_000):
    assert config.level_is_valid(start)
    assert config.level_is_valid(end)
    
    if config.level_is_valid(start + end) and config.get_percent_playable(start + end) == 1.0:
        return []

    output = config.unigram_keys
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