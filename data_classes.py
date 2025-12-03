from dataclasses import dataclass
from datetime import datetime, timezone
from datetime import timedelta

@dataclass
class Run:
    run_id: str
    run_time: float
    run_time_formatted: timedelta
    run_date: datetime
    time_submitted: datetime
    time_verified: datetime
    verified_status: str
    game_id: str
    category_id: str
    player_id: str
    verifier_id: str        
    
    @staticmethod
    def create_from_json(run_data):
        return Run(
            run_time              = run_data['times']['primary_t'],
            run_time_formatted    = timedelta(seconds=run_data['times']['primary_t']),
            run_date              = datetime.strptime(run_data['date'], '%Y-%m-%d'),
            time_submitted        = datetime.strptime(run_data['submitted'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc),
            time_verified         = run_data['status'].get('verify-date'),
            verified_status       = run_data['status']['status'],
            run_id                = run_data['id'],
            game_id               = run_data['game'],
            category_id           = run_data['category'],
            player_id             = run_data['players'][0]['id'],
            verifier_id           = run_data['status']['examiner']
        )
        
        
@dataclass
class Game:
    def __init__(game_id, name, abbreviation, release_date, platform_ids, moderator_ids, level_ids):
        self.game_id = game_id
        self.name = name
        self.abbreviation = abbreviation
        self.release_date = release_date
        self.platform_ids = platform_ids
        self.moderator_ids = moderator_ids
        self.level_ids = level_ids
        
        
class Category:
    def __init__(category_id, name, link, run_ids):
        self.category_id = category_id
        self.name = name
        self.link = link
        self.run_ids = run_ids
        
        
class Level:
    def __init__(level_id, name, link):
        self.level_id = level_id
        self.name = name
        self.link = link
    