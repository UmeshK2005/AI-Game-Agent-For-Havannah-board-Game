# AI Agent Overview

**Authors:** Umesh Kumar, Aditya Sahu  

Our AI agent relies on **three algorithms**. Each algorithm is associated with a score, and the combination of these scores is used to decide the final move.

---

## 1. Monte Carlo Tree Simulation (MCTS)

- Implemented in its **basic form** with simulations on random moves.  
- Advanced strategies like **RAVE** or **Last Good Reply** were tested but reduced performance because fewer iterations could be run.  
- **Move scoring:**  
  Each move is given a certain number of iterations by the MCTS. The score of a move is based on the number of iterations it receives. Since iterations can vary depending on the time remaining, MCTS scores are **normalized**, with the highest iterations given a score of 100.

---

## 2. Rand-Algorithm

- A **self-devised algorithm** to evaluate the quality of a move based on the current board state.  
- **Procedure:**  
  1. Consider a node and its neighbors and joints (virtual connections).  
  2. Each connected component is assigned a score.  
  3. The score of a move is the **sum of the scores of all connected components** in its neighbors and joints (without repetitions).  

- **Connected Component Scoring:** Based on four parameters:
  1. **Edge connection:** Number of edges connected to the component.  
  2. **Corner connection:** Number of corners connected to the component.  
  3. **Number of nodes:** Larger components increase the score.  
  4. **Vicinity to edge:** Components closer to edges tend to have higher scores.  

- Scores are calculated using a formula derived through **intuition and experimentation**.

---

## 3. Flower-Algorithm

- Another **self-devised algorithm** that gives preference to moves in certain formations.  
- There are **four formations** (not depicted in text).  
- If any formation is present, the weight of certain moves is **increased**.

---

## 4. Special Strategy

- A **hard-coded strategy** designed to gain an advantage over MCTS-based opponents.  
- Ensures a **sure victory** if its formation remains uninterrupted for 5 moves.  
- **Procedure:**  
  1. Join two corners first.  
  2. Form a **kite formation** in the next 3 moves.  
  3. Once the kite is formed, the algorithm fills joints based on priority, considering opponent moves.  

- This strategy gives a **good early advantage** and a strong position even if interrupted.

---

## 5. Overall Strategy of the Agent

1. **Opening moves:**  
   - First 2 moves are **hard-coded** to occupy corners.  
   - Next 3 moves form the kite (special strategy).  

2. **Runtime move selection:**  
   - Moves are decided based on the **weighted sum** of scores from the three algorithms.  
   - The move with the **maximum score** is chosen.  

3. **Weight adjustment over the game:**
   - **Moves 1–11:**  
     - MCTS has **low weight**.  
     - Rand-algorithm has **higher weight**, with joint selection emphasized.  
   - **Moves 12–18:**  
     - Weight of MCTS is increased.  
     - Rand and MCTS have almost **equal weights** around move 15.  
   - **Moves 19–24:**  
     - MCTS given **higher priority**.  
     - Rand weight is reduced as many connected components are formed.  
     - Flower given **moderate weight**.  
   - **Moves 25–30:**  
     - MCTS weight is **further increased** as it performs better in later stages.  
   - **Moves 30–end:**  
     - Agent relies **solely on MCTS**, with Flower and Rand as tie-breakers.  

- **Summary:** MCTS weight **increases gradually** as the game progresses, while Rand and Flower are used more in early/mid-game.

---

