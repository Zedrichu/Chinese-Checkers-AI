class Tile:
    def __call__(self, x, y):
        return self.tiles[y][x]
    
    