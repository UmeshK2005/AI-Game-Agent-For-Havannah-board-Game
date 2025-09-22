Umesh Kumar(2022CS11115)
Aditya Sahu(2022CS11113)
Our AI agent relies on 3 algorithm. Each algorithm is associated with a score and the combination of those scores are used to decide the 
final move.
1) Monte carlo tree simulation: This is done in its most basic form. The simulation are done on random moves. The idea of using MCTS with 
ideas like RAVE or Last Good reply strategy was also coded and tested but, it led to reduction in perforance because MCTS could run lesser 
number of iterations. 
Each move is given some iterations by the MCTS. So thw MCTS score of each move is determined on the basis of the number of iterations given
some move. Since the number of iterations can very depending on the time remaining, we have normailzed the scores of MCTS like the one with
the highest iterations is given a score of 100.
2) Rand-algorithm: This is a self devised algorithm used for determining how good a move will be based on the current state of the board.
Suppose we have a node, consider its neighbours and joints(virtual connections).Now in this algorithm each connected component is associated
with a score. The score of the node(move) is equal to the sum of scores of all the connected components present in its neighbours and joints
(without repititions). Now the scoring of a conneted component is done on 4 parameters.
    a) Edge connection: The number of edges to which the connected component is connected.
    b) Corner connection: The number of corners the connected component is connected with.
    c) Number of nodes: The number of nodes the connected component has inceases the score.
    d) Vicinity to edge: If a connected component is closer to the edge it is likely to have a greater score.
Using a formula(self devised through intuition and experiment). we calculate the score of a connected component and hence the score of a move.
3) Flower-algorithm: It is also a self-devised algorithm used for giving preferences to certain moves in the vicinity. To incorporate its 
impact it is also associated with some score. It consists of 4 formations(can't be depicted in text file), if any of those formations is 
in the current state then the weight of certain move is increased.
4) Special-strategy: To gain advantage over the participants using MCTS as their primary tool we have used a special strategy that is hard coded.
The strategy gives a sure victory if its formation is uninterrupted for 5 moves. This not only gives a very good chance of early victory but
also if it is interrupted leads to a good position of out agent in the board.
The strategy consists of joining 2 corners first. Then there is a kite formation in the subsequent 3 moves. Note that it is not possible for
opponent to win in these 5 moves however he can block our formation. Once the kite formation is formed it starts filling the joints in some
priority order determined by the fact that the other neighbour-joint is filled by opponent or not.

Overall strategy of agent:
The first 2 moves are hard coded to occupy the corners.
The next 3 moves are used for the formation of kite(special strategy). If the formation is uninterrupted then the algorithm completes the formation
leading to victory. If interrupted it switches to next part.
In the main runtime of the agent the moves are decided on the basis of score determined by the 3 algorithms. The weighted sum of these 3 algorithm
scores are calculated. The one move with the maximum score is chosen. Now the weights of different algorithms is also varied acording to moves.
For moves 1-11: MCTS is given very less weight and Rand-algorithm is given more weight. Also within Rand algorithm the selection of joints
is given more weight in intial stages to get the agent to a good position.
For the moves 12-18: The weight of MCTS is increased and Rand and MCTS almost have equal weights around 15 moves.
For moves 19-24: The weight of MCTS score is given even more priority and the weight of Rand is reduced since by this time many connected
components would have been formed so all moves will have a high score wrt to that. Flower is also given moderate weight.
For moves 25-30: The weight of MCTS is increased even more. It is noticed that MCTS given good results at the later stages of the game as 
it is able to run more iterations. So the algorithm tends to rely more on MCTS.
For moves 30- end: The algorithm also solely relies on MCTS with Flower and Rand being a tie breaker strategy. The weigthts vary over the
duration of the game. Like it is the weight of MCTS increases as the game approaches the end.
