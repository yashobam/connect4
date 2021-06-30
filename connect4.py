import random
from os import system
import time
class Board:
    
    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.slots = [[' '] * self.width for row in range(self.height)]

    def __repr__(self):
        
        s = ''         
        for row in range(self.height):
            s += '|'   
            for col in range(self.width):
                s += self.slots[row][col] + '|'

            s += '\n'  
        for i in range(self.width):
            s+="--"
        s+="-"
        s+='\n'
        s+=" "
        for j in range(self.width):
            s+= str(j%10)+" "

        return s

    def add_checker(self, checker, col):
        
        assert(checker == 'X' or checker == 'O')
        assert(col >= 0 and col < self.width)
        
        for i in range(self.height):
            if self.slots[i][col]=="X" or self.slots[i][col]=="O":
                self.slots[i-1][col]=checker
                break
            elif self.height-1==i:
                self.slots[i][col]=checker
                break
    
    def add_checkers(self, colnums):
        checker = 'X'  
        for col_str in colnums:
            col = int(col_str)
            if 0 <= col < self.width:
                self.add_checker(checker, col)

            if checker == 'X':
                checker = 'O'
            else:
                checker = 'X'

    def reset(self):
        self.slots = [[' '] * self.width for row in range(self.height)]


    def can_add_to(self, col):
        if col<0 or col>=self.width:
            return False
        elif self.slots[0][col]=="X" or self.slots[0][col]=="O":
            return False
        else:
            return True


    def is_full(self):
        for i in range(self.width):
             if self.can_add_to(i)==True:

                return False
        return True


    def remove_checker(self,col):
        for i in range(self.height):
            if self.slots[i][col]=="X" or self.slots[i][col]=="O":
                self.slots[i][col]=" "
                break
            elif self.height-1==i:
                self.slots[i][col]=" "
                break


    def is_win_for(self,checker):
        x=0
        for i in range(self.height):
            for j in range(self.width):
                if self.slots[i][j]==checker:
                    
                    if self.leftdia(checker,i,j)>=4:
                        x=1
                    elif self.rightdia(checker,i,j)>=4:
                        x=1
                    elif self.horizontal(checker,i,j)>=4:
                        x=1
                    elif self.vertical(checker,i,j)>=4:
                        x=1
        if x==1:
            return True
        else:
            return False


    def leftdia(self,checker,r,c):
        if r-3<=-1 or c-3<=-1:
            return 0
        elif self.slots[r][c]==checker and self.slots[r-1][c-1]==checker and self.slots[r-2][c-2]==checker and self.slots[r-3][c-3]==checker:
            return 4
        else:
            return 0

    def rightdia(self,checker,r,c):
        if r-3<=-1 or c+3>=self.width:
            return 0
        elif self.slots[r][c]==checker and self.slots[r-1][c+1]==checker and self.slots[r-2][c+2]==checker and self.slots[r-3][c+3]==checker:
            return 4
        else:
            return 0


    def vertical(self,checker,r,c):
        if r-3<0:
            return 0
        elif self.slots[r][c]==checker and self.slots[r-1][c]==checker and self.slots[r-2][c]==checker and self.slots[r-3][c]==checker:
            return 4
        else:
            return 0


    def horizontal(self,checker,r,c):
        if c-3<0:
            return 0
        elif self.slots[r][c]==checker and self.slots[r][c-1]==checker and self.slots[r][c-2]==checker and self.slots[r][c-3]==checker:
            return 4
        else:
            return 0

class Player:
    def __init__(self,checker):
        self.checker=checker
        self.num_moves=0


    def __repr__(self):
        s="Player "+self.checker
        return s


    def opponent_checker(self):
        return "X" if self.checker=="O" else "O"


    def next_move(self,b):
        c=int(input("Enter column: "))
        print("\n")
        if (b.width<=c or c<0) and c!=999:
            print("Try again!")
            return self.next_move(b)
        elif c==999:
            print("You quit the game")
            select(3)
        else:
            self.num_moves+=1
            return c


def connect_four(p1, p2):
   
    if p1.checker not in 'XO' or p2.checker not in 'XO' \
       or p1.checker == p2.checker:
        print('need one X player and one O player.')
        return None

    print('Welcome to Connect Four!')
    print()
    b = Board(6, 7)
    print(b)
    
    while True:
        if process_move(p1, b) == True:
            return b

        if process_move(p2, b) == True:
            return b
