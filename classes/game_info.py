from datetime import datetime, timezone


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
        