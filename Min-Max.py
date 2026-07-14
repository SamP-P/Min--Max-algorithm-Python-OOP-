class MinMax(Player):
    def __init__(self, board, depth):
        super().__init__()
        self.board = board
        self.obj_grid = board.getgrid()
        self.testgrid = copy.deepcopy(board.getgrid())
        self.depth = depth
        self.value = -1000
        self.tempvalue = 0
        self.col = 0
        self.row = 0

        self.ROW = 0
        self.COL = 0 
        self.mf = False

        

        self.depthcurrent = 1


    def evaluate_move(self, row, col):
        score = 0

        score += self.center_bonus(row, col)
        score += self.line_strength(row, col, "white")
        score += self.block_opponent(row, col)
        score += self.check_captures(row, col, "white")

        score += self.threat_bonus(row, col, "white")

        return score


    def center_bonus(self, row, col):
        center = ROWS // 2
        distance = abs(row - center) + abs(col - center)
        return max(0, 10 - distance)


    def line_strength(self, row, col, player):
        score = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for dr, dc in directions:
            score += self.count_stones2(row, col, dr, dc, "white") * 2

        return score


    def block_opponent(self, row, col):
        score = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for dr, dc in directions:
            score += self.count_stones2(row, col, dr, dc, "black") * 3

        return score


    def check_captures(self, row, col, player):
        opponent = "black" if player == "white" else "white"
        captures = 0
    
        for dr, dc in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            if (0 <= row + 3*dr < ROWS and 0 <= col + 3*dc < COLS):
                if (self.testgrid[row + dr][col + dc] == opponent and
                    self.testgrid[row + 2*dr][col + 2*dc] == opponent and
                    self.testgrid[row + 3*dr][col + 3*dc] == player):
                    captures += 2
        
            if (0 <= row - 3*dr < ROWS and 0 <= col - 3*dc < COLS):
                if (self.testgrid[row - dr][col - dc] == opponent and
                    self.testgrid[row - 2*dr][col - 2*dc] == opponent and
                    self.testgrid[row - 3*dr][col - 3*dc] == player):
                    captures += 2
    
        return captures


    def threat_bonus(self, row, col, player):
        score = 0
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for dr, dc in directions:
            count = self.count_stones2(row, col, dr, dc, player)

            if count == 3:
                score += 10     
            elif count == 4:
                score += 50     
            elif count >= 5:
                score += 1000   

        return score







    def minimax(self, depth, maximising, low= -1000, high = 1000):
    
        if depth == 0:
            score = 0
            for r in range(ROWS):
                for c in range(COLS):
                    if self.testgrid[r][c] == "white":
                        score += self.evaluate_move(r, c)
                    elif self.testgrid[r][c] == "black":
                        score -= self.evaluate_move(r, c)
            return score

        if maximising:
                best = -10000
                for r in range(ROWS):
                    for c in range(COLS):
                        if self.testgrid[r][c] is None:
                            near = False
                            for dr in range(-2, 3):
                                for dc in range(-2, 3):
                                    nr, nc = r + dr, c + dc
                                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                                        if self.testgrid[nr][nc] is not None:
                                            near = True
                                            break
                                if near:
                                    break
                
                            if not near:
                                continue
                    
                            self.testgrid[r][c] = "white"
                            score = self.minimax(depth - 1, False, low, high)
                            self.testgrid[r][c] = None
                            best = max(best, score)
                            low = max(low, score)
                            if high <= low:
                                return best
                return best






        else:
            best = 1000
            for r in range(ROWS):
                for c in range(COLS):
                    if self.testgrid[r][c] is None:
                        near = False
                        for dr in range(-2, 3):
                            for dc in range(-2, 3):
                                nr, nc = r + dr, c + dc
                                if 0 <= nr < ROWS and 0 <= nc < COLS:
                                    if self.testgrid[nr][nc] is not None:
                                        near = True
                                        break
                            if near:
                                break
                
                        if not near:
                            continue
                    
                        self.testgrid[r][c] = "black"
                        score = self.minimax(depth - 1, True, low, high)
                        self.testgrid[r][c] = None
                        best = min(best, score)
                        high = min(high, score)
                        if high <= low:
                            return best
            return best
        
      
    def MinMaxloop(self):
        self.mf = False
        Depth = self.depthcurrent
        self.value = -10000
    
        candidates = []
    
        for col in range(COLS):
            for row in range(ROWS):
                if self.testgrid[row][col] is None:
                    near_stone = False
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            r, c = row + dr, col + dc
                            if 0 <= r < ROWS and 0 <= c < COLS:
                                if self.testgrid[r][c] is not None:
                                    near_stone = True
                                    break
                        if near_stone:
                            break
                
                    if near_stone:
                        candidates.append((row, col))
    
        if len(candidates) == 0:
            center = ROWS // 2
            for col in range(center - 3, center + 4):
                for row in range(center - 3, center + 4):
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if self.testgrid[row][col] is None:
                            candidates.append((row, col))
    
        for row, col in candidates:
            self.tempvalue = 0
        
            self.testgrid[row][col] = "white"
            self.tempvalue = self.minimax(self.depth, False, -1000, 1000)
            self.testgrid[row][col] = None
        
            if self.tempvalue > self.value:
                self.row = row  
                self.col = col
                self.value = self.tempvalue
    
        self.mf = True
        return
                  

    def count_stones2(self, row, col, dr, dc, player):
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and self.testgrid[r][c] == player:
            count += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and self.testgrid[r][c] == player:
            count += 1 
            r -= dr 
            c -= dc
        return count

            
    def stone_count(self):
        count = 0
        for i in range(ROWS):
            for l in range(COLS):
                if self.board.getgrid()[i][l] is not None:
                    count += 1
        return count


    def movereturn(self):
        if self.stone_count() > 1:
            self.mf = False
            self.depthcurrent = 1
            self.value = -1
            self.testgrid = copy.deepcopy(self.board.getgrid())
            self.MinMaxloop()
            return self.col, self.row

        else:
            center = ROWS // 2
            r = random.randint(center - 3, center + 3)
            c = random.randint(center - 3, center + 3)
            return c, r