def process_move(p,b):
    print(str(p)+"'s turn\n")
    c = p.next_move(b)
    if b.is_full()==True:
        print("It's a tie!")
        return True
    b.add_checker(p.checker,c)
    print(b)
    print("\n")
    if b.is_win_for(p.checker)==True:
        print(p," wins in ",p.num_moves," moves."+"\n"+"\n"+"\n"+"\n")
        return True
    
    else:
        return False

class RandomPlayer(Player):
    def next_move(self,b):
        c=random.randrange(0,b.width)
        if b.can_add_to(c)==False:
            return self.next_move(b)
        else:
            self.num_moves+=1
            return c
class AIPlayer(Player):
    def __init__(self,checker,tiebreak,lookahead):
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak=tiebreak
        self.lookahead=lookahead

    def __repr__(self):
        s=""
        s="Player "+self.checker
        return s
    def max_score_column(self,scores):
        maxscore=-1
        posmaxscore=0
        indices = [-1]*len(scores)
        c=0
        for i in range(len(scores)):
            if scores[i]>maxscore:
                maxscore=scores[i]
                for j in range(len(scores)):
                    indices[j]=-1
                for k in range(len(scores)):
                    if maxscore==scores[k]:
                        indices[k]=k
        for l in range(len(scores)):
            if l>-1:
                c+=1
            if indices[l]!=-1:
                posmaxscore=indices[l]
        if c>1:
            if self.tiebreak=='RIGHT':
                for m in range(len(scores)):
                    if indices[m]!=-1:
                        posmaxscore=m
                        
            elif self.tiebreak=='LEFT':
                for m in range(len(scores)):
                    if indices[m]!=-1:
                        posmaxscore=indices[m]
                        break
            else:
                posmaxscore=random.choice(indices)
                if posmaxscore==-1:
                    return self.max_score_column(scores)
        return posmaxscore

    def scores_for(self,b):
        scores=[50]*b.width
        for i in range(b.width):
            if b.can_add_to(i)==False:
                scores[i]=-1
            elif b.is_win_for(self.checker):
                scores[i]=100
            elif b.is_win_for(self.opponent_checker()):
                scores[i]=0
            elif self.lookahead==0:
                scores[i]=50
            else:
                b.add_checker(self.checker,i)
                Opponent=AIPlayer(self.opponent_checker(),self.tiebreak,self.lookahead-1)
                oppsc=Opponent.scores_for(b)
                
                if max(oppsc) == 0:
                    scores[i] = 100
                elif max(oppsc) == 100:
                    scores[i] = 0
                elif max(oppsc) == 50:
                    scores[i] = 50
                b.remove_checker(i)
        return scores
    def next_move(self,b):
        c=self.max_score_column(self.scores_for(b))
        self.num_moves+=1
        return c
def select(n):
    print("""\nType 1 for Player vs Player
Type 2 for Player vs AI
Type 3 for Player vs Random
Type 4 for AI vs AI
Type 5 for AI vs Random
Type 6 for Random vs Random
Type 7 to clear screen
Type 8 to change difficulty 1-5 (current difficulty: {})
WARNING: The higher the difficulty the more time the AI will take
You can also type 999 to exit any game\n""".format(n))
    ch=int(input("Enter your choice: "))
    print()
    if ch==1:
        connect_four(Player("X"),Player("O"))
        select(n)
    elif ch==2:
        connect_four(Player("X"),AIPlayer("O","RANDOM",n))
        select(n)
    elif ch==3:
        connect_four(Player("X"),RandomPlayer("O"))
        select(n)
    elif ch==4:
        connect_four(AIPlayer("X","RANDOM",n),AIPlayer("O","RANDOM",n))
        select(n)
    elif ch==5:
        connect_four(AIPlayer("X","RANDOM",n),RandomPlayer("O"))
        select(n)
    elif ch==6:
        connect_four(RandomPlayer("X"),RandomPlayer("O"))
        select(n)
    elif ch==7:
        system('cls')
        select(n)
    elif ch==8:
        c=int(input("\nEnter your difficulty: "))
        if c>0 and c<=5:
            select(c)
        else:
            print("\nDifficulty too high\n")
            select(3)
    elif ch!=999:
        print("\nThat choice doesn't exist\n")
        time.sleep(2)
        select(n)
def start():
    try:
        select(3)
    except RecursionError as re:
        print('\nSorry but the AI took too long. Restarting the game\n')
        select(3)
start()