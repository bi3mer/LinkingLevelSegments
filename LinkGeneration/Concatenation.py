def build_link(start, end, config):
    return [] if config.get_percent_playable(start + end) == 1.0 else None