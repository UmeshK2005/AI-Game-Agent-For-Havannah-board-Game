import time
import math
import random
import numpy as np
import copy
import psutil
from helper import *
from collections import deque
from collections import Counter  

class Node:
    def __init__(self, state: np.array, wins: int, visits: int, player: int):
        self.state = state       # Current board state
        self.wins = wins         # Number of wins from this node
        self.visits = visits     # Number of simulations through this node
        self.player = player     # Player to move
        self.children = []       # Child nodes
        self.parent = None       # Parent node
        self.move = None         # Move that led to this node

class AIPlayer:
    def __init__(self, player_number: int, timer):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}: ai'.format(player_number)
        self.timer = timer
        self.C=1.4
        self.current_turn = 0 
        self.real_turn=0
        self.num_edges=1 
        self.num_corner=1 
        self.num_nodes=1 
        self.prox_edge=1 
        self.guarnteed_hit=False
        self.choose=0 
        self.corner=None 
        self.j=0
        self.opposite_rand = 0.8
        self.C1=0.0 
        self.C2=0.0
        self.C3=0.0 
        self.C4=0.0 
        self.first_run=False
        self.is_first_check=False  
        self.monte_time=7.0

    def victory(self, state):
        lst = get_valid_actions(state)
        for e in lst:
            x = state.copy()
            row, col = e
            x[row, col] = self.player_number
            if check_win(x, e, self.player_number)[0]:
                return e 
        return None 
    def loss1(self,state):
        lst = get_valid_actions(state)
        for e in lst:
            x = state.copy()
            row, col = e
            x[row, col] = 3 - self.player_number
            if check_win(x, e, 3 - self.player_number)[0]:
                return e 
    def loss(self, state):
        lst = get_valid_actions(state)
        for e in lst:
            x = state.copy()
            row, col = e
            x[row, col] = 3 - self.player_number
            if check_win(x, e, 3 - self.player_number)[0]:
                return e 
        for e in lst:
            x = state.copy()
            row, col = e
            x[row, col] = 3 - self.player_number
            lst1=get_valid_actions(x)
            move =None 
            for e1 in lst1:
                y=x.copy()
                row1,col1=e1
                y[row1,col1]=self.player_number
                lst2=get_valid_actions(y)
                b1=False 
                for e2 in lst2:
                    z = y.copy()
                    row2, col2 = e
                    z[row2, col2] = 3 - self.player_number
                    if check_win(z, e2, 3 - self.player_number)[0]:
                        move = e2 
                        b1=True 
                        break 
                if b1:
                    return move 
                        
                 
        return None 
 
    def check_prox(self,state,player,lst):
        visited = set(lst)  
        queue = deque([(node, 0) for node in lst])    
        while queue:
            current_node, depth = queue.popleft()
            if get_edge(current_node,len(state))!=-1:
                return depth 
            neigh=get_neighbours(len(state),current_node)
            for ne in neigh:
                if ne not in visited and state[ne]!=3-player:
                    visited.add(ne)
                    queue.append((ne,depth+1))
        return -1 
    def evaluation(self,state,move,player):
        vis=set()
        start_move =move 
        stk=[start_move]
        vis.add(start_move)
        while stk:
            m=stk.pop()
            lt=get_neighbours(len(state),m)
            for e in lt:
                if e not in vis and state[e]==player:
                    vis.add(e)
                    stk.append(e)
        lst=list(vis)
        num_edges=0
        num_corners=0
        set_edges=set()
        for e in lst:
            a=get_edge(e,len(state))
            if a!=-1:
                if a not in set_edges:
                    num_edges+=1 
                    set_edges.add(a)
            a=get_corner(e,len(state))
            if a!=-1:
                num_corners+=1 
        a=self.check_prox(state,player,lst)
        num_nodes=len(lst) 
        im_edges=0 
        im_corner=0
        im_nodes=0
        im_prox=0
        if num_edges==2:
            im_edges=30 
        if num_edges==1:
            im_edges=18 
        if num_edges==0:
            im_edges=7 
        im_nodes=2*num_nodes
        if num_corners==1:
            im_corner=20
        if a!=-1:
            im_prox=(40/(a+2))
        total = im_corner*self.num_corner+im_edges*self.num_edges+im_nodes*self.num_nodes+im_prox*self.prox_edge 
        return total
        pass 
     
    
    def neigh_and_joint(self,state,move,player,d1,eval_dic):
        i, j = move
        siz =len(state)//2
        l1=[]
        l2=[]
        dims=len(state)
        if j<siz :
            l1=[[(i,j-1),(1,1)],[(i+1,j+1),(1,1)],[(i-1,j),(1,1)]]
            l2=[[(i+1,j),(1,1)],[(i,j+1),(1,1)],[(i-1,j-1),(1,1)]]
        elif j>siz:
            l1=[[(i+1,j-1),(1,1)],[(i,j+1),(1,1)],[(i-1,j),(1,1)]]
            l2=[[(i+1,j),(1,1)],[(i-1,j+1),(1,1)],[(i,j-1),(1,1)]]
        else:
            l1=[[(i,j-1),(1,1)],[(i,j+1),(1,1)],[(i-1,j),(1,1)]]
            l2=[[(i+1,j),(1,1)],[(i-1,j+1),(1,1)],[(i-1,j-1),(1,1)]]
        lt=l1+l2
        a=l2[0][0]
        i,j=a 
        if j<siz :
            lt+=[[(i,j-1),(2,2)],[(i+1,j+1),(2,2)]]
        elif j>siz:
            lt+=[[(i+1,j-1),(2,2)],[(i,j+1),(2,2)]]
        else:
            lt+=[[(i,j-1),(2,2)],[(i,j+1),(2,2)]]
        a=l2[1][0]
        i,j=a 
        if j<siz :
            lt+=[[(i+1,j+1),(2,2)],[(i-1,j),(2,2)]]
        elif j>siz:
            lt+=[[(i,j+1),(2,2)],[(i-1,j),(2,2)]]
        else:
            lt+=[[(i,j+1),(2,2)],[(i-1,j),(2,2)]]
        a=l2[2][0]
        i,j=a 
        if j<siz :
            lt+=[[(i-1,j),(2,2)],[(i,j-1),(2,2)]]
        elif j>siz:
            lt+=[[(i-1,j),(2,2)],[(i+1,j-1),(2,2)]]
        else:
            lt+=[[(i-1,j),(2,2)],[(i,j-1),(2,2)]]
        lst=[]
      #  print(move,lt)
        for e in lt:
            a,b=e[0]
            if is_valid(a,b,dims) and state[e[0]]==player :
                lst.append(e)
       # print(move,lst)
        c=0
        s={}
        C=((self.real_turn-5)*(0.7)-(self.real_turn-25)*1.3)/20 #joint_constant
      #  print(C,self.real_turn)
        x=max(C,2-C)
        for e in lst :
            if e[1]==(1,1):
                node = d1[e[0]]
                if node not in s:
                    c+=(eval_dic[node]*(2-C))
                    s[node]="neigh"
            if e[1]==(2,2):
                
                node = d1[e[0]]
                if node not in s:
                    c+=(eval_dic[node]*C)
               #     print(e,c)
                    s[node]="joint"
                
        return c 
        
    def rand_algo(self,state):
        lst=get_valid_actions(state)
        d1={}
        dims=len(state)
        vis=set()
        comp=[]
        for i in range((len(state))):
            for j in range((len(state))):
             #   print(i,j,d1)
                if is_valid(i,j,dims) and state[i,j]==self.player_number and (i,j)not in vis:
                    d1[(i,j)]=(i,j)
                    comp.append((i,j))
                    stk=[(i,j)]
                    while stk:
                        row,col=stk.pop()
                        vis.add((row,col))
                        l=get_neighbours(dims,(row,col))
                        for e in l:
                            if e not in vis and state[e]==self.player_number:
                                d1[e]=d1[(row,col)]
                                stk.append(e)  
        eval_dic={}
        for node in comp:
            a=self.evaluation(state,node,self.player_number)
            eval_dic[node]=a 
        d2={}
        dims=len(state)
        vis=set()
        comp=[]
        for i in range((len(state))):
            for j in range((len(state))):
             #   print(i,j,d1)
                if is_valid(i,j,dims) and state[i,j]==3-self.player_number and (i,j)not in vis:
                    d2[(i,j)]=(i,j)
                    comp.append((i,j))
                    stk=[(i,j)]
                    while stk:
                        row,col=stk.pop()
                        vis.add((row,col))
                        l=get_neighbours(dims,(row,col))
                        for e in l:
                            if e not in vis and state[e]==3-self.player_number:
                                d2[e]=d2[(row,col)]
                                stk.append(e) 
        eval_dic2={}
        for node in comp:
            a=self.evaluation(state,node,3-self.player_number)
            eval_dic2[node]=a*self.opposite_rand 
      #  print(d1)
      #  print(eval_dic)
      #  print(d2)
      #  print(eval_dic2)
        lt=[]
        ans_dict={}
         
        for e in lst :
            t=self.neigh_and_joint(state,e,self.player_number,d1,eval_dic)
          #  print(e,t)
            t+=self.neigh_and_joint(state,e,3-self.player_number,d2,eval_dic2)
          #  print(e,t)
            ans_dict[e]=t
            continue
        return ans_dict
        pass 
        
    def special_attack(self,state):
       
        corner=self.corner 
       # print(self.choose,self.corner,self.j,self.current_turn)
        if self.current_turn<=5:
            lst=get_all_corners(len(state))
            mov1=None 
            mov2=None 
            for i in range(len(lst)):
                x=i 
                y=(i+1)%len(lst)
                if state[lst[x]]==self.player_number and state[lst[y]]==self.player_number:
                    mov1=lst[x]
                    mov2=lst[y]
            if self.current_turn==3:
                if mov1==(0,0):
                    if state[1,1]==0 and state[0,2]==0 and state[1,4]==0:
                        self.choose=1 
                        return (1,1)
                    if state[1,5]==0 and state[0,3]==0 and state[1,2]==0:
                        self.choose =2 
                        return (1,5)
                    return None
                if mov1==(0,5):
                    if state[1,5]==0 and state[0,7]==0 and state[1,8]==0:
                        self.choose =1
                        return (1,5)
                    if state[1,9]==0 and state[0,8]==0 and state[1,6]==0:
                        self.choose =2
                        return (1,9)
                    return None
                if mov1==(0,10):
                    if state[1,9]==0 and state[2,10]==0 and state[4,9]==0:
                        self.choose =1
                        return (1,9)
                    if state[5,9]==0 and state[3,10]==0 and state[2,9]==0:
                        self.choose =2
                        return (5,9)
                    return None
                if mov1==(5,10):
                    if state[5,9]==0 and state[7,8]==0 and state[8,6]==0:
                        self.choose =1
                        return (5,9)
                    if state[9,5]==0 and state[8,7]==0 and state[6,8]==0:
                        self.choose =2
                        return (9,5)
                    return None
                if mov1==(10,5):
                    if state[9,5]==0 and state[8,3]==0 and state[6,2]==0:
                        self.choose =1
                        return (9,5)
                    if state[5,1]==0 and state[7,2]==0 and state[8,4]==0:
                        self.choose =2
                        return (5,1)
                    return None
                if mov1==(5,0):
                    if state[5,1]==0 and state[3,0]==0 and state[2,1]==0:
                        self.choose =1
                        return (5,1)
                    if state[1,1]==0 and state[2,0]==0 and state[4,1]==0:
                        self.choose =2
                        return (1,1)
                    return None 
            if self.current_turn==4:
                if mov1==(0,0):
                    if state[1,1]==self.player_number:
                        if state[0,2]==3-self.player_number or state[1,4]==3-self.player_number:
                            return None 
                        return random.choice([(0,2),(1,4)])
                    if state[1,5]==self.player_number:
                        if state[0,3]==3-self.player_number or state[1,2]==3-self.player_number:
                            return None 
                        return random.choice([(0,3),(1,2)])
                    return None
                if mov1==(0,5):
                    if state[1,5]==self.player_number:
                        if state[0,7]==3-self.player_number or state[1,8]==3-self.player_number:
                            return None 
                        return random.choice([(0,7),(1,8)])
                    if state[1,9]==self.player_number:
                        if state[0,8]==3-self.player_number or state[1,6]==3-self.player_number:
                            return None 
                        return random.choice([(0,8),(1,6)])
                    return None
                if mov1==(0,10):
                    if state[1,9]==self.player_number:
                        if state[2,10]==3-self.player_number or state[4,9]==3-self.player_number:
                            return None 
                        return random.choice([(2,10),(4,9)])
                    if state[5,9]==self.player_number:
                        if state[3,10]==3-self.player_number or state[2,9]==3-self.player_number:
                            return None 
                        return random.choice([(3,10),(2,9)])
                    return None
                if mov1==(5,10):
                    if state[5,9]==self.player_number:
                        if state[7,8]==3-self.player_number or state[8,6]==3-self.player_number:
                            return None 
                        return random.choice([(7,8),(8,6)])
                    if state[9,5]==self.player_number:
                        if state[8,7]==3-self.player_number or state[6,8]==3-self.player_number:
                            return None 
                        return random.choice([(8,7),(6,8)])
                    return None
                if mov1==(10,5):
                    if state[9,5]==self.player_number:
                        if state[8,3]==3-self.player_number or state[6,2]==3-self.player_number:
                            return None 
                        return random.choice([(8,3),(6,2)])
                    if state[5,1]==self.player_number:
                        if state[7,2]==3-self.player_number or state[8,4]==3-self.player_number:
                            return None 
                        return random.choice([(7,2),(8,4)])
                    return None
                if mov1==(5,0):
                    if state[5,1]==self.player_number:
                        if state[3,0]==3-self.player_number or state[2,1]==3-self.player_number:
                            return None 
                        return random.choice([(3,0),(2,1)])
                    if state[1,1]==self.player_number:
                        if state[2,0]==3-self.player_number or state[4,1]==3-self.player_number:
                            return None 
                        return random.choice([(2,0),(4,1)])
                    return None
            if self.current_turn==5:
                if mov1==(0,0):
                    if state[1,1]==self.player_number:
                        if state[0,2]==self.player_number and state[1,4]==0:
                            self.guarnteed_hit=True 
                            self.corner=(0,0)
                            return (1,4)
                        if state[0,2]==0 and state[1,4]==self.player_number:
                            self.guarnteed_hit=True 
                            self.corner=(0,0)
                            return (0,2)
                        return None 
                    if state[1,5]==self.player_number:
                        if state[0,3]==self.player_number and state[1,2]==0:
                            self.corner=(0,0)
                            self.guarnteed_hit=True 
                            return (1,2)
                        if state[0,3]==0 and state[1,2]==self.player_number:
                            self.corner=(0,0)
                            self.guarnteed_hit=True 
                            return (0,3)
                    return None
                if mov1==(0,5):
                    if state[1,5]==self.player_number:
                        if state[0,7]==self.player_number and state[1,8]==0:
                            self.corner=(0,5)
                            self.guarnteed_hit=True 
                            return (1,8)
                        if state[0,7]==0 and state[1,8]==self.player_number:
                            self.corner=(0,5)
                            self.guarnteed_hit=True 
                            return (0,7)
                    if state[1,9]==self.player_number:
                        if state[0,8]==self.player_number and state[1,6]==0:
                            self.corner=(0,5)
                            self.guarnteed_hit=True 
                            return (1,6)
                        if state[0,8]==0 and state[1,6]==self.player_number:
                            self.corner=(0,5)
                            self.guarnteed_hit=True 
                            return (0,8)
                    return None
                if mov1==(0,10):
                    if state[1,9]==self.player_number:
                        if state[2,10]==self.player_number and state[4,9]==0:
                            self.corner=(0,10)
                            self.guarnteed_hit=True 
                            return (4,9)
                        if state[2,10]==0 and state[4,9]==self.player_number:
                            self.corner=(0,10)
                            self.guarnteed_hit=True 
                            return (2,10)
                    if state[5,9]==self.player_number:
                        if state[3,10]==self.player_number and state[2,9]==0:
                            self.corner=(0,10)
                            self.guarnteed_hit=True 
                            return (2,9)
                        if state[3,10]==0 and state[2,9]==self.player_number:
                            self.corner=(0,10)
                            return (3,10)
                    return None
                if mov1==(5,10):
                    if state[5,9]==self.player_number:
                        if state[7,8]==self.player_number and state[8,6]==0:
                            self.corner=(5,10)
                            self.guarnteed_hit=True 
                            return (8,6)
                        if state[7,8]==0 and state[8,6]==self.player_number:
                            self.corner=(5,10)
                            self.guarnteed_hit=True 
                            return (7,8)
                    if state[9,5]==self.player_number:
                        if state[8,7]==self.player_number and state[6,8]==0:
                            self.corner=(5,10)
                            self.guarnteed_hit=True 
                            return (6,8)
                        if state[8,7]==0 and state[6,8]==self.player_number:
                            self.corner=(5,10)
                            self.guarnteed_hit=True 
                            return (8,7)
                    return None
                if mov1==(10,5):
                    if state[9,5]==self.player_number:
                        if state[8,3]==self.player_number and state[6,2]==0:
                            self.corner=(10,5)
                            self.guarnteed_hit=True 
                            return (6,2)
                        if state[8,3]==0 and state[6,2]==self.player_number:
                            self.corner=(10,5)
                            self.guarnteed_hit=True 
                            return (8,3)
                    if state[5,1]==self.player_number:
                        if state[7,2]==self.player_number and state[8,4]==0:
                            self.corner=(10,5)
                            self.guarnteed_hit=True 
                            return (8,4)
                        if state[7,2]==0 and state[8,4]==self.player_number:
                            self.corner=(10,5)
                            self.guarnteed_hit=True 
                            return (7,2)
                    return None
                if mov1==(5,0):
                    if state[5,1]==self.player_number:
                        if state[3,0]==self.player_number and state[2,1]==0:
                            self.corner=(5,0)
                            self.guarnteed_hit=True 
                            return (2,1)
                        if state[3,0]==0 and state[2,1]==self.player_number:
                            self.corner=(5,0)
                            self.guarnteed_hit=True 
                            return (3,0)
                    if state[1,1]==self.player_number:
                        if state[2,0]==self.player_number and state[4,1]==0:
                            self.corner=(5,0)
                            self.guarnteed_hit=True 
                            return (4,1)
                        if state[2,0]==0 and state[4,1]==self.player_number:
                            self.corner=(5,0)
                            self.guarnteed_hit=True 
                            return (2,0)
                    return None
        else:
         #   print("hi")
            if self.guarnteed_hit:
            #    print(corner,self.choose,self.j)
                if corner==(0,0):
                    l1=[[(1,2),(0,1)],[(1,3),(0,3)],[(0,4),(1,5)]]
                    l2=[[(0,4),(1,4)],[(0,2),(1,3)],[(0,1),(1,1)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                if corner==(0,5):
                    l1=[[(0,6),(1,6)],[(1,7),(0,8)],[(1,9),(0,9)]]
                    l2=[[(1,8),(0,9)],[(1,7),(0,7)],[(1,5),(0,6)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False
                if corner==(0,10):
                    l1=[[(2,9),(1,10)],[(3,9),(3,10)],[(5,9),(4,10)]]
                    l2=[[(4,9),(4,10)],[(3,9),(2,10)],[(1,9),(1,10)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False
                if corner==(5,10):
                    l1=[[(6,8),(6,9)],[(7,7),(8,7)],[(9,5),(9,6)]]
                    l2=[[(8,6),(9,6)],[(7,7),(7,8)],[(5,9),(6,9)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False
                if corner==(10,5):
                    l1=[[(8,4),(9,4)],[(7,3),(7,2)],[(6,1),(5,1)]]
                    l2=[[(6,1),(6,2)],[(7,3),(8,3)],[(9,4),(9,5)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False
                if corner==(5,0):
                    l1=[[(4,0),(4,1)],[(2,0),(3,1)],[(1,0),(1,1)]]
                    l2=[[(1,0),(2,1)],[(3,1),(3,0)],[(4,0),(5,1)]]
                    if self.choose==1 :
                        for e in l1:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l1:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False 
                        
                    else:
                        for e in l2:
                            x,y=e 
                            if state[x]==3-self.player_number and state[y]==0:
                                return y 
                            if state[y]==3-self.player_number and state[x]==0:
                                return x 
                            if state[y]==3-self.player_number and state[x]==3-self.player_number:
                                self.guarnteed_hit=False 
                                return None 
                        for e in l2:
                            x,y=e
                            if state[x]==0 and state[y]==0:
                                return x 
                        self.guarnteed_hit=False
                
                        
                        
                      
        return None 
    def initials(self,state):
        if self.first_run==False:
            start=fetch_remaining_time(self.timer, self.player_number)
            a=self.victory(state)
            b=self.loss(state)
            end=fetch_remaining_time(self.timer, self.player_number)
            if start-end>=15.0:
                self.is_first_check=True 
            if len(state)==7:
                if start<=180.0:
                    self.monte_time=10.0 
                if start>180.0 and start<=360.0:    
                    self.monte_time=20.0 
            if len(state)==11:
                if self.is_first_check:
                    if start<=480.0:
                        self.monte_time=11.0 
                    if start>480.0 and start<=600.0:
                        self.monte_time=13.0 
                else:
                    if start<=480.0:
                        self.monte_time=7.0 
                    if start>480.0 and start<=600.0:
                        self.monte_time=9.0
            
            self.first_run=True 
        self.real_turn+=1 
        self.dim=(len(state)+1)//2
        if len(state)==7:
            if self.player_number==1 and self.real_turn>=3:
                a = self.victory(state)
                b = self.loss(state)
                if a is not None:
             #       print("hi",1)
                    return a 
                if b is not None:
             #       print("hi",2)
                    return b  
            if self.player_number==2 and self.real_turn>=2:
                a = self.victory(state)
                b = self.loss(state)
                if a is not None:
             #       print("hi",1)
                    return a 
                if b is not None:
             #       print("hi",2)
                    return b  
        if len(state)==11:
            if self.player_number==1 and self.real_turn>=5:
                if self.is_first_check:
                    a = self.victory(state)
                    b = self.loss1(state)
                    if a is not None:
                 #       print("hi",1)
                        return a 
                    if b is not None:
                 #       print("hi",2)
                        return b  
                else:
                    a = self.victory(state)
                    b = self.loss(state)
                    if a is not None:
                 #       print("hi",1)
                        return a 
                    if b is not None:
                 #       print("hi",2)
                        return b  
            if self.player_number==2 and self.real_turn>=4:
                if self.is_first_check:
                    a = self.victory(state)
                    b = self.loss1(state)
                    if a is not None:
                 #       print("hi",1)
                        return a 
                    if b is not None:
                 #       print("hi",2)
                        return b  
                else:
                    a = self.victory(state)
                    b = self.loss(state)
                    if a is not None:
                  #      print("hi",1)
                        return a 
                    if b is not None:
                   #     print("hi",2)
                        return b   
        self.current_turn+=1 
     #   print(self.current_turn)
        lst=get_all_corners(len(state))
        if self.player_number==1:
            if self.current_turn==1:
                lt=[]
                for e in lst:
                    if state[e]==0:
                        lt.append(e)
                return random.choice(lt)
            if self.current_turn==2:
                lt=[]
                for i in range(len(lst)):
                    x=i 
                    y=(i+1)%len(lst)
                    if state[lst[x]]==self.player_number and state[lst[y]]==0:
                        return lst[y]
                    if state[lst[y]]==self.player_number and state[lst[x]]==0:
                        return lst[x]
                    if state[lst[x]]==0:
                        lt.append(lst[x])
                if lt:
                    return random.choice(lt) 
        else:
            if self.current_turn==1:
                has_moved=False 
                move=None 
                for i in range(len(lst)) :
                    e=lst[i]
                    if state[e]==1:
                        move=i 
                        has_moved=True 
                        break 
                if has_moved:
                    return lst[((i+2)%6)]
                else:
                    return random.choice(lst)
            if self.current_turn==2:
                lt=[]
                for i in range(len(lst)):
                    x=i 
                    y=(i+1)%len(lst)
                    if state[lst[x]]==self.player_number and state[lst[y]]==0:
                        return lst[y]
                    if state[lst[y]]==self.player_number and state[lst[x]]==0:
                        return lst[x]
                    if state[lst[x]]==0:
                        lt.append(lst[x])
                if lt:
                    return random.choice(lt) 
    #    return None 
        if len(state)==11:
          #  return None 
            return self.special_attack(state)
        else:
            return None 
        
    def monte_carlo(self, state: np.array) :
        root = Node(state, 0, 0, 3 - self.player_number)  # Initialize the root node
        start_time = fetch_remaining_time(self.timer, self.player_number)
        i=0
        # Run the MCTS loop for a set time (e.g., 10 seconds)
        while (start_time - fetch_remaining_time(self.timer, self.player_number)) <= self.monte_time:
            i+=1 
            # Selection
            leaf = self.selection(root)
            if len(get_valid_actions(leaf.state, self.player_number)) > 0:
                leaf = self.expansion(leaf)

            # Simulation
            reward = self.simulation(leaf)

            # Backpropagation
            self.backpropagation(leaf, reward)
      #  print(i)
        # Choose the best move based on the most visited child
        best_move = self.best_move(root)
      #  print(best_move,"dsdvxsv")
        return best_move
      


    def selection(self, node: Node) -> Node:
        while node.children:
            node = self.select_child(node)  # Select child with highest UCB1 score
        return node

    def select_child(self, node: Node) -> Node:
        best_score = -float('inf')
        best_child = None
      #  C = math.sqrt(2)  # Exploration constant
        for child in node.children:
            if child.visits == 0:
                score = float('inf')  # Prioritize unexplored nodes
            else:
                exploitation = child.wins / child.visits
                exploration = self.C * math.sqrt(math.log(node.visits) / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_child = child
        return best_child
    

    def expansion(self, node: Node) -> Node:
        valid_moves = get_valid_actions(node.state, 3 - node.player)
     #   print(valid_moves)
        random.shuffle(valid_moves)  # Randomize move selection

        for move in valid_moves:
            new_state = node.state.copy()
            row, col = move
            new_state[row, col] = 3 - node.player  # Make the move for the opponent

            # Create a new child node with the updated move
            child_node = Node(new_state, 0, 0, 3 - node.player)
            child_node.move = move  # Update move in the child node
            child_node.parent = node
            node.children.append(child_node)

        return node.children[0]  # Return one of the newly expanded nodes

    def simulation(self, node: Node) -> int:
        temp_state = node.state.copy()
        current_player = node.player
        last_move = node.move  # Initialize last move with node's move

        while not self.is_terminal(temp_state, last_move):
            valid_moves = get_valid_actions(temp_state, current_player)
            
            if not valid_moves:
                return 0  # Draw if no valid moves
            best_move = random.choice(valid_moves)

            # Apply the selected move
            row, col = best_move
            temp_state[row, col] = current_player
            last_move = best_move  # Update last move

            # Switch player
            current_player = 3 - current_player

        # Determine winner
        winner = 3-current_player
        if winner == self.player_number:
            return 1  # AI player wins
        elif winner == 3 - self.player_number:
            return -1  # Opponent wins
        return 0  # Draw

    def backpropagation(self, node: Node, reward: int):
        while node is not None:
            node.visits += 1
            if node.player == self.player_number:
                node.wins += reward  # Positive reward for AI
            else:
                node.wins -= reward  # Negative reward for opponent
            node = node.parent

    def is_terminal(self, state: np.array, move: Tuple[int, int]) -> bool:
        return check_win(state, move, self.player_number)[0]

    def best_move(self, root: Node) :
        max_visits = -1
        best_move = None
        lst=[]
        for child in root.children:
            lst.append((child.visits,child.move))
         #   print(child.visits,child.move)
            if child.visits > max_visits:
                max_visits = child.visits
                best_move = child.move
        lst.sort()
        lst.reverse()
     #   print(lst,"jjhjhj")
        return lst
       
    def flower_condition1(self,state,d,player):
        lst=get_valid_actions(state,player)
        for e in lst :
            lt=get_neighbours(len(state),e)
            if len(lt)<4:
                continue 
            i, j = e 
            siz =len(state)//2
            l1=[]
            l2=[]
            dims=len(state)
            if j<siz :
                l1=[(i,j-1),(i+1,j+1),(i-1,j)]
                l2=[(i+1,j),(i,j+1),(i-1,j-1)]
            elif j>siz:
                l1=[(i+1,j-1),(i,j+1),(i-1,j)]
                l2=[(i+1,j),(i-1,j+1),(i,j-1)]
            else:
                l1=[(i,j-1),(i,j+1),(i-1,j)]
                l2=[(i+1,j),(i-1,j+1),(i-1,j-1)]
            lt=[l1[0],l2[0],l1[1],l2[1],l1[2],l2[2]]
            l1=[]
            for (x,y) in lt:
                if is_valid(x,y,dims):
                    l1.append((x,y))
            lt=l1 
            for i in range(len(lt)):
                if state[lt[i]]==player and state[lt[(i+1)%len(lt)]]==player and state[lt[(i+2)%len(lt)]]==player and state[lt[(i+3)%len(lt)]]==player:
                    d[e]=-10**5 
                    break        
    def flower_condition2(self,state,d,player):
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i,j]==player:
                    lt=get_neighbours(len(state),(i,j))
                    l1=[]
                    for e in lt:
                        if state[e]!=3:
                            l1.append(e)
                    lt=l1
                #    print(lt,(i,j))
                    if len(lt)<=4:
                        continue 
                    if is_valid(i,j,len(state)) and state[i,j]==player:
                        siz =len(state)//2
                        l1=[]
                        l2=[]
                        dims=len(state)
                        if j<siz :
                            l1=[(i,j-1),(i+1,j+1),(i-1,j)]
                            l2=[(i+1,j),(i,j+1),(i-1,j-1)]
                        elif j>siz:
                            l1=[(i+1,j-1),(i,j+1),(i-1,j)]
                            l2=[(i+1,j),(i-1,j+1),(i,j-1)]
                        else:
                            l1=[(i,j-1),(i,j+1),(i-1,j)]
                            l2=[(i+1,j),(i-1,j+1),(i-1,j-1)]
                        lt=[l1[0],l2[0],l1[1],l2[1],l1[2],l2[2]]
                        c=0
                      #  print((i,j))
                        for e in lt:
                            if state[e]==player:
                                c+=1 
                        if c==1:
                            if state[lt[0]]==player:
                                for e in [l1[1],l2[1],l1[2]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            if state[lt[1]]==player:
                                for e in [l2[1],l1[2],l2[2]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            if state[lt[2]]==player:
                                for e in [l1[2],l2[2],l1[0]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            if state[lt[3]]==player:
                                for e in [l2[2],l1[0],l2[0]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            if state[lt[4]]==player:
                                for e in [l1[0],l2[0],l1[1]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            if state[lt[5]]==player:
                                for e in [l2[0],l1[1],l2[1]]:
                                    x,y=e 
                                    if is_valid(x,y,dims) and state[e]==0:
                                        d[e]+=20 
                            
    def flower_condition3(self,state,d,player):
        for i in range(len(state)):
            for j in range(len(state)):
                lt=get_neighbours(len(state),(i,j))
                l1=[]
                for e in lt:
                    if state[e]!=3:
                        l1.append(e)
                lt=l1
             #   print(lt,(i,j))
                if len(lt)<=4:
                    continue 
                if is_valid(i,j,len(state)) and state[i,j]!=3-player:
                    siz =len(state)//2
                    l1=[]
                    l2=[]
                    dims=len(state)
                    if j<siz :
                        l1=[(i,j-1),(i+1,j+1),(i-1,j)]
                        l2=[(i+1,j),(i,j+1),(i-1,j-1)]
                    elif j>siz:
                        l1=[(i+1,j-1),(i,j+1),(i-1,j)]
                        l2=[(i+1,j),(i-1,j+1),(i,j-1)]
                    else:
                        l1=[(i,j-1),(i,j+1),(i-1,j)]
                        l2=[(i+1,j),(i-1,j+1),(i-1,j-1)]
                    lt=[l1[0],l2[0],l1[1],l2[1],l1[2],l2[2]]
                    c=0
                  #  print((i,j))
                  #  print(lt)
                    for e in lt:
                        if state[e]==player:
                            c+=1 
                    if c==2:
                        for k in range(6):
                            x1,y1=lt[k]
                            x2,y2=lt[(k+2)%6]
                            if state[x1,y1]==player and state[x2,y2]==player:
                                x3,y3=lt[(k+4)%6]
                                if state[x3,y3]==0:
                                    d[(x3,y3)]+=30 
                                    break 
    def flower_condition4(self,state,d,player):
        for i in range(len(state)):
            for j in range(len(state)):
                lt=get_neighbours(len(state),(i,j))
                l1=[]
                for e in lt:
                    if state[e]!=3:
                        l1.append(e)
                lt=l1
                if len(lt)<=4:
                    continue 
                if is_valid(i,j,len(state)) and state[i,j]!=3-player:
                    siz =len(state)//2
                    l1=[]
                    l2=[]
                    dims=len(state)
                    if j<siz :
                        l1=[(i,j-1),(i+1,j+1),(i-1,j)]
                        l2=[(i+1,j),(i,j+1),(i-1,j-1)]
                    elif j>siz:
                        l1=[(i+1,j-1),(i,j+1),(i-1,j)]
                        l2=[(i+1,j),(i-1,j+1),(i,j-1)]
                    else:
                        l1=[(i,j-1),(i,j+1),(i-1,j)]
                        l2=[(i+1,j),(i-1,j+1),(i-1,j-1)]
                    lt=[l1[0],l2[0],l1[1],l2[1],l1[2],l2[2]]
                    c=0
                    for e in lt:
                        if state[e]==player:
                            c+=1 
                    if c==2:
                        for k in range(6):
                            x1,y1=lt[k]
                            x2,y2=lt[(k+1)%6]
                            if state[x1,y1]==player and state[x2,y2]==player and k==0:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3-1,y3)
                                    
                                elif j>siz:
                                    x4,y4=(x3-1,y3)
                                    
                                else:
                                    x4,y4=(x3-1,y3)
                                    break
                                if is_valid(x4,y4,dims) and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                            if state[x1,y1]==player and state[x2,y2]==player and k==1:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3-1,y3-1)
                                    
                                elif j>siz:
                                    x4,y4=(x3,y3-1)
                                    
                                else:
                                    x4,y4=(x3-1,y3-1)
                                    break
                                if is_valid(x4,y4,dims)and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                            if state[x1,y1]==player and state[x2,y2]==player and k==2:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3,y3-1)
                                    
                                elif j>siz:
                                    x4,y4=(x3+1,y3-1)
                                    
                                else:
                                    x4,y4=(x3,y3-1)
                                    break
                                if is_valid(x4,y4,dims)and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                            if state[x1,y1]==player and state[x2,y2]==player and k==3:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3+1,y3)
                                    
                                elif j>siz:
                                    x4,y4=(x3+1,j)
                                    
                                else:
                                    x4,y4=(x3+1,y3)
                                    break
                                if is_valid(x4,y4,dims)and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                            if state[x1,y1]==player and state[x2,y2]==player and k==4:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3+1,y3+1)
                                    
                                elif j>siz:
                                    x4,y4=(x3,y3+1)
                                    
                                else:
                                    x4,y4=(x3,y3+1)
                                    break
                                if is_valid(x4,y4,dims)and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                            if state[x1,y1]==player and state[x2,y2]==player and k==5:
                                x3,y3=lt[(k+3)%6]
                                x4,y4=(-1,-1)
                                if j<siz :
                                    x4,y4=(x3,y3+1)
                                    
                                elif j>siz:
                                    x4,y4=(x3-1,y3+1)
                                    
                                else:
                                    x4,y4=(x3-1,y3+1)
                                    break
                                if is_valid(x4,y4,dims)and state[x4,y4]==0 and state[i,j]==player:
                                    d[(x4,y4)]+=35 
                                                                
    def flower(self,state):
        d=Counter()
        self.flower_condition1(state,d,self.player_number)
      #  print(d)
     #   for e in d:
     #       print(e,d[e],"1")
        self.flower_condition2(state,d,self.player_number)
     #   for e in d:
     #       print(e,d[e],"2")
        self.flower_condition3(state,d,self.player_number)
     #   for e in d:
      #      print(e,d[e],"3")
        self.flower_condition4(state,d,self.player_number)
        self.flower_condition1(state,d,3-self.player_number)
      #  print(d)
     #   for e in d:
     #       print(e,d[e],"1")
        self.flower_condition2(state,d,3-self.player_number)
     #   for e in d:
     #       print(e,d[e],"2")
        self.flower_condition3(state,d,3-self.player_number)
     #   for e in d:
      #      print(e,d[e],"3")
        self.flower_condition4(state,d,3-self.player_number)
        
        ans=[]
        for e in d:
            ans.append((e,d[e]))
      #  print(ans)
        return d 
        pass 
    
    def manga(self,state):
        lst=get_valid_actions(state,self.player_number)
        d={}
        for e in lst :
            if get_edge(e,len(state))!=-1:
                d[e]=23
                continue 
            if get_corner(e,len(state))!=-1:
                d[e]=30
                continue 
            d[e]=0
        return d 
    
    def combiner(self,state):
        a=self.initials(state)
        if a!=None:
    #        print(a,"this move")
            return a
        monte_list=self.monte_carlo(state)
        
     #   print(monte_list,len(monte_list))
        ans_rand=self.rand_algo(state)
        ans_flower=self.flower(state)
        ans_manga=self.manga(state)
      #  print(ans_rand)
        rand_flower_manga_d={}
        lst=get_valid_actions(state,self.player_number)
        for e in lst:
            rand_flower_manga_d[e]=(0,0,0)
        for e in ans_rand:
            x,y,z=rand_flower_manga_d[e]
            rand_flower_manga_d[e]=(ans_rand[e],y,z)
         #   print(e,rand_flower_manga_d[e])
        for e in ans_flower:
            x,y,z=rand_flower_manga_d[e]
            rand_flower_manga_d[e]=(x,ans_flower[e],z)
        for e in ans_manga:
            x,y,z=rand_flower_manga_d[e]
            rand_flower_manga_d[e]=(x,y,ans_manga[e])
        
        for e in rand_flower_manga_d:
            if rand_flower_manga_d[e]==(0,0,0):
                continue 
            x,y=e
        x=monte_list[0][0]
        monte_d={}
        for e in monte_list:
            monte_d[e[1]]=(100*e[0])/x 
     #       print(e)
        final_d={}
        n=self.real_turn
        if n<=11:
            if len(state)==7:
                self.C1=1.0 
                self.C2=0.5 
                self.C3=1.0 
                self.C4=((0.5*(n-11))/(-10))+((1.8*(n-1))/10)
            else:
                self.C1=1.0 
                self.C2=0.5 
                self.C3=1.0 
                self.C4=((n-1)*0.8)/10 # it was 0.8
        if n>=12 and n<=18:
            if len(state)==7:
                self.C1=((1.3*(n-18))/(-6))+((0.7*(n-12))/6) 
                self.C2=0.25 
                self.C3=0.8 
                self.C4=2.0-self.C1 
            else:
                self.C1=((1.3*(n-18))/(-6))+((0.7*(n-12))/6) 
                self.C2=0.25 
                self.C3=0.8 
                self.C4=2.0-self.C1
        if n>=19 and n<=24:
            self.C1=((0.7*(n-24))/(-5))+((0.4*(n-19))/5)  
            self.C2=0.0   
            self.C3=0.8 
            self.C4=((1.6*(n-24))/(-5))+((2.5*(n-19))/5)
        if n>=25 and n<=30:
            self.C1=0.3 
            self.C2=0.0   
            self.C3=0.6  
            self.C4=((2.5*(n-30))/(-5))+((3.5*(n-25))/5)
        if n>=31:
            self.C1=0.2 
            self.C2=0.0   
            self.C3=0.3  
            self.C4=((3.5*(n-46))/(-15))+((6.0*(n-31))/15)
        for e in lst :
            m1=rand_flower_manga_d[e][0]
            m2=rand_flower_manga_d[e][2]
            m3=rand_flower_manga_d[e][1]
            m4=monte_d[e] 
            final_d[e]=m1*self.C1+m2*self.C2 +m3*self.C3 +m4*self.C4 
                    
        lt=[]
        for e in final_d:
            
            lt.append([final_d[e],e])
        lt.sort()
        lt.reverse()
        for e in lt:
            x,y=e[1]
       #     print(x,y,e[0])
        
            
        return lt[0][1]
        
    def get_move(self, state: np.array) -> Tuple[int, int]:
        return self.combiner(state)
