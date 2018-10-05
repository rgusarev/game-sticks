from tkinter import *
from random import choice, randint


# Scheme of segments numbering
   #         0          1
   #  -------------------------
   #  |           |           |
   #  |           |           |
   # 6|          7|          8|
   #  |           |           |
   #  |     2     |     3     |
   #  ------------------------
   #  |           |           |
   #  |           |           |
   # 9|         10|         11|
   #  |           |           |
   #  |           |           |
   #  |     4     |     5     |
   #  ------------------------

class Game:
    def __init__(self, ROWS, COLUMNS, player=1):
        self.player = player
        self.ROWS = ROWS
        self.COLUMNS = COLUMNS
        self.segments = []
        self.Map = [[Cell() for i in range(COLUMNS)] for j in range(ROWS)]

        # creating top horizontal segments
        for j in range(COLUMNS):
            x = Segment(top_cell=(0, j))
            self.segments.append(x)
            self.Map[0][j].top_seg = len(self.segments) - 1

        # creating middle horizontal segments
        for i in range(ROWS - 1):
            for j in range(COLUMNS):
                x = Segment(bottom_cell=(i, j), top_cell=(i + 1, j))
                self.segments.append(x)
                self.Map[i][j].bottom_seg = len(self.segments) - 1
                self.Map[i + 1][j].top_seg = len(self.segments) - 1

        # creating bottom horizontal segments
        for j in range(COLUMNS):
            x = Segment(bottom_cell=(ROWS - 1, j))
            self.segments.append(x)
            self.Map[ROWS - 1][j].bottom_seg = len(self.segments) - 1

        # creating all vertical segments
        for i in range(ROWS):
            x = Segment(left_cell=(i, 0))
            self.segments.append(x)
            self.Map[i][0].left_seg = len(self.segments) - 1
            for j in range(COLUMNS - 1):
                x = Segment(left_cell=(i, j), right_cell=(i, j + 1))
                self.segments.append(x)
                self.Map[i][j].right_seg = len(self.segments) - 1
                self.Map[i][j + 1].left_seg = len(self.segments) - 1
            x = Segment(right_cell=(i, COLUMNS - 1))
            self.segments.append(x)
            self.Map[i][COLUMNS - 1].right_seg = len(self.segments) - 1

    def IsOccupied(self, x, y):
        '''
        Returns True iff all neighbour segments of self.Map[x][y] are used
        '''
        return self.segments[self.Map[x][y].left_seg].IsUsed() and \
               self.segments[self.Map[x][y].top_seg].IsUsed() and \
               self.segments[self.Map[x][y].right_seg].IsUsed() and \
               self.segments[self.Map[x][y].bottom_seg].IsUsed()

    def OccupiedBy(self, x, y):
        '''
        Returns number of the player who occupied this cell. Returns 0 if cell is empty.
        '''
        return self.Map[x][y]._occupied

    def GetAllFreeSegments(self):
        '''
        Returns list of all free segments of current gameboard.
        '''
        return [k for k in range(len(self.segments)) if not self.segments[k]._used]

    def getAllFreeSegmentsNWall(self, N):
        '''
        Returns list of all segments which are borders of all cells with exactly N used border segments.
        '''
        ans = []
        for c in self.getAllCells(N):
            x, y = c
            if not self.segments[self.Map[x][y].left_seg].IsUsed():
                ans.append(self.Map[x][y].left_seg)
            if not self.segments[self.Map[x][y].top_seg].IsUsed():
                ans.append(self.Map[x][y].top_seg)
            if not self.segments[self.Map[x][y].right_seg].IsUsed():
                ans.append(self.Map[x][y].right_seg)
            if not self.segments[self.Map[x][y].bottom_seg].IsUsed():
                ans.append(self.Map[x][y].bottom_seg)
        return ans

    def getAllCells(self, count):
        '''
        Returns list of (x, y) cells with exatly count used border segments.
        '''
        res = []
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if (self.segments[self.Map[i][j].left_seg]._used) +\
                   (self.segments[self.Map[i][j].top_seg]._used) +\
                   (self.segments[self.Map[i][j].right_seg]._used) + \
                   (self.segments[self.Map[i][j].bottom_seg]._used) == count:
                    res.append((i, j))
        return res

    def MakeMove(self, seg_id):
        '''
        Makes move. Changes gameboard. Maybe shift current player.
        '''
        if self.segments[seg_id].IsUsed():
            return
        self.segments[seg_id].SetUsed()
        bonus_move = False
        if self.segments[seg_id].left_cell is not None:
            x, y = self.segments[seg_id].left_cell
            if self.IsOccupied(x, y):
                bonus_move = True
                self.Map[x][y]._occupied = self.player
        if self.segments[seg_id].top_cell is not None:
            x, y = self.segments[seg_id].top_cell
            if self.IsOccupied(x, y):
                bonus_move = True
                self.Map[x][y]._occupied = self.player
        if self.segments[seg_id].right_cell is not None:
            x, y = self.segments[seg_id].right_cell
            if self.IsOccupied(x, y):
                bonus_move = True
                self.Map[x][y]._occupied = self.player
        if self.segments[seg_id].bottom_cell is not None:
            x, y = self.segments[seg_id].bottom_cell
            if self.IsOccupied(x, y):
                bonus_move = True
                self.Map[x][y]._occupied = self.player
        if not bonus_move:
            self.player = 3 - self.player

    def WhoWin(self):
        w1, w2 = 0, 0
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if self.Map[i][j]._occupied == 1:
                    w1 += 1
                else:
                    w2 += 1
        return 1 if w1 > w2 else 2

    def __str__(self):
        res = []
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                fstring = 'i={0:d} j={1:d} segments: left={2:d}, top={3:d}, right={4:d}, bottom={5:d} occupied by {6:d}'
                res.append(fstring.format(i, j, self.Map[i][j].left_seg, self.Map[i][j].top_seg, self.Map[i][j].right_seg, self.Map[i][j].bottom_seg, self.Map[i][j]._occupied))
        return '\n'.join(['current player ' + str(self.player)] + res)


