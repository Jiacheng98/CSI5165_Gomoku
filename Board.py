class Board():
    """
    A class to represent a board. 
    ...

    Attributes
    ----------
    size : int

    """

    def __init__(self, size):
        self.size = size
        self.board = [['-' for x in range(size)] for y in range(size)] 

    def __len__(self):
        return self.size

    def __getitem__(self, row):
        return self.board[row]

    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self.board)  