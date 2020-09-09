from collections import namedtuple


class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self


class Move:  # <1>
    def __init__(self, point=None, is_restart=False,  is_regret=False, is_pass=False, is_resign=False, is_turn_back=False):
        assert (point is not None) ^ is_restart ^ is_regret ^ is_pass ^ is_resign ^ is_turn_back
        self.point = point
        self.is_play = (self.point is not None)
        self.is_restart = is_restart
        self.is_regret = is_regret
        self.is_pass = is_pass
        self.is_resign = is_resign
        self.is_turn_back = is_turn_back

    @classmethod
    def play(cls, point):  # <2>
        return Move(point=point)

    @classmethod
    def restart(cls):  # <3>
        return Move(is_restart=True)

    @classmethod
    def regret(cls):  # <3>
        return Move(is_regret=True)

    @classmethod
    def pass_turn(cls):  # <3>
        return Move(is_pass=True)

    @classmethod
    def resign(cls):  # <4>
        return Move(is_resign=True)

    @classmethod
    def turn_back(cls):  # <4>
        return Move(is_turn_back=True)


class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def without_liberty(self, point):  # <2>
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    # <1> `stones` and `liberties` are now immutable `frozenset` instances
    # <2> The `without_liberty` methods replaces the previous `remove_liberty` method...
    # <3> ... and `with_liberty` replaces `add_liberty`.
    # end::fast_go_strings[]

    def merged_with(self, string):
        """Return a new string containing all stones in both strings."""
        assert string.color == self.color
        combined_stones = self.stones | string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
               self.color == other.color and \
               self.stones == other.stones and \
               self.liberties == other.liberties

    def __deepcopy__(self, memodict={}):
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))

    '''
    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):  # <2>
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
               self.color == other.color and \
               self.stones == other.stones and \
               self.liberties == other.liberties
    '''