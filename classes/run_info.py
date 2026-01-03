from common import tool


class RunInfo:
    def __init__(self, data):
        #ids
        self.run_id = data.get('id')
        self.game_id = data.get('game')
        self.category_id = data.get('category')

        #time
        self.run_time = data.get('times', {}).get('primary_t')
        self.run_time_formatted = tool.get_formatted_time(self.run_time) if self.run_time else None
        self.run_date = tool.parse_date(data.get('date'))
        self.time_submitted = tool.parse_date_and_seconds(data.get('submitted'))

        #status
        status = data.get('status', {})
        self.verify_status = status.get('status')
        self.time_verified = status.get('verify-date')
        self.verifier_id = status.get('examiner')

        #players
        players = data.get('players', [])
        player_ids = [player.get('id') for player in players if player.get('rel') == 'user']
        self.single_player_id = None
        self.multiple_player_ids = None

        if len(player_ids) == 1:
            self.single_player_id = player_ids[0]
        elif len(player_ids) > 1:
            self.multiple_player_ids = player_ids

    def get_player_ids(self):
        player_ids = []

        if self.single_player_id:
            player_ids.append(self.single_player_id)

        if self.multiple_player_ids:
            player_ids.extend(self.multiple_player_ids)

        return player_ids

    def __repr__(self):
        fields = "\n  ".join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{self.__class__.__name__}(\n  {fields}\n)"
