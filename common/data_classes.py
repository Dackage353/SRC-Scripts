from dataclasses import dataclass, field
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

        run_date = datetime.strptime(run_data['date'], '%Y-%m-%d') if run_data['date'] else None
        time_submitted = datetime.strptime(run_data['submitted'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) if run_data['submitted'] else None

        players = run_data.get('players', [])
        player_id = run_data['players'][0].get('id') if len(players) > 0 else None

        return Run(
            run_time              = run_data['times']['primary_t'],
            run_time_formatted    = timedelta(seconds=run_data['times']['primary_t']),
            run_date              = run_date,
            time_submitted        = time_submitted,
            time_verified         = run_data['status'].get('verify-date'),
            verified_status       = run_data['status']['status'],
            run_id                = run_data['id'],
            game_id               = run_data['game'],
            category_id           = run_data['category'],
            player_id             = player_id,
            verifier_id           = run_data['status']['examiner']
        )
        
        
@dataclass
class Game:
    game_id: str
    name: str
    abbreviation: str
    release_date: datetime
    platform_ids: list[str] = field(default_factory=list)
    platform_ids: list[str] = field(default_factory=list)
    moderator_ids: list[str] = field(default_factory=list)
    level_ids: list[str] = field(default_factory=list)
        
        
@dataclass
class Category:
    category_id: str
    name: str
    link: str
    run_ids: list[str] = field(default_factory=list)
        

@dataclass
class Level:
    level_id: str
    name: str
    link: str


@dataclass
class Leaderboard:
    game_id: str
    category_id: str