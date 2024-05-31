def is_valid_move(board, visited, row, col, designated_point):
    rows = len(board)
    cols = len(board[0])
    return (0 <= row < rows and 0 <= col < cols and
            board[row][col] != 'O' and not visited[row][col] and
            (row, col) != designated_point)

def does_path_exist(board, start, end, designated_point):
    rows = len(board)
    cols = len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def backtrack(row, col):
        if (row, col) == end:
            return True
        visited[row][col] = True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(board, visited, new_row, new_col, designated_point):
                if backtrack(new_row, new_col):
                    return True
                
        visited[row][col] = False
        return False
    
    start_row, start_col = start
    return backtrack(start_row, start_col)

board = [
    [' ', ' ', ' ', 'O', ' ', ' ', 'O', ' '],
    ['O', ' ', 'O', ' ', ' ', ' ', ' ', 'O'],
    [' ', ' ', ' ', ' ', 'O', ' ', ' ', ' '],
    [' ', 'O', ' ', ' ', ' ', 'O', ' ', ' '],
    [' ', ' ', ' ', ' ', 'O', ' ', ' ', ' '],
    ['O', ' ', 'O', ' ', ' ', ' ', 'O', ' ']
]

start = (1, 0)
end = (1, 2)
designated_point = (1, 1)

path_exists = does_path_exist(board, start, end, designated_point)
print("Path exists:", path_exists)
