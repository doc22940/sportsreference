import pandas as pd
import re
from .constants import (ADVANCED_OPPONENT_STATS_URL,
                        ADVANCED_STATS_URL,
                        BASIC_OPPONENT_STATS_URL,
                        BASIC_STATS_URL,
                        PARSING_SCHEME)
from pyquery import PyQuery as pq
from .. import utils
from .conferences import Conferences
from .schedule import Schedule


class Team:
    """
    An object containing all of a team's season information.

    Finds and parses all team stat information and identifiers, such as full
    and short names, and sets them as properties which can be directly read
    from for easy reference.

    Parameters
    ----------
    team_data : string
        A string containing all of the rows of stats for a given team. If
        multiple tables are being referenced, this will be comprised of
        multiple rows in a single string.
    team_conference : string (optional)
        A string of the team's conference abbreviation, such as 'big-12'.
    year : string (optional)
        The requested year to pull stats from.
    """
    def __init__(self, team_data, team_conference=None, year=None):
        self._team_conference = team_conference
        self._year = year
        self._abbreviation = None
        self._name = None
        self._games_played = None
        self._wins = None
        self._losses = None
        self._win_percentage = None
        self._simple_rating_system = None
        self._strength_of_schedule = None
        self._conference_wins = None
        self._conference_losses = None
        self._home_wins = None
        self._home_losses = None
        self._away_wins = None
        self._away_losses = None
        self._points = None
        self._opp_points = None
        self._minutes_played = None
        self._field_goals = None
        self._field_goal_attempts = None
        self._field_goal_percentage = None
        self._three_point_field_goals = None
        self._three_point_field_goal_attempts = None
        self._three_point_field_goal_percentage = None
        self._free_throws = None
        self._free_throw_attempts = None
        self._free_throw_percentage = None
        self._offensive_rebounds = None
        self._total_rebounds = None
        self._assists = None
        self._steals = None
        self._blocks = None
        self._turnovers = None
        self._personal_fouls = None
        self._opp_field_goals = None
        self._opp_field_goal_attempts = None
        self._opp_field_goal_percentage = None
        self._opp_three_point_field_goals = None
        self._opp_three_point_field_goal_attempts = None
        self._opp_three_point_field_goal_percentage = None
        self._opp_free_throws = None
        self._opp_free_throw_attempts = None
        self._opp_free_throw_percentage = None
        self._opp_offensive_rebounds = None
        self._opp_total_rebounds = None
        self._opp_assists = None
        self._opp_steals = None
        self._opp_blocks = None
        self._opp_turnovers = None
        self._opp_personal_fouls = None
        self._pace = None
        self._offensive_rating = None
        self._free_throw_attempt_rate = None
        self._three_point_attempt_rate = None
        self._true_shooting_percentage = None
        self._total_rebound_percentage = None
        self._assist_percentage = None
        self._steal_percentage = None
        self._block_percentage = None
        self._effective_field_goal_percentage = None
        self._turnover_percentage = None
        self._offensive_rebound_percentage = None
        self._free_throws_per_field_goal_attempt = None
        self._opp_offensive_rating = None
        self._opp_free_throw_attempt_rate = None
        self._opp_three_point_attempt_rate = None
        self._opp_true_shooting_percentage = None
        self._opp_total_rebound_percentage = None
        self._opp_assist_percentage = None
        self._opp_steal_percentage = None
        self._opp_block_percentage = None
        self._opp_effective_field_goal_percentage = None
        self._opp_turnover_percentage = None
        self._opp_offensive_rebound_percentage = None
        self._opp_free_throws_per_field_goal_attempt = None

        self._parse_team_data(team_data)

    def _parse_team_data(self, team_data):
        """
        Parses a value for every attribute.

        This function looks through every attribute and retrieves the value
        according to the parsing scheme and index of the attribute from the
        passed HTML data. Once the value is retrieved, the attribute's value is
        updated with the returned result.

        Note that this method is called directly once Team is invoked and does
        not need to be called manually.

        Parameters
        ----------
        team_data : string
            A string containing all of the rows of stats for a given team. If
            multiple tables are being referenced, this will be comprised of
            multiple rows in a single string.
        """
        for field in self.__dict__:
            if field == '_year' or \
               field == '_team_conference':
                continue
            value = utils._parse_field(PARSING_SCHEME,
                                       team_data,
                                       # Remove the '_' from the name
                                       str(field)[1:])
            setattr(self, field, value)

    @property
    def dataframe(self):
        """
        Returns a pandas DataFrame containing all other class properties and
        values. The index for the DataFrame is the string abbreviation of the
        team, such as 'PURDUE'.
        """
        fields_to_include = {
            'abbreviation': self.abbreviation,
            'assist_percentage': self.assist_percentage,
            'assists': self.assists,
            'away_losses': self.away_losses,
            'away_wins': self.away_wins,
            'block_percentage': self.block_percentage,
            'blocks': self.blocks,
            'conference': self.conference,
            'conference_losses': self.conference_losses,
            'conference_wins': self.conference_wins,
            'effective_field_goal_percentage':
            self.effective_field_goal_percentage,
            'field_goal_attempts': self.field_goal_attempts,
            'field_goal_percentage': self.field_goal_percentage,
            'field_goals': self.field_goals,
            'free_throw_attempt_rate': self.free_throw_attempt_rate,
            'free_throw_attempts': self.free_throw_attempts,
            'free_throw_percentage': self.free_throw_percentage,
            'free_throws': self.free_throws,
            'free_throws_per_field_goal_attempt':
            self.free_throws_per_field_goal_attempt,
            'games_played': self.games_played,
            'home_losses': self.home_losses,
            'home_wins': self.home_wins,
            'losses': self.losses,
            'minutes_played': self.minutes_played,
            'name': self.name,
            'offensive_rating': self.offensive_rating,
            'offensive_rebound_percentage': self.offensive_rebound_percentage,
            'offensive_rebounds': self.offensive_rebounds,
            'opp_assist_percentage': self.opp_assist_percentage,
            'opp_assists': self.opp_assists,
            'opp_block_percentage': self.opp_block_percentage,
            'opp_blocks': self.opp_blocks,
            'opp_effective_field_goal_percentage':
            self.opp_effective_field_goal_percentage,
            'opp_field_goal_attempts': self.opp_field_goal_attempts,
            'opp_field_goal_percentage': self.opp_field_goal_percentage,
            'opp_field_goals': self.opp_field_goals,
            'opp_free_throw_attempt_rate': self.opp_free_throw_attempt_rate,
            'opp_free_throw_attempts': self.opp_free_throw_attempts,
            'opp_free_throw_percentage': self.opp_free_throw_percentage,
            'opp_free_throws': self.opp_free_throws,
            'opp_free_throws_per_field_goal_attempt':
            self.opp_free_throws_per_field_goal_attempt,
            'opp_offensive_rating': self.opp_offensive_rating,
            'opp_offensive_rebound_percentage':
            self.opp_offensive_rebound_percentage,
            'opp_offensive_rebounds': self.opp_offensive_rebounds,
            'opp_personal_fouls': self.opp_personal_fouls,
            'opp_points': self.opp_points,
            'opp_steal_percentage': self.opp_steal_percentage,
            'opp_steals': self.opp_steals,
            'opp_three_point_attempt_rate': self.opp_three_point_attempt_rate,
            'opp_three_point_field_goal_attempts':
            self.opp_three_point_field_goal_attempts,
            'opp_three_point_field_goal_percentage':
            self.opp_three_point_field_goal_percentage,
            'opp_three_point_field_goals': self.opp_three_point_field_goals,
            'opp_total_rebound_percentage': self.opp_total_rebound_percentage,
            'opp_total_rebounds': self.opp_total_rebounds,
            'opp_true_shooting_percentage': self.opp_true_shooting_percentage,
            'opp_turnover_percentage': self.opp_turnover_percentage,
            'opp_turnovers': self.opp_turnovers,
            'pace': self.pace,
            'personal_fouls': self.personal_fouls,
            'points': self.points,
            'simple_rating_system': self.simple_rating_system,
            'steal_percentage': self.steal_percentage,
            'steals': self.steals,
            'strength_of_schedule': self.strength_of_schedule,
            'three_point_attempt_rate': self.three_point_attempt_rate,
            'three_point_field_goal_attempts':
            self.three_point_field_goal_attempts,
            'three_point_field_goal_percentage':
            self.three_point_field_goal_percentage,
            'three_point_field_goals': self.three_point_field_goals,
            'total_rebound_percentage': self.total_rebound_percentage,
            'total_rebounds': self.total_rebounds,
            'true_shooting_percentage': self.true_shooting_percentage,
            'turnover_percentage': self.turnover_percentage,
            'turnovers': self.turnovers,
            'win_percentage': self.win_percentage,
            'wins': self.wins
        }
        return pd.DataFrame([fields_to_include], index=[self._abbreviation])

    @property
    def conference(self):
        """
        Returns a ``string`` of the team's conference abbreviation, such as
        'big-12' for the Big 12 Conference.
        """
        return self._team_conference

    @property
    def abbreviation(self):
        """
        Returns a ``string`` of the team's short name, such as 'PURDUE' for the
        Purdue Boilermakers.
        """
        return self._abbreviation

    @property
    def schedule(self):
        """
        Returns an instance of the Schedule class containing the team's
        complete schedule for the season.
        """
        return Schedule(self._abbreviation, self._year)

    @property
    def name(self):
        """
        Returns a ``string`` of the team's full name, such as 'Purdue
        Boilermakers'.
        """
        return self._name

    @property
    def games_played(self):
        """
        Returns an ``int`` of the total number of games the team has played
        during the season.
        """
        return int(self._games_played)

    @property
    def wins(self):
        """
        Returns an ``int`` of the total number of games the team won during the
        season.
        """
        return int(self._wins)

    @property
    def losses(self):
        """
        Returns an ``int`` of the total number of games the team lost during
        the season.
        """
        return int(self._losses)

    @property
    def win_percentage(self):
        """
        Returns a ``float`` of the number of wins divided by the number of
        games played during the season. Percentage ranges from 0-1.
        """
        return float(self._win_percentage)

    @property
    def simple_rating_system(self):
        """
        Returns a ``float`` of the team's average point differential compared
        to the strength of schedule. Higher values indicate stronger teams. An
        average team is denoted with 0.0. Negative numbers are comparatively
        worse than average.
        """
        return float(self._simple_rating_system)

    @property
    def strength_of_schedule(self):
        """
        Returns a ``float`` of the team's strength of schedule based on the
        points above and below average. An average strength of schedule is
        denoted with 0.0. Negative numbers are comparatively easier than
        average.
        """
        return float(self._strength_of_schedule)

    @property
    def conference_wins(self):
        """
        Returns an ``int`` of the total number of conference games the team won
        during the season.
        """
        return int(self._conference_wins)

    @property
    def conference_losses(self):
        """
        Returns an ``int`` of the total number of conference games the team
        lost during the season.
        """
        return int(self._conference_losses)

    @property
    def home_wins(self):
        """
        Returns an ``int`` of the total number of home games the team won
        during the season.
        """
        return int(self._home_wins)

    @property
    def home_losses(self):
        """
        Returns an ``int`` of the total number of home games the team lost
        during the season.
        """
        return int(self._home_losses)

    @property
    def away_wins(self):
        """
        Returns an ``int`` of the total number of away games the team won
        during the season.
        """
        return int(self._away_wins)

    @property
    def away_losses(self):
        """
        Returns an ``int`` of the total number of away games the team lost
        during the season.
        """
        return int(self._away_losses)

    @property
    def points(self):
        """
        Returns an ``int`` of the total number of points the team scored during
        the season.
        """
        return int(self._points)

    @property
    def opp_points(self):
        """
        Returns an ``int`` of the total number of points opponents have scored
        during the season.
        """
        return int(self._opp_points)

    @property
    def minutes_played(self):
        """
        Returns an ``int`` of the total number of minutes played by the team
        during the season.
        """
        return int(self._minutes_played)

    @property
    def field_goals(self):
        """
        Returns an ``int`` of the total number of field goals made during the
        season.
        """
        return int(self._field_goals)

    @property
    def field_goal_attempts(self):
        """
        Returns an ``int`` of the total number of field goal attempts during
        the season.
        """
        return int(self._field_goal_attempts)

    @property
    def field_goal_percentage(self):
        """
        Returns a ``float`` of the number of field goals made divided by the
        total number of field goal attempts. Percentage ranges from 0-1.
        """
        return float(self._field_goal_percentage)

    @property
    def three_point_field_goals(self):
        """
        Returns an ``int`` of the total number of three point field goals made
        during the season.
        """
        return int(self._three_point_field_goals)

    @property
    def three_point_field_goal_attempts(self):
        """
        Returns an ``int`` of the total number of three point field goal
        attempts during the season.
        """
        return int(self._three_point_field_goal_attempts)

    @property
    def three_point_field_goal_percentage(self):
        """
        Returns a ``float`` of the number of three point field goals made
        divided by the number of three point field goal attempts. Percentage
        ranges from 0-1.
        """
        return float(self._three_point_field_goal_percentage)

    @property
    def free_throws(self):
        """
        Returns an ``int`` of the total number of free throws made during the
        season.
        """
        return int(self._free_throws)

    @property
    def free_throw_attempts(self):
        """
        Returns an ``int`` of the total number of free throw attempts during
        the season.
        """
        return int(self._free_throw_attempts)

    @property
    def free_throw_percentage(self):
        """
        Returns a ``float`` of the number of free throws made divided by the
        number of free throw attempts during the season.
        """
        return float(self._free_throw_percentage)

    @property
    def offensive_rebounds(self):
        """
        Returns an ``int`` of the total number of offensive rebounds during the
        season.
        """
        return int(self._offensive_rebounds)

    @property
    def total_rebounds(self):
        """
        Returns an ``int`` of the total number of rebounds during the season.
        """
        return int(self._total_rebounds)

    @property
    def assists(self):
        """
        Returns an ``int`` of the total number of assists during the season.
        """
        return int(self._assists)

    @property
    def steals(self):
        """
        Returns an ``int`` of the total number of steals during the season.
        """
        return int(self._steals)

    @property
    def blocks(self):
        """
        Returns an ``int`` of the total number of blocks during the season.
        """
        return int(self._blocks)

    @property
    def turnovers(self):
        """
        Returns an ``int`` of the total number of turnovers during the season.
        """
        return int(self._turnovers)

    @property
    def personal_fouls(self):
        """
        Returns an ``int`` of the total number of personal fouls during the
        season.
        """
        return int(self._personal_fouls)

    @property
    def opp_field_goals(self):
        """
        Returns an ``int`` of the total number of field goals made during the
        season by opponents.
        """
        return int(self._opp_field_goals)

    @property
    def opp_field_goal_attempts(self):
        """
        Returns an ``int`` of the total number of field goal attempts during
        the season by opponents.
        """
        return int(self._opp_field_goal_attempts)

    @property
    def opp_field_goal_percentage(self):
        """
        Returns a ``float`` of the number of field goals made divided by the
        total number of field goal attempts by opponents. Percentage ranges
        from 0-1.
        """
        return float(self._opp_field_goal_percentage)

    @property
    def opp_three_point_field_goals(self):
        """
        Returns an ``int`` of the total number of three point field goals made
        during the season by opponents.
        """
        return int(self._opp_three_point_field_goals)

    @property
    def opp_three_point_field_goal_attempts(self):
        """
        Returns an ``int`` of the total number of three point field goal
        attempts during the season by opponents.
        """
        return int(self._opp_three_point_field_goal_attempts)

    @property
    def opp_three_point_field_goal_percentage(self):
        """
        Returns a ``float`` of the number of three point field goals made
        divided by the number of three point field goal attempts by opponents.
        Percentage ranges from 0-1.
        """
        return float(self._opp_three_point_field_goal_percentage)

    @property
    def opp_free_throws(self):
        """
        Returns an ``int`` of the total number of free throws made during the
        season by opponents.
        """
        return int(self._opp_free_throws)

    @property
    def opp_free_throw_attempts(self):
        """
        Returns an ``int`` of the total number of free throw attempts during
        the season by opponents.
        """
        return int(self._opp_free_throw_attempts)

    @property
    def opp_free_throw_percentage(self):
        """
        Returns a ``float`` of the number of free throws made divided by the
        number of free throw attempts during the season by opponents.
        """
        return float(self._opp_free_throw_percentage)

    @property
    def opp_offensive_rebounds(self):
        """
        Returns an ``int`` of the total number of offensive rebounds during the
        season by opponents.
        """
        return int(self._opp_offensive_rebounds)

    @property
    def opp_total_rebounds(self):
        """
        Returns an ``int`` of the total number of rebounds during the season by
        opponents.
        """
        return int(self._opp_total_rebounds)

    @property
    def opp_assists(self):
        """
        Returns an ``int`` of the total number of assists during the season by
        opponents.
        """
        return int(self._opp_assists)

    @property
    def opp_steals(self):
        """
        Returns an ``int`` of the total number of steals during the season by
        opponents.
        """
        return int(self._opp_steals)

    @property
    def opp_blocks(self):
        """
        Returns an ``int`` of the total number of blocks during the season by
        opponents.
        """
        return int(self._opp_blocks)

    @property
    def opp_turnovers(self):
        """
        Returns an ``int`` of the total number of turnovers during the season
        by opponents.
        """
        return int(self._opp_turnovers)

    @property
    def opp_personal_fouls(self):
        """
        Returns an ``int`` of the total number of personal fouls during the
        season by opponents.
        """
        return int(self._opp_personal_fouls)

    @property
    def pace(self):
        """
        Returns a ``float`` of the average number of possessions per 40
        minutes.
        """
        return float(self._pace)

    @property
    def offensive_rating(self):
        """
        Returns a ``float`` of the average number of points scored per 100
        possessions.
        """
        return float(self._offensive_rating)

    @property
    def free_throw_attempt_rate(self):
        """
        Returns a ``float`` of the average number of free throw attempts per
        field goal attempt.
        """
        return float(self._free_throw_attempt_rate)

    @property
    def three_point_attempt_rate(self):
        """
        Returns a ``float`` of the percentage of field goal attempts from
        3-point range. Percentage ranges from 0-1.
        """
        return float(self._three_point_attempt_rate)

    @property
    def true_shooting_percentage(self):
        """
        Returns a ``float`` of the team's true shooting percentage which
        considers free throws, 2-point field goals, and 3-point field goals.
        Percentage ranges from 0-1.
        """
        return float(self._true_shooting_percentage)

    @property
    def total_rebound_percentage(self):
        """
        Returns a ``float`` of the percentage of available rebounds a team
        grabbed.
        Percentage ranges from 0-100.
        """
        return float(self._total_rebound_percentage)

    @property
    def assist_percentage(self):
        """
        Returns a ``float`` of the percentage of field goals that were
        assisted.
        Percentage ranges from 0-100.
        """
        return float(self._assist_percentage)

    @property
    def steal_percentage(self):
        """
        Returns a ``float`` of the percentage of opponent possessions that
        ended in a steal. Percentage ranges from 0-100.
        """
        return float(self._steal_percentage)

    @property
    def block_percentage(self):
        """
        Returns a ``float`` of the percentage of 2-point field goals by the
        opponent that were blocked. Percentage ranges from 0-100.
        """
        return float(self._block_percentage)

    @property
    def effective_field_goal_percentage(self):
        """
        Returns a ``float`` of the field goal percentage while giving extra
        weight to 3-point field goals. Percentage ranges from 0-1.
        """
        return float(self._effective_field_goal_percentage)

    @property
    def turnover_percentage(self):
        """
        Returns a ``float`` of the number of times the team turned the ball
        over per 100 possessions.
        """
        return float(self._turnover_percentage)

    @property
    def offensive_rebound_percentage(self):
        """
        Returns a ``float`` of the percentage of available offensive rebounds a
        team grabbed. Percentage ranges from 0-100.
        """
        return float(self._offensive_rebound_percentage)

    @property
    def free_throws_per_field_goal_attempt(self):
        """
        Returns a ``float`` of the number of free throws per field goal
        attempt.
        """
        return float(self._free_throws_per_field_goal_attempt)

    @property
    def opp_offensive_rating(self):
        """
        Returns a ``float`` of the average number of points scored per 100
        possessions by the opponent.
        """
        return float(self._opp_offensive_rating)

    @property
    def opp_free_throw_attempt_rate(self):
        """
        Returns a ``float`` of the average number of free throw attempts per
        field goal attempt by the opponent.
        """
        return float(self._opp_free_throw_attempt_rate)

    @property
    def opp_three_point_attempt_rate(self):
        """
        Returns a ``float`` of the percentage of field goal attempts from
        3-point range by the opponent. Percentage ranges from 0-1.
        """
        return float(self._opp_three_point_attempt_rate)

    @property
    def opp_true_shooting_percentage(self):
        """
        Returns a ``float`` of the opponent's true shooting percentage which
        considers free throws, 2-point field goals, and 3-point field goals.
        Percentage ranges from 0-1.
        """
        return float(self._opp_true_shooting_percentage)

    @property
    def opp_total_rebound_percentage(self):
        """
        Returns a ``float`` of the percentage of available rebounds the
        opponent grabbed. Percentage ranges from 0-100.
        """
        return float(self._opp_total_rebound_percentage)

    @property
    def opp_assist_percentage(self):
        """
        Returns a ``float`` of the percentage of the opponent's field goals
        that were assisted. Percentage ranges from 0-100.
        """
        return float(self._opp_assist_percentage)

    @property
    def opp_steal_percentage(self):
        """
        Returns a ``float`` of the percentage of possessions that ended in a
        steal by the opponent. Percentage ranges from 0-100.
        """
        return float(self._opp_steal_percentage)

    @property
    def opp_block_percentage(self):
        """
        Returns a ``float`` of the percentage of 2-point field goals that were
        blocked by the opponent. Percentage ranges from 0-100.
        """
        return float(self._opp_block_percentage)

    @property
    def opp_effective_field_goal_percentage(self):
        """
        Returns a ``float`` of the opponent's field goal percentage while
        giving extra weight to 3-point field goals. Percentage ranges from 0-1.
        """
        return float(self._opp_effective_field_goal_percentage)

    @property
    def opp_turnover_percentage(self):
        """
        Returns a ``float`` of the number of times the opponent turned the ball
        over per 100 possessions.
        """
        return float(self._opp_turnover_percentage)

    @property
    def opp_offensive_rebound_percentage(self):
        """
        Returns a ``float`` of the percentage of available offensive rebounds
        the opponent grabbed. Percentage ranges from 0-100.
        """
        return float(self._opp_offensive_rebound_percentage)

    @property
    def opp_free_throws_per_field_goal_attempt(self):
        """
        Returns a ``float`` of the number of free throws per field goal attempt
        by the opponent.
        """
        return float(self._opp_free_throws_per_field_goal_attempt)


