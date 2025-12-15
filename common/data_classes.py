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
    def create_from_json(data):

        run_date = datetime.strptime(data['date'], '%Y-%m-%d') if data['date'] else None
        time_submitted = datetime.strptime(data['submitted'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) if data['submitted'] else None

        players = data.get('players', [])
        player_id = data['players'][0].get('id') if len(players) > 0 else None

        return Run(
            run_time              = data['times']['primary_t'],
            run_time_formatted    = timedelta(seconds=data['times']['primary_t']),
            run_date              = run_date,
            time_submitted        = time_submitted,
            time_verified         = data['status'].get('verify-date'),
            verified_status       = data['status']['status'],
            run_id                = data['id'],
            game_id               = data['game'],
            category_id           = data['category'],
            player_id             = player_id,
            verifier_id           = data['status']['examiner']
        )
        
        
@dataclass
class Game:
    game_id: str
    name: str
    abbreviation: str
    release_date: datetime
    super_moderator_ids: list[str] = field(default_factory=list)
    moderator_ids: list[str] = field(default_factory=list)
    platform_ids: list[str] = field(default_factory=list)
    category_ids: list[str] = field(default_factory=list)
    level_ids: list[str] = field(default_factory=list)

    @staticmethod
    def create_from_json(data):
        release_date = datetime.strptime(data['release-date'], '%Y-%m-%d') if data['release-date'] else None

        super_moderator_ids = []
        moderator_ids = []

        for id, type in data['moderators'].items():
            if type == 'super-moderator':
                super_moderator_ids.append(id)
            elif type == 'moderator':
                moderator_ids.append(id)

        

        return Game(
            game_id                = data['id'],
            name                   = data['names']['international'],
            abbreviation           = data['abbreviation'],
            release_date           = release_date,
            super_moderator_ids    = super_moderator_ids,
            moderator_ids          = moderator_ids,
            platform_ids           = data['platforms'],
            category_ids           = [category['id'] for category in data['categories']['data']],
            level_ids              = [level['id'] for level in data['levels']['data']]
        )
        
        
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