class Check:
    up = (-1,0)
    down = (1,0)
    left = (0,-1)
    right = (0,1)
    up2 = (-2,0)
    down2 = (2,0)
    left2 = (0,-2)
    right2 = (0,2)
    up3 = (-3,0)
    down3 = (3,0)
    left3 = (0,-3)
    right3 = (0,3)
    up4 = (-4,0)
    down4 = (4,0)
    left4 = (0,-4)
    right4 = (0,4)
    
    directions = [right, down, left, up]

    # =================================================================================================
    # SQUARE CHECK METHODS
    # =================================================================================================
    # region SQUARE CHECKS
    # =================================================================================================
    # Specific check
    def square_is(self, row, col, type):
        return self.board[row][col] == type
    def square_is_empty(self, row, col):
        return self.board[row][col] == self.empty_square_code
    def square_is_obstacle(self, row, col):
        return self.board[row][col] == self.obstacle_code
    # =================================================================================================
    # Diagonal obstacles check
    def obstacle_above_left(self, row, col):
        return self.board[row-1][col-1] == self.obstacle_code
    def obstacle_above_right(self, row, col):
        return self.board[row-1][col+1] == self.obstacle_code
    def obstacle_below_left(self, row, col):
        return self.board[row+1][col-1] == self.obstacle_code
    def obstacle_below_right(self, row, col):
        return self.board[row+1][col+1] == self.obstacle_code
    # =================================================================================================
    # Empty squares check
    def empty_square_left(self, row, col):
        return self.board[row][col-1] == self.empty_square_code
    def empty_square_right(self, row, col):
        return self.board[row][col+1] == self.empty_square_code
    def empty_square_above(self, row, col):
        return self.board[row-1][col] == self.empty_square_code
    def empty_square_below(self, row, col):
        return self.board[row+1][col] == self.empty_square_code
    def empty_square_left_and_right(self, row, col):
        return self.empty_square_left(row, col) and self.empty_square_right(row, col)
    def empty_square_above_and_below(self, row, col):
        return self.empty_square_above(row, col) and self.empty_square_below(row, col)
    # =================================================================================================
    # Obstacles check
    def obstacle_left(self, row, col):
        return self.board[row][col-1] == self.obstacle_code
    def obstacle_right(self, row, col):
        return self.board[row][col+1] == self.obstacle_code
    def obstacle_above(self, row, col):
        return self.board[row-1][col] == self.obstacle_code
    def obstacle_below(self, row, col):
        return self.board[row+1][col] == self.obstacle_code
    def obstacle_left_and_right(self, row, col):
        return self.obstacle_left(row, col) and self.obstacle_right(row, col)
    def obstacle_above_and_below(self, row, col):
        return self.obstacle_above(row, col) and self.obstacle_below(row, col)
    # =================================================================================================
    # Edges check
    def edge_left(self, row, col):
        return col == 0
    def edge_right(self, row, col):
        return col == len(self.board[0]) - 1
    def edge_above(self, row, col):
        return row == 0
    def edge_below(self, row, col):
        return row == len(self.board) - 1
    # =================================================================================================
    # Corners check
    def is_top_left_corner(self, row, col):
        return (row == 0 and col == 0)
    def is_top_right_corner(self, row, col):
        return (row == 0 and col == len(self.board[0]) -1)
    def is_bottom_left_corner(self, row, col):
        return (row == len(self.board) - 1 and col == 0)
    def is_bottom_right_corner(self, row, col):
        return (row == len(self.board) - 1 and col == len(self.board[0]) - 1)
    # =================================================================================================
    # Middle check
    def is_in_middle(self, row, col):
        return 0 < row < len(self.board) - 1 and 0 < col < len(self.board[0]) - 1
    # endregion

