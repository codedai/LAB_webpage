import numpy
import time
import random

WHITE = -1
BLACK = +1
EMPTY = 0
PASS_MOVE = None

class GO(object):
    def __init__(self,size = 19,komi = 4.5):
        self.size = size
        self.komi = komi
        self.board = numpy.zeros((size,size))
        self.board.fill(EMPTY)
        self.turns = 0
        self.current_player = BLACK
        self.passes_black = 0
        self.passes_white = 0
        self.ko = None
        self.history = []
        self.is_end = False
        self.liberty_sets = [[set() for _ in range(size)] for _ in range(size)]
        for x in range(size):
            for y in range(size):
                self.liberty_sets[x][y] = set(self._neighbors((x,y)))
        self.liberty_count = numpy.zeros((size,size),dtype = numpy.int)
        self.liberty_count.fill(-1)
        self.group_sets = [[set() for _ in range(size)] for _ in range(size)]
    def get_group(self,position):
        (x, y) = position
        return self.group_sets[x][y]
    def get_group_around(self, postion):
        group = []
        for (x, y) in self._neighbors(position):
            if self.board[x][y] != EMPTY:
                group = self.group_sets[x][y]
                gourp_member = next(iter(group))
                if not any(group_member in g for g in groups):
                    group.append(group)
        return groups
    def _on_board(self, position):
        (x, y) = position
        return 0 <= x and x < self.size and 0 <= y and y < self.size
    def _diagonals(self, position):
        (x, y) = position
        return filter(self._on_board, [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)])
    def _neighbors(self, position):
        (x, y) = position
        return filter(self._on_board, [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
    def _update_neighbors(self, position):
        (x, y) = position
        temp_group = set()
        temp_group.add(position)
        temp_libs = self.liberty_sets[x][y]
        for (nx, ny) in self._neighbors(position):
            self.liberty_sets[nx][ny] -= set([position])
            if self.board[nx][ny] == -self.current_player:
                new_liberty_count = len(self.liberty_sets[nx][ny])
                for (gx, gy) in self.group_sets[nx][ny]:
                    self.liberty_count[gx][gy] = new_liberty_count
            elif self.board[x][y] == self.board[nx][ny]:
                temp_group |= self.group_sets[nx][ny]
                temp_libs |= self.liberty_sets[nx][ny]
        count_temp_libs = len(temp_libs)
        for (gx, gy) in temp_group:
            self.group_sets[gx][gy] = temp_group
            self.liberty_sets[gx][gy] = temp_libs
            self.liberty_count[gx][gy] = count_temp_libs
    def _remove_group(self,group):
        for (x, y) in group:
            self.board[x, y] = EMPTY
        for (x, y) in group:
            self.group_sets[x][y] = set()
            self.liberty_sets[x][y] = set()
            self.liberty_count[x][y] = -1
            for (nx, ny) in self._neighbors((x, y)):
                if self.board[nx, ny] == EMPTY:
                    self.liberty_sets[x][y].add((nx, ny))
                else:
                    self.liberty_sets[nx][ny].add((x, y))
                    for (gx, gy) in self.group_sets[nx][ny]:
                        self.liberty_count[gx][gy] = len(self.liberty_sets[nx][ny])
    def is_suicide(self, action):
        (x, y) = action
        num_liberties_here = len(self.liberty_sets[x][y])
        if num_liberties_here == 0:
            for (nx, ny) in self._neighbors(action):
                is_friendly_group = self.board[nx, ny] == self.current_player
                is_enemy_group = self.board[nx, ny] == -self.current_player
                group_has_other_liberties = len(self.liberty_sets[nx][ny] - set([action])) > 0
                if is_friendly_group and group_has_other_liberties:
                    return False
                if is_enemy_group and not group_has_other_liberties:
                    return False
            return True
        return False
    def is_legal(self, action):
        if action is PASS_MOVE:
            return True
        (x, y) = action
        empty = self.board[x][y] == EMPTY
        suicide = self.is_suicide(action)
        ko = action == self.ko
        return self._on_board(action) and not suicide and not ko and empty
    def do_move(self, action, color = EMPTY):
        color = color or self.current_player
        reset_player = self.current_player
        if self.is_legal(action):
            self.ko = None
            if action is not PASS_MOVE:
                (x, y) = action
                self.board[x][y] = color
                self._update_neighbors(action)
                for (nx, ny) in self._neighbors(action):
                    if self.board[nx, ny] == -color and len(self.liberty_sets[nx][ny]) == 0:
                        captured_group = self.group_sets[nx][ny]
                        num_captured = len(captured_group)
                        self._remove_group(captured_group)
                        if num_captured == 1:
                            would_recapture = len(self.liberty_sets[x][y]) == 1
                            recapture_size_is_1 = len(self.group_sets[x][y]) == 1
                            if would_recapture and recapture_size_is_1:
                                self.ko = (nx, ny)
            else:
                if color == BLACK:
                    self.passes_black += 1
                if color == WHITE:
                    self.passes_white += 1
            self.current_player = -color
            self.turns += 1
            self.history.append(action)
        else:
            self.current_player = reset_player
        if len(self.history) > 1:
            if self.history[-1] is PASS_MOVE and self.history[-2] is PASS_MOVE and self.current_player == WHITE:
                self.is_end = True
        return self.is_end
    def get_legal_moves(self, include_eyes=True):
        moves = [None]
	for x in range(self.size):
            for y in range(self.size):
                if self.is_legal((x, y)) and (include_eyes or not self.is_eye((x, y), self.current_player)):
                    moves.append((x, y))
        return moves
    def is_eye(self, position, owner, stack=[]):
        if not self.is_eyeish(position, owner):
            return False
        num_bad_diagonal = 0
        allowable_bad_diagonal = 1 if len(self._neighbors(position)) == 4 else 0
        for d in self._diagonals(position):
            if self.board[d] == -owner:
                num_bad_diagonal += 1
            elif self.board[d] == EMPTY and d not in stack:
                stack.append(position)
                if not self.is_eye(d, owner, stack):
                    num_bad_diagonal += 1
                stack.pop()
            if num_bad_diagonal > allowable_bad_diagonal:
                return False
	return True

    def is_eyeish(self, position, owner):
        (x, y) = position
        if self.board[x, y] != EMPTY:
            return False
        for (nx, ny) in self._neighbors(position):
            if self.board[nx, ny] != owner:
                return False
	return True
    def get_winner(self):
        score_white = numpy.sum(self.board == WHITE)
        score_black = numpy.sum(self.board == BLACK)
        empties = zip(*numpy.where(self.board == EMPTY))
        for empty in empties:
            if self.is_eyeish(empty, BLACK):
                score_black += 1
            elif self.is_eyeish(empty, WHITE):
                score_white += 1
        score_white += self.komi
        if score_black > score_white:
            winner = BLACK
        elif score_white > score_black:
            winner = WHITE
        else:
            winner = EMPTY
        return winner
    def copy(self):
        other = GO(self.size)
        other.board = self.board.copy()
        other.turns = self.turns
        other.current_player = self.current_player
        other.ko = self.ko
        other.history = self.history
        #other.num_black_prisoners = self.num_black_prisoners
        #other.num_white_prisoners = self.num_white_prisoners
    	for x in range(self.size):
	    for y in range(self.size):
		other.group_sets[x][y] = set(self.group_sets[x][y])
		other.liberty_sets[x][y] = set(self.liberty_sets[x][y])
	other.liberty_count = self.liberty_count.copy()
	return other

class Node(object):
    def __init__(self,state,father):
        self.father = father
        self.sons = []
        self.used_moves = []
        self.state = state
        self.visited = 0
        self.win = 0
    def get_sons(self):
        return self.sons
    def is_expanded(self):
        num_sons = len(self.used_moves)
        num_actions = len(self.state.get_legal_moves())
        if (num_sons == num_actions):
            return False
        return True
class MCTS(object):
    def __init__(self,root):
        self.root =  root
        self.depth = 0
    def Search(self,start,ti):
        start_time = time.clock()
        while time.clock() - start_time <= ti:
            next_Node = self.Tree_policy(start)
            result = self.Default_policy(next_Node)
            self.Backpropagation(result,next_Node)
            print time.clock() - start_time
        return self.best_son(start,0)
    def Tree_policy(self,root):
        t = root
        depth = 0
        while not t.state.is_end and not t.is_expanded():
            t = self.best_son(t,(1/2) ** (1/2))
            depth += 1
        if depth > self.depth:
            self.depth = depth
        legal_moves= t.state.get_legal_moves()
        moves = list(set(legal_moves)-set(t.used_moves))
        #print moves
        action = legal_moves[random.randrange(0,len(moves),1)]
        #can be instead by NNs
        state = t.state.copy()
        state.do_move(action)
        new = Node(state,t)
        t.used_moves.append(action)
        t.sons.append(new)
        return new
    def Default_policy(self,root):
        t = root.state.copy()
        while not t.is_end:
            legal_moves = t.get_legal_moves()
            moves_size = len(legal_moves)
            action = legal_moves[random.randrange(0,moves_size,1)]
            t.do_move(action)
        return t.get_winner()
    def UCT(self,v,father,c):
        if v.visited == 0:
            return -1
        return v.win / v.visited + c * (numpy.log(father.visited) / v.visited) * (1/2)
    def Backpropagation(self,result,t):
        node = t
        while True:
            if node.state.current_player == result:
                node.win += 1
            node.visited += 1
            if node == self.root:
                break
            node = node.father
    def best_son(self,node,c):
        sons = node.get_sons()
        best = -2
        bestson = node
        for i in sons:
            if self.UCT(i,node,c) == -1 or self.UCT(i,node,c) != -1 and self.UCT(i,node,c) > best:
                best = self.UCT(i,node,c)
                bestson = i
        return bestson

root = Node(GO(),-1)
tree = MCTS(root)
t = tree.root
t = tree.Search(t,20)
print t.state.board
