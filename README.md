# Checkers CLI with AI

**Status:** Work in Progress 🚧

## Overview

This project is a command-line implementation of the classical Checkers game. supports two-player interaction

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

- **AI Integration**: Implementing a Minimax-based AI opponent will be added, allowing players to compete against the
  computer.
- **AI Enhancement**: Implementing Minimax with Alpha-Beta pruning for a smarter opponent, and a faster gameplay experience.
- **General**: Adding redo functionality.

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