"""Tests for sudoku_logic module."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import sudoku_logic


class TestBoardCreation:
    """Test board creation functionality."""

    def test_create_empty_board(self):
        """Test that empty board is created with correct dimensions."""
        board = sudoku_logic.create_empty_board()
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)
        assert all(cell == 0 for row in board for cell in row)

    def test_empty_board_all_zeros(self):
        """Test that all cells in empty board are zero."""
        board = sudoku_logic.create_empty_board()
        for row in board:
            for cell in row:
                assert cell == sudoku_logic.EMPTY


class TestIsSafe:
    """Test the is_safe validation function."""

    def test_is_safe_empty_board(self):
        """Test that any number is safe on empty board."""
        board = sudoku_logic.create_empty_board()
        for num in range(1, 10):
            assert sudoku_logic.is_safe(board, 0, 0, num)

    def test_is_safe_duplicate_in_row(self):
        """Test that duplicate in row is not safe."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        assert not sudoku_logic.is_safe(board, 0, 1, 5)

    def test_is_safe_duplicate_in_column(self):
        """Test that duplicate in column is not safe."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        assert not sudoku_logic.is_safe(board, 1, 0, 5)

    def test_is_safe_duplicate_in_box(self):
        """Test that duplicate in 3x3 box is not safe."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # Any cell in the same 3x3 box should fail
        assert not sudoku_logic.is_safe(board, 1, 1, 5)
        assert not sudoku_logic.is_safe(board, 2, 2, 5)

    def test_is_safe_different_box(self):
        """Test that same number in different box is safe."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # This should be safe - different 3x3 box
        assert sudoku_logic.is_safe(board, 3, 3, 5)

    def test_is_safe_valid_placement(self):
        """Test valid placements."""
        board = sudoku_logic.create_empty_board()
        board[0][0] = 1
        board[0][1] = 2
        board[1][0] = 3
        # Number 4 should be safe at (1,1)
        assert sudoku_logic.is_safe(board, 1, 1, 4)


class TestDeepCopy:
    """Test the deep_copy function."""

    def test_deep_copy_creates_copy(self):
        """Test that deep_copy creates a separate copy."""
        board1 = sudoku_logic.create_empty_board()
        board1[0][0] = 5
        board2 = sudoku_logic.deep_copy(board1)
        board2[0][0] = 9
        assert board1[0][0] == 5
        assert board2[0][0] == 9

    def test_deep_copy_nested_independence(self):
        """Test that nested structures are independent."""
        board1 = sudoku_logic.create_empty_board()
        board1[0][0] = 7
        board2 = sudoku_logic.deep_copy(board1)
        board2[0] = [0] * 9
        assert board1[0][0] == 7
        assert board2[0][0] == 0


class TestFillBoard:
    """Test the fill_board function."""

    def test_fill_board_completes(self):
        """Test that fill_board completes and fills entire board."""
        board = sudoku_logic.create_empty_board()
        result = sudoku_logic.fill_board(board)
        assert result is True
        # All cells should be filled
        assert all(board[i][j] != 0 for i in range(9) for j in range(9))

    def test_fill_board_valid_sudoku(self):
        """Test that filled board is valid Sudoku."""
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        # Check rows
        for row in board:
            assert len(set(row)) == 9  # All unique
            assert all(1 <= cell <= 9 for cell in row)
        
        # Check columns
        for col in range(9):
            column = [board[row][col] for row in range(9)]
            assert len(set(column)) == 9
            assert all(1 <= cell <= 9 for cell in column)
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row * 3 + i][box_col * 3 + j])
                assert len(set(box)) == 9


class TestRemoveCells:
    """Test the remove_cells function."""

    def test_remove_cells_count(self):
        """Test that correct number of cells remain."""
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        clues = 35
        sudoku_logic.remove_cells(board, clues)
        
        # Count filled cells
        filled_count = sum(1 for row in board for cell in row if cell != 0)
        assert filled_count == clues

    def test_remove_cells_leaves_empty_cells(self):
        """Test that remove_cells leaves empty cells."""
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        sudoku_logic.remove_cells(board, 20)
        
        # Some cells should be empty
        empty_count = sum(1 for row in board for cell in row if cell == 0)
        assert empty_count > 0


class TestGeneratePuzzle:
    """Test the generate_puzzle function."""

    def test_generate_puzzle_returns_two_boards(self):
        """Test that generate_puzzle returns puzzle and solution."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        assert puzzle is not None
        assert solution is not None
        assert len(puzzle) == 9
        assert len(solution) == 9

    def test_generate_puzzle_with_clues(self):
        """Test generate_puzzle with custom clues parameter."""
        clues = 25
        puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == clues

    def test_generate_puzzle_solution_complete(self):
        """Test that generated solution is complete."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        # Solution should have no empty cells
        assert all(solution[i][j] != 0 for i in range(9) for j in range(9))

    def test_generate_puzzle_puzzle_has_empty_cells(self):
        """Test that generated puzzle has empty cells."""
        puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
        
        empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
        assert empty_count > 0

    def test_generate_puzzle_puzzle_matches_solution_clues(self):
        """Test that puzzle cells match solution cells."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    assert puzzle[i][j] == solution[i][j]

    def test_generate_puzzle_default_clues(self):
        """Test generate_puzzle with default clues."""
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        # Default is 35 clues
        assert filled_count == 35


class TestSudokuConstants:
    """Test module constants."""

    def test_size_constant(self):
        """Test SIZE constant."""
        assert sudoku_logic.SIZE == 9

    def test_empty_constant(self):
        """Test EMPTY constant."""
        assert sudoku_logic.EMPTY == 0
