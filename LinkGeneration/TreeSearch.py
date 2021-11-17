from collections import deque

from Config.Icarus import FORWARD_STRUCTURE_GRAM

def build_link(start, end, config):
    if config.level_is_valid(start + end) and config.get_percent_playable(start + end) == 1.0:
        return []

    START_LINK = config.FORWARD_STRUCTURE_GRAM.generate((start[-1],), 100) # FORWARD_STRUCTURE_GRAM
    END_LINK = config.BACKWARD_STRUCTURE_GRAM.generate((end[0],), 100)     # BACKWARD_STRUCTURE_GRAM
    END_LINK = list(reversed(END_LINK))

    assert start + START_LINK + END_LINK + end

    if config.get_percent_playable(start + START_LINK + END_LINK + end) == 1.0:
        return []

    output = config.LINKERS
    queue = deque([o for o in output])

    fitness_calculations = 0
    while len(queue) > 0:
        current_path = queue.popleft()
        NEW_LEVEL = start + START_LINK + current_path + END_LINK + end

        if config.get_percent_playable(NEW_LEVEL) == 1.0:
            return START_LINK + current_path + END_LINK
        else:
            fitness_calculations += 1

        if len(current_path) < config.max_link_length:
            for o in output:
                queue.append(current_path + o)

    return None