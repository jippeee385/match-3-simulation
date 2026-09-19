# Match-3 Difficulty Lab

A data science project exploring game difficulty, player behaviour, and level balancing in a simulated match-3 game inspired Candy Crush Saga.

The goal is to build a small but effective simulation environment that allows us to investigate how level design affects different types of players, and how data science and machine learning can be used to tune the player experience.

## What we're building

The project will progressively develop:

### Match-3 game simulator
Board, swaps, matches, cascades, special candies, blockers and objectives.
Parameterised levels so that difficulty can be systematically varied.
### Player behaviour models
Random players as a baseline.
Heuristic players representing different levels of skill and decision-making.
Stochastic behaviour to represent variation between players.
### Difficulty analysis
Monte Carlo simulation of games.
Win probability, attempts, failure streaks, objective completion and other player-level metrics.
Analysis of how different level parameters affect difficulty across player segments.
### Level balancing and optimisation
Identify which level-design parameters drive difficulty.
Explore trade-offs between challenge, progression and player experience.
Search for level configurations that achieve a desired difficulty profile.
### Reinforcement learning
If I have time, develop an RL agent capable of learning to play the game.
Compare learned behaviour with the simulated player models.
Explore whether increasingly capable agents provide a useful way of estimating level difficulty.

## Core question

How can simulation and data science be used to understand and balance difficulty in a match-3 game?

The project is deliberately focused on the data science and modelling problem rather than graphics or game development. The game engine exists to provide a controlled environment in which player behaviour and level design can be experimentally studied.
