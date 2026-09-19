# Match-3 Game — Technical Design

- We use numpy array for the board with integers to represent the candies
- The default board size is 8x8
- v0: no special candies
- Default agent is a random choice of swaps to try


## Classes
- Game: Controls the overall game flow, mostly checking and resolving the board
- Level: Contains the information for a level: name, move budget, objective, board size, how many candy types, blocker positions (none in v0)
- Board: Like in RL, this represents the current state of the board in play, in a numpy array, the environment
  - candy positions
  - Also contains the environment action resolutions
- Moves: super simple class that holds the single move available: swap two adjacent candies
- State: current state of the game.