class Teams:
    """
    A list of all NCAA Men's Basketball teams and their stats in a given year.

    Finds and retrieves a list of all NCAA Men's Basketball teams from
    www.sports-reference.com and creates a Team instance for every team that
    participated in the league in a given year. The Team class comprises a list
    of all major stats and a few identifiers for the requested season.

    Parameters
    ----------
    year : string (optional)
        The requested year to pull stats from.
    """
    def __init__(self, year=None):
        self._teams = []
        self._conferences_dict = Conferences(year).team_conference

        self._retrieve_all_teams(year)

    def __getitem__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        short name.

        Parameters
        ----------
        abbreviation : string
            An NCAAB team's short name (ie. 'PURDUE' for the Purdue
            Boilermakers).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.

        Raises
        ------
        ValueError
            If the requested team is not present within the Teams list.
        """
        for team in self._teams:
            if team.abbreviation.upper() == abbreviation.upper():
                return team
        raise ValueError('Team abbreviation %s not found' % abbreviation)

    def __call__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        short name. This method is a wrapper for __getitem__.

        Parameters
        ----------
        abbreviation : string
            An NCAAB team's short name (ie. 'PURDUE' for the Purdue
            Boilermakers).

        Returns
        -------
        Team instance
            if the requested team can be found, its Team instance is returned
        """
        return self.__getitem__(abbreviation)

    def __repr__(self):
        """Returns a ``list`` of all NCAAB teams for the given season."""
        return self._teams

    def __iter__(self):
        """Returns an iterator of all of the NCAAB teams for a given season."""
        return iter(self.__repr__())

    def __len__(self):
        """Returns the number of NCAAB teams for a given season."""
        return len(self.__repr__())

    def _add_stats_data(self, teams_list, team_data_dict):
        """
        Add a team's stats row to a dictionary.

        Pass table contents and a stats dictionary of all teams to accumulate
        all stats for each team in a single variable.

        Parameters
        ----------
        teams_list : generator
            A generator of all row items in a given table.
        team_data_dict : {str: {'data': str}} dictionary
            A dictionary where every key is the team's abbreviation and every
            value is another dictionary with a 'data' key which contains the
            string version of the row data for the matched team.

        Returns
        -------
        dictionary
            An updated version of the team_data_dict with the passed table row
            information included.
        """
        for team_data in teams_list:
            if 'class="over_header thead"' in str(team_data) or\
               'class="thead"' in str(team_data):
                continue
            abbr = utils._parse_field(PARSING_SCHEME,
                                      team_data,
                                      'abbreviation')
            try:
                team_data_dict[abbr]['data'] += team_data
            except KeyError:
                team_data_dict[abbr] = {'data': team_data}
        return team_data_dict

    def _retrieve_all_teams(self, year):
        """
        Find and create Team instances for all teams in the given season.

        For a given season, parses the specified NCAAB stats table and finds
        all requested stats. Each team then has a Team instance created which
        includes all requested stats and a few identifiers, such as the team's
        name and abbreviation. All of the individual Team instances are added
        to a list.

        Note that this method is called directly once Teams is invoked and does
        not need to be called manually.

        Parameters
        ----------
        year : string
            The requested year to pull stats from.
        """
        team_data_dict = {}

        if not year:
            year = utils._find_year_for_season('ncaab')
        doc = pq(BASIC_STATS_URL % year)
        teams_list = utils._get_stats_table(doc, 'table#basic_school_stats')
        doc = pq(BASIC_OPPONENT_STATS_URL % year)
        opp_list = utils._get_stats_table(doc, 'table#basic_opp_stats')
        doc = pq(ADVANCED_STATS_URL % year)
        adv_teams_list = utils._get_stats_table(doc, 'table#adv_school_stats')
        doc = pq(ADVANCED_OPPONENT_STATS_URL % year)
        adv_opp_list = utils._get_stats_table(doc, 'table#adv_opp_stats')

        for stats_list in [teams_list, opp_list, adv_teams_list, adv_opp_list]:
            team_data_dict = self._add_stats_data(stats_list, team_data_dict)

        for team_name, team_data in team_data_dict.items():
            team = Team(team_data['data'],
                        self._conferences_dict[team_name.lower()],
                        year)
            self._teams.append(team)

    @property
    def dataframes(self):
        """
        Returns a pandas DataFrame where each row is a representation of the
        Team class. Rows are indexed by the team abbreviation.
        """
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)
