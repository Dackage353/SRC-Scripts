from .single_star import SingleStar

class Level:
    def __init__(self, level_data, game_id, level_variables):
        self.data = level_data
        self.game_id = game_id

        self.id = self.data.get('id')
        self.name = self.data.get('name')
        
        self.init_single_stars(level_variables)

    def init_single_stars(self, level_variables):
        self.single_stars = []

        if self.id in level_variables:
            variable_values = level_variables[self.id].get('values').get('values')
            for key, values in variable_values.items():
                self.single_stars.append(SingleStar(
                    id          = key,
                    level_id    = self.id,
                    game_id     = self.game_id,
                    name        = values.get('label')
                ))