class Cell:
    '''
    Cell describes one cell of the gameboard with its 4 border segments
    '''
    def __init__(self, left_seg = None, top_seg = None, right_seg = None, bottom_seg = None, occupied = 0):
        self.left_seg = left_seg
        self.top_seg = top_seg
        self.right_seg = right_seg
        self.bottom_seg = bottom_seg
        self._occupied = occupied

    def left(self):
        return self._left

    def right(self):
        return self._right

    def top(self):
        return self._top

    def bottom(self):
        return self._bottom

    def __str__(self):
        return 'Segments from left clockwise: {0} {1} {2} {3}'.format(self.left_seg, self.top_seg, self.right_seg, self.bottom_seg)



class Segment:
    '''
    Decribes one segment with neigbour cells if exists
    '''
    def __init__(self, left_cell = None, right_cell = None, top_cell = None, bottom_cell = None):
        self.left_cell = left_cell
        self.top_cell = top_cell
        self.right_cell = right_cell
        self.bottom_cell = bottom_cell
        self._used = False

    def IsUsed(self):
        return self._used

    def SetUsed(self):
        self._used = True

    def __str__(self):
        left = '' if self.left_cell is None else 'left=' + str(self.left_cell)
        top = '' if self.top_cell is None else 'top=' + str(self.top_cell)
        right = '' if self.right_cell is None else 'right=' + str(self.right_cell)
        bottom = '' if self.bottom_cell is None else 'bottom=' + str(self.bottom_cell)
        return '{0:s} {1:s} {2:s} {3:s}'.format(left, top, right, bottom)

def round_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def CreateGameField(H, W):
    H += 1
    W += 1
    # horizontal segments
    for i in range(H):
        for j in range(W - 1):
            round_rectangle(w, DX + CELLSIZE * j + GAP, DY + CELLSIZE * i - GAP, DX + CELLSIZE * (j + 1) - GAP, DY + CELLSIZE * i + GAP, fill=FREE_SEGMENT_COLOR)

    # # vertical segments
    for i in range(H - 1):
        for j in range(W):
            round_rectangle(w, DX + CELLSIZE * j - GAP, DY + CELLSIZE * i + GAP, DX + CELLSIZE * j + GAP, DY + CELLSIZE * (i + 1) - GAP, fill=FREE_SEGMENT_COLOR)            


