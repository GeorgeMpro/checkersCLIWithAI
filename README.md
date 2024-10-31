# Checkers CLI with AI

**Status:** Work in Progress 🚧

## Overview

This project is a command-line implementation of the classical Checkers game. Supports two-player interaction.

This project is being developed with a TDD-first approach and guided by SOLID principles to reinforce skills in clean,
modular, and maintainable code.

## Current State of the Game

- **Interactive CLI**: Fully functional game in player vs. player mode.<br>
  Players can view the board, receive prompts for available moves, and input commands to play the
  game.
- **Core Game Mechanics**: Implements classic Checkers rules, including capturing moves, chain captures, and king
  promotions.
- **Endgame Detection**: Automatically recognizes win conditions (no more moves, no more pieces).

## Future Improvements

- **AI Integration**:
    - **Minimax Integration**: A Minimax-based AI opponent for P vs. AI, and AI vs. AI gameplay.
    - **Alpha Beta Pruning**:  Optimize Minimax for smarter, faster gameplay.
    - **Opening Book and Iterative Deepening** (Optional): Add preset opening moves and iterative deepening for endgame strategy.

- **Driver and Analysis**:
    - **Driver Experimentation**: Run AI vs. AI simulations to test different heuristic performance.
    - **Data Analysis**:
        - Use Pandas to aggregate data and Matplotlib to visualize win rates, game lengths, and heuristic effectiveness.
        - Summarize insights and refine configurations based on findings.

- **Heuristic Optimization**:
    - **Enhanced Heuristics**: Refine heuristics through driver simulations to identify optimal configurations.
    - **Cell-Based Scoring** (Optional):  Integrate positional scoring (e.g. central control, protected cells) and adjust based on results.

- **Game Enhancements** (Optional):
    - **Redo Moves**: Add redo functionality for user experience and testing.
    - **Player Configurations**: Allow users to customize AI settings (heuristic, lookahead depth, AI vs. AI).

## Installation and Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/GeorgeMpro/checkersCLIWithAI

2. Navigate to the project folder and run the game:
    ```bash
   python3 main.py

## Running Tests

    python3 -m pytest

The tests cover:

- Board and piece functionality (`test_board.py`)
- Game state and win conditions (`test_game_state.py`)
- Move generation and validations (`test_game_play.py`)
- User prompt and input handling (`test_user_interaction.py`)