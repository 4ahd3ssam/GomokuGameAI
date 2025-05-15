# Gomoku (Five in a Row) Game Solver



## 🧩 Overview
GomokuGameAI is a Python-based game solver for the classic Gomoku (Five in a Row) game. It supports:
- Human vs AI mode using the **Minimax algorithm**
- AI vs AI mode comparing **Minimax** and **Alpha-Beta Pruning**

---

## ✨ Features
- Customizable board size (default: 15x15)
- Turn-based interface for Human vs AI
- AI vs AI simulation with move-by-move display
- Console board visualization
- Optional GUI (Bonus)

---

## 🧠 AI Algorithms
### Minimax Algorithm
- Explores all possible game states up to a certain depth
- Evaluates and chooses optimal move

### Alpha-Beta Pruning
- Optimized version of Minimax
- Skips unnecessary branches
- Faster and more efficient decision-making

### Depth Limitation
- Controls the complexity and execution time of AI decisions

---

## 🎮 Game Rules
- Two players alternate turns
- The first player to get five consecutive marks (horizontally, vertically, or diagonally) wins
- Board is empty initially; players choose positions to place their marks

---

## 📥 Input
- Board size (optional)
- Mode selection:
  - `1` – Human vs AI
  - `2` – AI vs AI
- Initial moves (in Human mode)
- Current board state (optional advanced feature)

---

## 📤 Output
- AI’s chosen move in the form of coordinates (row, col)
- Updated game board printed after every move
- Winner announcement


