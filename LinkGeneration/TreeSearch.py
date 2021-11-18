from collections import deque

def __generate(grammar, prior, is_valid, connection):
    output = []

    while grammar.has_next_step(prior):
        valid_found = False
        for token in grammar.get_unweighted_output_list(prior):
            new_output = output + [token]
            prior = tuple(prior[1:]) + (token,)
            if is_valid(connection(new_output)):
                if len(new_output) > 4:
                    from Config import DungeonGram
                    from sys import exit
                    print(DungeonGram.level(connection(new_output)))
                    exit()
                    
                output = new_output
                valid_found = True
                break
        
        if not valid_found: 
            break
    
    return output

def build_link(start, end, config):
    if config.level_is_valid(start + end) and config.get_percent_playable(start + end) == 1.0:
        return []

    START_LINK = __generate(config.FORWARD_STRUCTURE_GRAM, (start[-1],), config.level_is_valid, lambda link: start + link)
    END_LINK = __generate(config.BACKWARD_STRUCTURE_GRAM, (end[0],), config.level_is_valid, lambda link: link + end)
    END_LINK = list(reversed(END_LINK))

    assert start + START_LINK + END_LINK + end

    if config.get_percent_playable(start + START_LINK + END_LINK + end) == 1.0:
        return START_LINK + END_LINK

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

        if len(current_path) < config.MAX_LINK_LENGTH:
            for o in output:
                queue.append(current_path + o)

    return None