
def gen_grid(w, h):
  # grid = [[(y*w)+x for x in range(w)] for y in range(h)]
  return [[None for x in range(w)] for y in range(h)]

def parse_pos(w, h, pos: str):
  assert(len(pos) > 0)
  # find midpoint
  i = 0
  while pos[i] not in "1234567890":
    i += 1
  y = int(pos[i:])
  assert(y < h)
  # convert left half to base-26
  b26 = pos[:i].lower()
  exp = len(b26) - 1
  x = 0
  for c in b26:
    x += (ord(c) - 97) * (26 ** exp)
    exp -= 1
  assert(x < w)
  return (x, h - y)

def knight_pathfinder(w, h, pos: str):
  grid = gen_grid(w, h)
  posx, posy = parse_pos(w, h, pos)
  posqueue = [(posx, posy, 0)]
  while len(posqueue) > 0:
    info = posqueue.pop(0)
    cposx, cposy, d = info[0], info[1], info[2]
    # get legal moves
    for x in (2, 1, -1 , -2):
      if abs(x) == 2:
        for y in (1, -1):
          nextpos = (-1, -1, -1)
          if 0 <= cposy+y < h and 0 <= cposx+x < w and (cposx+x, cposy+y):
            nextpos = (cposx+x, cposy+y, d+1)
          if nextpos != (-1, -1, -1) \
          and nextpos not in posqueue \
          and grid[nextpos[1]][nextpos[0]] is None:
            posqueue += [nextpos]
      else:
        for y in (2, -2):
          nextpos = (-1, -1, -1)
          if 0 <= cposy+y < h and 0 <= cposx+x < w and (cposx+x, cposy+y):
            nextpos = (cposx+x, cposy+y, d+1)
          if nextpos != (-1, -1, -1) \
          and nextpos not in posqueue \
          and grid[nextpos[1]][nextpos[0]] is None:
            posqueue += [nextpos]
    
    grid[cposy][cposx] = d

  return grid
  ...

"""
def print_grid(grid):
  h = len(grid)
  w = len(grid[0])
  for y in range(h):
    for x in range(w):
      print(f"[{grid[y][x]:2d}]", end="")
    print()
"""
def print_grid(grid):
    # ANSI foreground colors
    COLORS = {
        0: "\033[106m",  # blue
        1: "\033[101m",  # red
        2: "\033[42m",  # green
        3: "\033[45m",  # magenta
        4: "\033[103m",  # yellow
        5: "\033[100m",  # yellow
    }
    RESET = "\033[0m"

    h = len(grid)
    w = len(grid[0])

    for y in range(h):
        for x in range(w):
            v = grid[y][x]
            color = COLORS.get(v, "")  # default: no color if not mapped
            # print(f"{color} {f'{v:2d}' if v > 5 else '  '} {RESET}", end="")
            print(f"{color} {f'{v:2d}'} {RESET}", end="")
        print()


w, h, pos = 8, 8, "d4"
print(f"From {pos}, knight can make")
print_grid(knight_pathfinder(w, h, pos))
print(f"hops to get there")
# print_grid(knight_pathfinder(36, 36, "u18"))