def ShowGame(G):
    for i in range(G.ROWS):
        for j in range(G.COLUMNS):
            if not G.IsOccupied(i, j):
                clr = '#000000'
            else:
                if G.OccupiedBy(i, j) == 1:
                    clr = '#660000'
                else:
                    clr = '#006600'
            round_rectangle(w, DX + CELLSIZE * j + GAP, DY + CELLSIZE * i + GAP, DX + CELLSIZE * (j + 1) - GAP, DY + CELLSIZE * (i + 1) - GAP, fill = clr)


def PointSegment(event):
    seg_id = -1
    for i in range(H + 1):
        for j in range(W):
            if DX + CELLSIZE * j + GAP <= event.x <= DX + CELLSIZE * (j + 1) - GAP and DY + CELLSIZE * i - GAP <= event.y <= DY + CELLSIZE * i + GAP:
                round_rectangle(w, DX + CELLSIZE * j + GAP, DY + CELLSIZE * i - GAP, DX + CELLSIZE * (j + 1) - GAP, DY + CELLSIZE * i + GAP, fill=OCCUPIED_SEGMENT_COLOR)
                seg_id = W * i + j
    for i in range(H):
        for j in range(W + 1):
            if DX + CELLSIZE * j - GAP <= event.x <= DX + CELLSIZE * j + GAP and DY + CELLSIZE * i + GAP <= event.y <= DY + CELLSIZE * (i + 1) - GAP:
                round_rectangle(w, DX + CELLSIZE * j - GAP, DY + CELLSIZE * i + GAP, DX + CELLSIZE * j + GAP, DY + CELLSIZE * (i + 1) - GAP, fill=OCCUPIED_SEGMENT_COLOR)
                seg_id = (H + 1) * W + i * (W + 1) + j
    if seg_id >= 0:
        G.MakeMove(seg_id)
    ShowGame(G)

def PlayGame(G, p1, p2):
    while len(G.GetAllFreeSegments()) > 0:
        if G.player == 1:
            G.MakeMove(p1(G))
        else:
            G.MakeMove(p2(G))

def Player_Random(G):
    return choice(G.GetAllFreeSegments())


def Player_Simple_Euristic(G):
    t2 = G.getAllFreeSegmentsNWall(2)
    t3 = G.getAllFreeSegmentsNWall(3)
    all_segs = G.GetAllFreeSegments()
    others = list(set(all_segs) - set(t2))
    if len(t3) > 0:
        return choice(t3)
    else:
        if len(others) > 0:
            return choice(others)
        else:
            return choice(all_segs)

# # --------------START-------------------------------
# # THIS PIECE IS FOR STAT GAMES BETWEEN TWO FUNCTIONS
# H, W = 3, 3
# w1, w2 = 0, 0
# GAMES = 100
# for _ in range(GAMES):
#     G = Game(ROWS = H, COLUMNS = W)
#     PlayGame(G, Player_Random, Player_Simple_Euristic)
#     w = G.WhoWin()
#     if w == 1:
#         w1 += 1
#     else:
#         w2 += 1
# print('Total games: {0:d}'.format(GAMES))
# print('First won in {0:d} games, second won in {1:d}'.format(w1, w2))
# # --------------END--------------------------------


# --------------START-----------------------------
# THIS PIECE IS FOR VISUAL GAME BETWEEN TWO PEOPLE
H, W = 3, 3
G = Game(ROWS = H, COLUMNS = W)
OCCUPIED_SEGMENT_COLOR = '#cccccc'
FREE_SEGMENT_COLOR = '#333333'

 
master = Tk()
DX, DY = 15, 15
CELLSIZE = (600 - DX * 2) // max(H, W)

GAP = 10
w = Canvas(master, width=W * CELLSIZE + 2 * DX, height=H * CELLSIZE + 2 * DY, bg='#000000')
CreateGameField(H, W)
w.bind('<Button-1>', PointSegment)
w.pack()
mainloop()
# --------------END-------------------------------


# H, W = 3, 3
# G = Game(ROWS = H, COLUMNS = W)
# a, b = map(int, input('Enter cell coordinates: ').split())
# print(G.Map[a][b])