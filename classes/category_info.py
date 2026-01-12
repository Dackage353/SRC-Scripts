from common import fetch_handler, file_helper, reference, src_helper, tool


class CategoryInfo:
    def __init__(self, data):
        self.id                  = data.get('id')
        self.is_miscellaneous    = data.get('miscellaneous')
        self.name                = data.get('name')
        self.rules               = data.get('rules')
        self.type                = data.get('type')
        self.weblink             = data.get('weblink')

        player_count_info = data.get('players', {})
        self.player_count_type     = player_count_info.get('type')
        self.player_count_value    = player_count_info.get('value')

        links = data.get('links', [])
        links_by_relation = {link.get('rel'): link.get('uri') for link in links}
        self.game_api_link           = links_by_relation.get('game')
        self.leaderboard_api_link    = links_by_relation.get('leaderboard')
        self.records_api_link        = links_by_relation.get('records')
        self.runs_api_link           = links_by_relation.get('runs')
        self.self_api_link           = links_by_relation.get('self')
        self.variables_api_link      = links_by_relation.get('variables')

        self.game_id = self.game_api_link.rsplit('/', 1)[-1] if self.game_api_link else None
        
    @property
    def game_name(self):
        return reference.game_names[self.game_id]

    @property
    def game_and_category_name(self):
        return f'{reference.game_names[self.game_id]} - {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'
    