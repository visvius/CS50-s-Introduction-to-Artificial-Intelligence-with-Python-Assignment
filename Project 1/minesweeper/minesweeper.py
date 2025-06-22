import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # mines can only be determined if no. of cells == count of mines, since all cells are mines
        if (len(self.cells) == self.count):
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if no cell can be a mine, all of them are safe
        # if any of the cell can be a mine, we have no certainity
        if (self.count == 0):
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # remove the cell that is a mine
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # remove the cell that is safe and not a mine
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1 - add to moves
        self.moves_made.add(cell)
        # Step 2 - mark it as safe(given) and updates every other knowledge
        self.mark_safe(cell)

        # Step 3 - create a new sentence containing every neighbor and add it to knowledge
        # Note - remove neighbors known to be safe or mine
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (i, j)
                    # if neighbor know to be a mine, dont add it to knowledge and reduce counts of known mines
                    if neighbor in self.mines:
                        count -= 1
                    # if neighbor is not know to be a mine or is confirmed to be safe, add it 
                    elif neighbor not in self.safes:
                        neighbors.add(neighbor)
        # if any new neighbors have been found
        if neighbors:
            self.knowledge.append(Sentence(neighbors, count))
        
        # Step 4 - Checking if any new safes or mines added from sentences
        updatesDone = True
        while updatesDone:
            updatesDone = False
            allSafes = set()
            allMines = set()
            
            # finding all safe and known mine cells from all knowledge sentences
            for sentence in self.knowledge:
                allSafes = allSafes.union(sentence.known_safes())
                allMines = allMines.union(sentence.known_mines())

            # check if new safe cells have been found
            for safe_cell in allSafes:
                if safe_cell not in self.safes:
                    self.mark_safe(safe_cell)
                    updatesDone = True

            # check if new mines have been found
            for mine_cell in allMines:
                if mine_cell not in self.mines:
                    self.mark_mine(mine_cell)
                    updatesDone = True
        
        # Step 5 - infer new sentences using subsets 
        inferences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2:
                    continue
                # remove the subset from the superset to find new inferences
                if s1.cells.issubset(s2.cells):
                    newCells = s2.cells - s1.cells
                    diffCount = s2.count - s1.count
                    inference = Sentence(newCells, diffCount)
                    # if inference is not already known
                    if inference not in inferences and inference not in self.knowledge:
                        inferences.append(inference)
        
        self.knowledge.extend(inferences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        # no safe moves known
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        validMoves = set()
        for i in range(self.height):
            for j in range(self.width):
                validMoves.add((i,j))
        
        validMoves = validMoves - self.mines - self.moves_made

        if validMoves:
            return random.choice(list(validMoves))
        return None

