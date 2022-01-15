from random import choice, sample
from collections import namedtuple

Ladder = namedtuple("Ladder", "head tail")
Snake = namedtuple("Snake", "head tail")

def generate_snakes_ladders():
    snakes = []
    ladders = []
    n_snake_or_ladders = [7,8,9]
    # number of snakes to put on board
    n_snakes = choice(n_snake_or_ladders)
    # number of ladders to put on board
    n_ladders = choice(n_snake_or_ladders)

    # create a board layout 10X10 where each row is sequence of 10 cells
    l = [list(map(lambda x: x + (i*10),range(1,11))) for i in range(10)]
    
    # a map structure that keeps link to each row of board
    board  = {k+1 : v for k,v in enumerate(l) }
    
    # to ensure no ladder leads to 100 and no snake bites here
    board[10].remove(100)
    
    '''
        The below code generates snake position on board using following method:
        1. Generate row keys of board
        2. Select one key from the list
        3. Remove the key from keys (so that we don't get same key twice)
        4. Select another key from keys
        
        These two keys will be used to access the row sequence of board, and selecting 
        one element from each of the two rows. This will help in generating 
        head and tail positions of snake on  the board.

        below is sample depiction of board
        {
            "1": list(range(1,11))
            "2" : list(range(11,21))
            "3" : list(range(21,31))
            .
            .
            .
            "10": list(range(91,101))
        }
        
        The same logic follows for generating ladders but the board state remains same
        to avoid snake's head and ladder's head collision
    
    '''
    # modifies the board map
    while n_snakes:
        keys = list(range(1 ,len(board) + 1))
        key1 = choice(keys)
        keys.remove(key1)
        key2 = choice(keys)

        start = choice(board[key1])
        end = choice(board[key2])
        # reorder start end so that s > e (Part of requirement where snake's head must be ahead of tail.)
        rse = (start, end) if start > end else (end, start) 
        board[key1].remove(start)
        board[key2].remove(end) 

        head, tail = rse
        snakes.append(Snake(head, tail))
        
        n_snakes-=1
    
    while n_ladders:
        keys = list(range(1,11))
        key1 = choice(keys)
        keys.remove(key1)
        key2 = choice(keys)

        start = choice(board[key1])
        end = choice(board[key2])
        rse = z = (start, end) if start > end else (end, start) # reorder start end so that s > e
        board[key1].remove(start)
        board[key2].remove(end) 
        
        head, tail = rse
        ladders.append(Ladder(head, tail))
        
        n_ladders-=1
    return (snakes, ladders)

class Coin:
    def __init__(self, color) -> None:
        self.color = color
        self.index = -1
    def update_index(self, new_index):
        self.index = new_index

class Dice:
    def __init__(self):
        self._side = 6
    
    def roll(self) -> int:
        return choice(range(1, self._side + 1))
    
class Player:
    def __init__(self, name, coin:Coin) -> None:
        self.name = name
        self.coin = coin
        self.has_won = False 
        self.last_roll = 0
        self.rank = -1

    def roll(self, dice: Dice):
       res = dice.roll()
       self.last_roll = res
       print(f"{self.name} rolled ->{res}")

    def update_rank(self, rank):
        self.rank = rank
    
    def __str__(self) -> str:
        return str({"player": self.name, "coin": self.coin.color, "index": self.coin.index, "rank": self.rank})

class SnakeBoard:
    def __init__(self, snakes, ladders ):
        self.snakes = snakes
        self.ladders = ladders
    
    # return  if player has next move or not
    def update(self, player: Player):
        has_next_move = False
        if player.coin.index >= 0 :
            new_idx = player.coin.index + player.last_roll
            if  new_idx <= 99:
                snake_head = self.snakes.get(new_idx)
                ladder_tail  = self.ladders.get(new_idx)
                if snake_head:
                    new_idx = snake_head
                elif ladder_tail:
                    new_idx = ladder_tail
                player.coin.update_index(new_idx)
                if player.last_roll == 6:
                    has_next_move = True
            elif new_idx == 100 and player.last_roll != 6:
                player.coin.update_index(100)
                player.has_won = True
            print(player)

        else:
            if player.last_roll == 6:
                player.coin.update_index(0)
                has_next_move = True
                print(player)

        return has_next_move

#TODO: Handle more than two consecutive sixes 
class Game:
    def __init__(self, n_players) -> None:
        self.n_players = n_players
        self.coins = [Coin(color) for color in sample("RGBY", k= n_players)]
        self.players = [Player(f"Player {i}", coin) for i, coin in enumerate(self.coins)]
        self.dice = Dice() 
        self.board = self.__setup_board()
        self.current_player = None
        self.players_won = 0
    
    def start(self):
        current_player_idx = 0 
        while True:
            current_player_idx = current_player_idx % self.n_players
            self.current_player = self.players[current_player_idx]
            print("\n")
            has_next_move = not self.current_player.has_won
            while has_next_move:
                self.current_player.roll(self.dice)
                has_next_move = self.board.update(self.current_player)
                
                if self.current_player.has_won:
                    self.players_won+=1
                    self.current_player.update_rank(self.players_won)
            current_player_idx +=1

            # continue playing until a loser remains
            if self.players_won + 1 == len(self.players):
                break

        print("\n")
        _ = [print(player) for player in self.players]

    def __setup_board(self):
        snakes_pos, ladders_pos = generate_snakes_ladders()
        snakes = {head: tail for head, tail in snakes_pos}
        ladders ={tail:head for head, tail in ladders_pos}
        return SnakeBoard(snakes, ladders)


if __name__ == "__main__":
   players = 4
   g  = Game(players)
   g.start()