# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Coord, Direction, \
    Action, PlaceAction, MoveAction, EatAction, CascadeAction

from referee.game.constants import *


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Cascade game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        self._turn_count = 0
        # initialise empty board state as string (each ".." is placeholder for {color, height})
        self._board = [(None, None) for _ in range(BOARD_N * BOARD_N)]
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED (first player)")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object.
        """

        # Below we have hardcoded actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.

        # During placement phase (first 8 turns total, 4 per player)
        if self._turn_count < 4:
            match self._color:
                case PlayerColor.RED:
                    print("Testing: RED is playing a PLACE action")
                    return PlaceAction(Coord(0, self._turn_count))
                case PlayerColor.BLUE:
                    print("Testing: BLUE is playing a PLACE action")
                    return PlaceAction(Coord(7, self._turn_count))

        # During play phase
        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a MOVE action")
                return MoveAction(Coord(0, 0), Direction.Down)
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a MOVE action")
                return MoveAction(Coord(7, 0), Direction.Up)

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state.
        """
        if color == self._color:
            self._turn_count += 1

        # There are four possible action types: PLACE, MOVE, EAT, and CASCADE.
        # Below we check which type of action was played and print out the
        # details of the action for demonstration purposes. You should replace
        # this with your own logic to update your agent's internal game state.
        match action:
            case PlaceAction(coord):
                self._board[coord.r * BOARD_N + coord.c] = (color, 3)
                print(f"Testing: {color} played PLACE action at {coord}")
            case MoveAction(coord, direction):
                make_move_action(self._board, coord, direction)
                print(f"Testing: {color} played MOVE action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
            case EatAction(coord, direction):
                make_eat_action(self._board, coord, direction)
                print(f"Testing: {color} played EAT action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
            case CascadeAction(coord, direction):
                make_cascade_action(self._board, coord, direction)
                print(f"Testing: {color} played CASCADE action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
            case _:
                raise ValueError(f"Unknown action type: {action}")
            

def make_cascade_action(board: list, coord: Coord, direction: Direction) -> None:
    """
    updates board state according to coord and cascade direction assuming cascade
    """
    r = coord.r
    c = coord.c
    i = r * BOARD_N + c
    height = int(board[i][1])

    for n in range(1, height + 1):
        target_r = r + direction.r * n
        target_c = c + direction.c * n
        if not (0 <= target_r < BOARD_N) or not (0 <= target_c < BOARD_N):
            return
        target_i = target_r * BOARD_N + target_c
        target_piece = board[target_i]
        if target_piece[0] is not None:
            push_stack(board, target_r, target_c, direction)
        board[target_i] = (board[i][0], 1)

    board[i] = (None, None)

def push_stack(board: list, r: int, c: int, direction: Direction) -> None:
    """
    pushes stack at index in direction until it reaches empty space or falls off board
    """
    i = r * BOARD_N + c
    if board[i][0] is None:
        return
    next_r = r + direction.r
    next_c = c + direction.c
    next_i = next_r * BOARD_N + next_c
    if not (0 <= next_r < BOARD_N) or not (0 <= next_c < BOARD_N):
        return
    push_stack(board, next_r, next_c, direction)
    board[next_i] = board[i]
            
def make_eat_action(board: list, coord: Coord, direction: Direction) -> None:
    """
    updates board state according to coord and eat direction assuming eat is valid
    """
    r = coord.r
    c = coord.c
    i = r * BOARD_N + c

    new_r = (r + direction.r)
    assert(0 <= new_r < BOARD_N)
    new_c = (c + direction.c)
    assert(0 <= new_c < BOARD_N)

    new_i = new_r * BOARD_N + new_c

    current_piece = board[i]
    board[new_i] = current_piece
    board[i] = (None, None)

def make_move_action(board: list, coord: Coord, direction: Direction) -> None:
    """
    updates board state according to coord and move direction assuming move/merge is valid
    """
    r = coord.r
    c = coord.c
    i = r * BOARD_N + c

    new_r = (r + direction.r)
    assert(0 <= new_r < BOARD_N)
    new_c = (c + direction.c)
    assert(0 <= new_c < BOARD_N)
    new_i = new_r * BOARD_N + new_c

    current_piece = board[i]
    target_piece = board[new_i]
    if target_piece[0] == current_piece[0]:
        # if same color, merge
        new_height = current_piece[1] + target_piece[1]
        board[new_i] = (current_piece[0], new_height)
    else:
        board[new_i] = current_piece
    board[i] = (None, None)