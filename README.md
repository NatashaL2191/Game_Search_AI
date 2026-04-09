The goal is to compare deterministic and stochastic approaches to game playing AI in terms on correctness, efficency and performance. The project implements two adversarial search algorithms for playing Tic-Tac-Toe
  - Minimax with Alpha-Beta Pruning
  - Monte Carlo Tree Search (MCTS)

File explenation
  - game.py - Main game engine
  - tic_tac_toe.py - Initial game logic
  - minimax_agent.py - Minimax algorithm
  - mcts_agent.py - MCTS algorithm
  - tournament.py - Runs matches between agents
  - tests/ - Test Cases and results
  - AI-Mini3.pptx - Presentaion
  - Mini Project 3 Report.docx - Report

How to run tournament 
  - python tournament.py
How to run MCTS tests
  - python -m tests.test_mcts

Notes
- Minimax = perfect play
- Alpha-beta = faster
- MCTS = better with more iterations
