from common import reference
from dataclasses import dataclass, field
from datetime import datetime, timezone
from datetime import timedelta
import pandas as pd

def create_game_info_from_data(data):
    return [GameInfo(d) for d in data]


def create_category_info_from_data(data):
    return [CategoryInfo(d) for d in data]


def create_run_info_from_data(data):
    return [RunInfo(d) for d in data]


def parse_date_and_seconds(date_and_seconds):
    if date_and_seconds is None:
        return None

    try:
        return datetime.strptime(date_and_seconds, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    

def parse_date(date):
    if date is None:
        return None

    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return None


def get_data_frame_for_run_list(runs):
    reference.check_for_missing_info_from_runs(runs)
    df = pd.DataFrame([r.__dict__ for r in runs])
    
    df['game_name'] = df['game_id'].map(reference.game_names)
    df['category_name'] = df['category_id'].map(reference.category_names)
    df['single_player_name'] = df['single_player_id'].map(reference.user_names)
    df['verifier_name'] = df['verifier_id'].map(reference.user_names)
    
    df = df.sort_values(['game_name', 'category_name', 'single_player_name'], ascending=[True, True, True])
    
    return df
        
        
class RunInfo:
    def __init__(self, data):
        global parse_date, parse_date_and_seconds

        #ids
        self.run_id = data.get('id')
        self.game_id = data.get('game')
        self.category_id = data.get('category')

        #time
        self.run_time = data.get('times', {}).get('primary_t')
        self.run_time_formatted = timedelta(seconds=self.run_time) if self.run_time else None
        self.run_date = parse_date(data.get('date'))
        self.time_submitted = parse_date_and_seconds(data.get('submitted'))

        #status
        status = data.get('status', {})
        self.verify_status = status.get('status')
        self.time_verified = status.get('verify-date')
        self.verifier_id = status.get('examiner')

        #players
        players = data.get('players', [])
        player_ids = [player.get('id') for player in players if player.get('rel') == 'user']
        self.single_player_id = None
        self.multiple_player_ids = []

        if len(player_ids) == 1:
            self.single_player_id = player_ids[0]
        elif len(player_ids) > 1:
            self.multiple_player_ids = player_ids

    def get_player_ids(self):
        player_ids = []

        if self.single_player_id:
            player_ids.append(self.single_player_id)

        player_ids.extend(self.multiple_player_ids)

        return player_ids

    def __repr__(self):
        fields = "\n  ".join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{self.__class__.__name__}(\n  {fields}\n)"


class GameInfo:
    def __init__(self, data):
        
        names = data.get('names', {})
        self.name_international    = names.get('international')
        self.name_japanese         = names.get('japanese')
        self.name_twitch           = names.get('twitch')

        self.abbreviation         = data.get('abbreviation')
        self.discord_link         = data.get('discord')
        self.id                   = data.get('id')
        self.is_romhack           = data.get('romhack')
        self.release_year         = data.get('released')
        self.weblink              = data.get('weblink')

        self.boost_donors         = data.get('boostDistinctDonors')
        self.boosts               = data.get('boostReceived')

        try:
            self.creation_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) if (created := data.get('created')) else None
        except ValueError:
            self.creation_date = None

        #ruleset
        ruleset = data.get('ruleset', {})
        self.default_time              = ruleset.get('default-time')
        self.emulators_allowed         = ruleset.get('emulators-allowed')
        self.require_verification      = ruleset.get('require-verification')
        self.require_video             = ruleset.get('require-video')
        self.run_times                 = ruleset.get('run-times')
        self.show_milliseconds         = ruleset.get('show-milliseconds')

        #ids
        self.developer_ids       = data.get('developers')
        self.engine_ids          = data.get('engines')
        self.game_type_ids       = data.get('gametypes')
        self.genre_ids           = data.get('genres')
        self.platform_ids        = data.get('platforms')
        self.publisher_ids       = data.get('publishers')
        self.region_ids          = data.get('regions')

        mods = data.get('moderators', {})
        self.super_moderators_ids = [key for key, value in mods.items() if value == "super-moderator"]
        self.moderators_ids = [key for key, value in mods.items() if value == "moderator"]

        #api links
        links = data.get('links', [])
        links_by_relation = {link.get('rel'): link.get('uri') for link in links}
        self.api_base_game_link        = links_by_relation.get('base-game')
        self.api_categories_link       = links_by_relation.get('categories')
        self.api_derived_games_link    = links_by_relation.get('derived-games')
        self.api_game_link             = links_by_relation.get('game')
        self.api_leaderboard_link      = links_by_relation.get('leaderboard')
        self.api_levels_link           = links_by_relation.get('levels')
        self.api_records_link          = links_by_relation.get('records')
        self.api_romhacks_link         = links_by_relation.get('romhacks')
        self.api_runs_link             = links_by_relation.get('runs')
        self.api_self_link             = links_by_relation.get('self')
        self.api_series_link           = links_by_relation.get('series')
        self.api_variables_link        = links_by_relation.get('variables')

        #asset links
        assets = data.get('assets', {})
        self.assets_background_link      = assets.get('background', {}).get('uri')
        self.assets_cover_large_link     = assets.get('cover-large', {}).get('uri')
        self.assets_cover_medium_link    = assets.get('cover-medium', {}).get('uri')
        self.assets_cover_small_link     = assets.get('cover-small', {}).get('uri')
        self.assets_cover_tiny_link      = assets.get('cover-tiny', {}).get('uri')
        self.assets_foreground_link      = assets.get('foreground', {}).get('uri')
        self.assets_icon_link            = assets.get('icon', {}).get('uri')
        self.assets_logo_link            = assets.get('logo', {}).get('uri')
        self.assets_trophy_1st_link      = assets.get('trophy-1st', {}).get('uri')
        self.assets_trophy_2nd_link      = assets.get('trophy-2nd', {}).get('uri')
        self.assets_trophy_3rd_link      = assets.get('trophy-3rd', {}).get('uri')
        self.assets_trophy_4th_link      = assets.get('trophy-4th', {}).get('uri')

    def __repr__(self):
        fields = "\n  ".join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{self.__class__.__name__}(\n  {fields}\n)"
    
    def get_simple_text(self):
        fields = [
            'id',
            'name_international',
            'abbreviation',
            'creation_date',
            'release_year',
            'weblink'
        ]

        parts = [f"{field} = {getattr(self, field)!r}" for field in fields]

        return '\n'.join(parts)
        
class CategoryInfo:
    def __init__(self, data):
        self.id                  = data.get('id')
        self.is_miscellaneous    = data.get('miscellaneous')
        self.name                = data.get('name')
        self.rules               = data.get('rules')
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
        

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'
