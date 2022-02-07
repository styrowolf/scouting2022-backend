from pydantic import BaseModel
from enum import Enum

class Identifiable(BaseModel):
    id: str

    def assign_id(self):
        pass
    
    def generate_id(derive_from: str):
        pass

    def __eq__(self, other):
        if type(self) == type(other):
            return self.id == other.id
        return False

class AllianceColor(str, Enum):
    BLUE = "blue"
    RED = "red"

class Rung(str, Enum):
    NONE = "none"
    LOW = "low"
    MIDDLE = "middle"
    HIGH = "high"
    TRAVERSAL = "traversal"

    def to_points(self) -> int:
        if self == Rung.LOW:
            return 4
        elif self == Rung.MIDDLE:
            return 6
        elif self == Rung.HIGH:
            return 10
        elif self == Rung.TRAVERSAL: 
            return 15
        else:
            return 0

class Result(str, Enum):
    LOST = "lost"
    DRAW = "draw"
    WON = "won"

class MatchStats(BaseModel):
    taxi: bool
    auto_lower_hub: int
    auto_higher_hub: int
    teleop_lower_hub: int
    teleop_higher_hub: int
    bar: Rung
    dsq_or_no_show: bool

class TeamMatchStats(BaseModel):
    alliance_color: AllianceColor
    team: int
    stats: MatchStats

    def __eq__(self, other):
        if type(self) == type(other):
            return self.team == other.team
        return False

class MatchMetadata(Identifiable):
    name: str
    
    def assign_id(self):
        self.id = MatchMetadata.generate_id(self.name)
    
    def generate_id(name: str):
        return "match-" + name.encode().hex()

class Match(Identifiable):
    name: str
    stats: list[TeamMatchStats]

    def from_name(name: str):
        m = Match(id="", name=name, stats=[])
        m.assign_id()
        return m

    def assign_id(self):
        self.id = Match.generate_id(self.name)
    
    def generate_id(name: str):
        return "match-" + name.encode().hex()

    def put_stats(self, tms: TeamMatchStats):
        try:
            i = self.stats.index(tms)
            self.stats[i] = tms
        except:
            self.stats.append(tms)

    def get_stats(self, team: int):
        query = list(filter(lambda tms: tms.team == team, self.stats))
        if len(query) != 1:
            return None
        return query[0]

    def to_metadata(self):
        return MatchMetadata(name=self.name, id=self.id)

class TournamentMetadata(Identifiable):
    name: str
    matches: list[MatchMetadata]

    def assign_id(self):
        self.id = TournamentMetadata.generate_id(self.name)

    def generate_id(name: str):
        return "tournament-" + name.encode().hex()
        
class Tournament(Identifiable):
    name: str
    matches: list[Match]

    def from_name(name: str):
        t = Tournament(id="", name=name, matches=[])
        t.assign_id()
        return t

    def assign_id(self):
        self.id = Tournament.generate_id(self.name)

    def generate_id(name: str):
        return "tournament-" + name.encode().hex()

    def put_match(self, m: Match):
        try:
            i = self.matches.index(m)
            self.matches[i] = m
        except:
            self.matches.append(m)

    def get_match_by_id(self, id: str):
        query = list(filter(lambda m: m.id == id, self.matches))
        if len(query) != 1:
            return None
        return query[0]

    def to_metadata(self):
        return TournamentMetadata(name=self.name, id=self.id, matches=list(map(Match.to_metadata, self.matches)))

class TeamDataMetadata(BaseModel):
    team: int
    tournaments: list[TournamentMetadata]
        
class TeamData(BaseModel):
    team: int
    tournaments: list[Tournament]

    def put_tournament(self, t: Tournament):
        try:
            i = self.tournaments.index(t)
            self.tournaments[i] = t
        except:
            self.tournaments.append(t)

    def get_tournament_by_id(self, id: str):
        query = list(filter(lambda t: t.id == id, self.tournaments))
        if len(query) != 1:
            return None
        return query[0]

    def to_metadata(self):
        return TeamDataMetadata(team=self.team, tournaments=list(map(Tournament.to_metadata, self.tournaments)))

        