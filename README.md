# Checkers CLI with AI

## Overview

This project is a command-line-based implementation of the classic game of Checkers, currently being enhanced with AI
features. The goal is to create an intelligent opponent that can play against the user, with multiple levels of
complexity.

### Current Status

- **Game Logic**:
    - Basic movement and capturing rules have been implemented.
    - Working on finalizing king movement and capture logic.
    - Adding game state tracking for turn management and win conditions.

### AI Development Roadmap

The current focus is on integrating AI capabilities into the checkers game. Below is the roadmap for AI implementation,
from simpler approaches to more advanced strategies:

1. **A\* Search Algorithm**:
    - Currently working towards implementing **A*** to help the AI evaluate the best moves based on a cost function.
    - The cost function will prioritize capturing opponent pieces and kinging moves.

2. **Minimax Algorithm**:
    - Planning to build a **Minimax-based AI** with **alpha-beta pruning** to enhance move evaluation efficiency.
    - Alpha-beta pruning will reduce the number of board states evaluated, providing better performance while still
      making intelligent decisions.

3. **Considering: Monte Carlo Tree Search (MCTS)**:
    - Evaluating the possibility of using **MCTS** for decision-making.
    - MCTS will allow the AI to make decisions based on the results of multiple simulated games, providing an adaptive
      and probabilistic approach.

4. **Considering: AlphaZero-Inspired AI**:
    - Exploring a **simplified neural network** model inspired by **AlphaZero**.
    - The network will eventually assist in evaluating board states and guiding the search for optimal moves, combining
      MCTS with learned strategies.

### Upcoming Features

- **King Logic Implementation**:
    - Finish implementation of king movement, including capturing both forward and backward.

- **Game State Tracking**:
    - Implement a turn tracker, win condition detection, and a move counter.

### Technology and Tools

- **Language**: Python
- **AI Algorithms in Progress**: A*, Minimax, MCTS, and potentially a neural network.
- **Development Tools**: Pytest.

### Notes

- This project aims to integrate different AI techniques step by step, focusing first on classical approaches and then
  moving towards machine learning-based solutions.
- The AI implementations will be added iteratively, ensuring that each approach is thoroughly tested and functional
  before moving to the next.

## How to Run

To run the game:

```bash
python main.py
