from collections import deque

def build_link(start, end, config):
    if config.ALLOW_EMPTY_LINK and \
       config.level_is_valid(start + end) and \
       config.get_percent_playable(start + end) == 1.0:
        return []

    for START_LINK in config.FORWARD_STRUCTURE_GRAM.get_output(start):
        for END_LINK in config.BACKWARD_STRUCTURE_GRAM.get_output(end):
            END_LINK = list(reversed(END_LINK))

            if config.ALLOW_EMPTY_LINK and \
                config.get_percent_playable(start + START_LINK + END_LINK + end) == 1.0:
                return START_LINK + END_LINK

            output = config.LINKERS
            queue = deque([o for o in output])

            fitness_calculations = 0
            while len(queue) > 0:
                current_path = queue.popleft()
                NEW_LEVEL = start + START_LINK + current_path + END_LINK + end

                if config.get_percent_playable(NEW_LEVEL) == 1.0:
                    assert config.level_is_valid(NEW_LEVEL)
                    return START_LINK + current_path + END_LINK
                else:
                    fitness_calculations += 1

                if len(current_path) < config.MAX_LINK_LENGTH:
                    for o in output:
                        queue.append(current_path + o)

    return None