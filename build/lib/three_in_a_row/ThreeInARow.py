import pandas as pd
import string
import sys
from IPython.display import display, clear_output


class ThreeInARow():
    
    def __init__(self, rows=5, columns=5):
        """
        Class that makes it possible to play the game "three in a row" within a jupyter notebook

        Attributes:
            rows (int): amount of rows the playing board has
            columns (int): amount of columns the playing board has
        """
        
        assert rows >= 3, "At least 3 rows are needed to play"
        assert columns >= 3, "At least 3 columns are needed to play"
        self.rows = rows
        self.columns = columns
        self.setup_board()
        self.current_player = 0
    
    def return_board(self):
        '''
        Function that outputs the playing board displaying all the played turns

        Args:
            None
        
        Returns:
            A display of the current status of the playing board
        '''
        # Clear output so there is only 1 print statement
        clear_output()
        
        def color_red_or_green(val):
            """
            Supporting function that creates background colors in a pandas DataFrame

            Args:
                None
            
            Returns:
                A green/red/white background based on the cell value
            """
            if val == 'X':
                color = "green"
            elif val == "O":
                color = "red"
            else:
                color = "white"
            return 'background-color: %s' % color

        # Set CSS properties for th elements in dataframe
        th_props = [
          ('font-size', '13px'),
          ('text-align', 'center'),
          ('font-weight', 'bold'),
          ('color', '#6d6d6d'),
          ('background-color', '#f7f7f9')
          ]

        # Set CSS properties for td elements in dataframe
        td_props = [
            ('font-size', '20px'),
            ('font_weight', 'bold'),
            ('text-align', 'center'),
            ('border', '1px solid'),
            ('width', '80px'),
            ('height', '80px')
          ]

        # Set table styles
        styles = [
          dict(selector="th", props=th_props),
          dict(selector="td", props=td_props)
          ]

        # Show board in output of celll
        display((self.board.style 
            .applymap(color_red_or_green)
            .set_table_styles(styles)))
    
    def setup_board(self):
        """
        Function that creates the initial empty playing board
        
        Args:
            None
        
        Output:
            Displays the empty playboard
        """
        headers = list(string.ascii_uppercase)[:self.columns]
        rows = [x+1 for x in range(self.rows)]
        self.board = pd.DataFrame(data='', columns=headers, index=rows)
        self.return_board()
    
    def return_player(self):
        """
        Function that shows which player's turn it is

        Args:
            None
        
        Output:
            Print statement with player's turn
        """
        print(f"\nPlayer turn: {self.current_player % 2 + 1}\n")
    
    def find_first_option(self):
        """
        Function that finds the first option available in the selected column

        Args:
            None
        
        Output:
            place (int), the row-number of the first available row
        """
        place = len(self.board)
        for i in range(len(self.board), 0, -1):
            if self.board[self.column][i] != "":
                place = i - 1
                
        return place
    
    def play(self):
        """
        Function that represents one turn of the game

        Args:
            None
        
        Output:
            Print statement with victory
        """
        self.return_player()
        loc = input("Enter Column (Press q to leave): " )
              
        if str(loc) == "q":
            sys.exit('Game ended')
        
        if len(loc) > 1:
            print("Input can maximally be 1 character, pick another location")
            self.play()
        
        if self.current_player % 2 != 1:
            self.symbol = "X"
        else:
            self.symbol = "O"
            
        try:
            self.column = loc.upper()
            if string.ascii_uppercase.find(self.column) + 1 > self.columns:
                print("Column out of range, pick another location")
                self.play()
            else:
                self.col_num = string.ascii_uppercase.find(self.column)
        except Exception as e:
            print(e)
            print("Invalid Input, pick another location")
            self.play()
        
        self.row = self.find_first_option()
        
        if self.row <= 0:
            print("Invalid Input, pick another location")
            self.play()
                
        if self.board[self.column][self.row] != '':
            print("There already is input here! pick another location")
            self.play()
        else:      
            self.board.loc[(self.row, self.column)] = self.symbol
            
        self.return_board()
        
        if self.check_victory():
            print(f"Congratulations! Player {self.current_player % 2 + 1} won ")
            restart = input("Do you want to play again? (Y/N): ")
            
            if str((restart).lower()) == "y":
                self.setup_board()
                self.play()
            else:
                sys.exit('Game ended')
                
        else:        
            self.current_player += 1
            self.play()
        
    def check_victory(self):
        """
        Function that checks if there are 3 of the same symbol in a row somewhere on the board

        Args:
            None
        
        Output:
            True if the current player won
            False if the current player didnt win
        """

        for hor in range(-1, 2):
            for ver in range(-1, 2):
                r = self.row + hor
                v = string.ascii_uppercase[self.col_num + ver]

                # No movement so ignore
                if hor == 0 and ver == 0:
                    continue

                # continue if out of index
                if r <= 0 or self.col_num + ver < 0 or r > len(self.board) or self.col_num + ver >= len(self.board):
                    continue

                # if equal to symbol
                if self.board[v][r] == self.symbol:
                    
                    # Other side
                    r1 = self.row + -1*hor
                    v1 = string.ascii_uppercase[self.col_num + ver*-1]
                    
                    # Only check for victory if within index
                    if r1 > 0 and self.col_num + ver*-1 >= 0 and r1 <= len(self.board) and self.col_num + ver*-1 <= len(self.board):
                        # Win if similar symbol            
                        if self.board[v1][r1] == self.symbol:
                            return True

                    # One extra to left/right/diagonal
                    r2 = self.row + 2*hor 
                    v2 = string.ascii_uppercase[self.col_num + ver*2]
                    
                    # Only check for victory if within index
                    if r2 > 0 and self.col_num + ver*2 >= 0 and r2 <= len(self.board) and self.col_num + ver*2 <= len(self.board):
                        # Win if similar symbol             
                        if self.board[v2][r2] == self.symbol:
                            return True
        return False
        