from dataclasses import dataclass, field

@dataclass
class SingleStar:
    id: str
    level_id: str
    game_id: str
    name: str