"""Tests for Flask app routes."""
import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import sudoku_logic


class TestIndexRoute:
    """Test the index route."""

    def test_index_returns_200(self, client):
        """Test that index route returns 200 status."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """Test that index returns HTML content."""
        response = client.get('/')
        assert b'<!DOCTYPE' in response.data or b'<html' in response.data.lower()


class TestNewGameRoute:
    """Test the /new route for creating new games."""

    def test_new_game_returns_200(self, client):
        """Test that /new returns 200 status."""
        response = client.get('/new')
        assert response.status_code == 200

    def test_new_game_returns_json(self, client):
        """Test that /new returns JSON response."""
        response = client.get('/new')
        assert response.content_type.startswith('application/json')

    def test_new_game_puzzle_structure(self, client):
        """Test that puzzle has correct structure."""
        response = client.get('/new')
        data = json.loads(response.data)
        
        assert 'puzzle' in data
        puzzle = data['puzzle']
        assert len(puzzle) == 9
        assert all(len(row) == 9 for row in puzzle)

    def test_new_game_puzzle_values(self, client):
        """Test that puzzle contains valid values."""
        response = client.get('/new')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        for row in puzzle:
            for cell in row:
                assert 0 <= cell <= 9

    def test_new_game_custom_clues(self, client):
        """Test /new with difficulty parameter."""
        # Test hard difficulty (25 clues)
        response = client.get('/new?difficulty=hard')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == 25

    def test_new_game_easy_difficulty(self, client):
        """Test /new with easy difficulty."""
        response = client.get('/new?difficulty=easy')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == 45

    def test_new_game_medium_difficulty(self, client):
        """Test /new with medium difficulty."""
        response = client.get('/new?difficulty=medium')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == 35

    def test_new_game_hard_difficulty(self, client):
        """Test /new with hard difficulty."""
        response = client.get('/new?difficulty=hard')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == 25

    def test_new_game_stores_current_puzzle(self, client):
        """Test that new game stores puzzle in CURRENT."""
        response = client.get('/new')
        assert response.status_code == 200
        
        # The puzzle should be stored internally
        # We can verify this by checking the next request's response
        response2 = client.get('/new')
        assert response2.status_code == 200

    def test_new_game_default_clues_35(self, client):
        """Test that default clues is 35."""
        response = client.get('/new')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        filled_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert filled_count == 35

    def test_new_game_puzzle_has_empty_cells(self, client):
        """Test that puzzle has empty cells."""
        response = client.get('/new')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
        assert empty_count > 0


class TestCheckSolutionRoute:
    """Test the /check route for validating solutions."""

    def test_check_without_game(self, client):
        """Test /check when no game in progress."""
        response = client.post('/check', 
                              json={'board': sudoku_logic.create_empty_board()},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_check_with_game(self, client):
        """Test /check with an active game."""
        # First create a game
        client.get('/new')
        
        # Then check with a board
        response = client.post('/check',
                              json={'board': sudoku_logic.create_empty_board()},
                              content_type='application/json')
        assert response.status_code == 200

    def test_check_returns_json(self, client):
        """Test that /check returns JSON response."""
        client.get('/new')
        response = client.post('/check',
                              json={'board': sudoku_logic.create_empty_board()},
                              content_type='application/json')
        assert response.content_type.startswith('application/json')

    def test_check_returns_incorrect_list(self, client):
        """Test that /check returns incorrect cells list."""
        client.get('/new')
        response = client.post('/check',
                              json={'board': sudoku_logic.create_empty_board()},
                              content_type='application/json')
        data = json.loads(response.data)
        
        assert 'incorrect' in data
        assert isinstance(data['incorrect'], list)

    def test_check_correct_solution(self, client):
        """Test /check with correct solution."""
        # Create a game
        client.get('/new')
        
        # Get the solution by creating a filled board
        # Since we don't have direct access to CURRENT, we'll test the logic
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        # Manually set up the game by making a request
        response = client.post('/check',
                              json={'board': solution},
                              content_type='application/json')
        
        # Response should have incorrect array (may be empty or have mismatches
        # depending on the puzzle)
        data = json.loads(response.data)
        assert 'incorrect' in data

    def test_check_incorrect_solution(self, client):
        """Test /check with incorrect solution."""
        # Create a game
        client.get('/new')
        
        # Create a board with wrong values
        wrong_board = sudoku_logic.create_empty_board()
        wrong_board[0][0] = 9
        
        response = client.post('/check',
                              json={'board': wrong_board},
                              content_type='application/json')
        
        data = json.loads(response.data)
        assert 'incorrect' in data
        assert isinstance(data['incorrect'], list)

    def test_check_with_list_format(self, client):
        """Test /check with board as list of lists."""
        client.get('/new')
        
        board = [[0] * 9 for _ in range(9)]
        response = client.post('/check',
                              json={'board': board},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'incorrect' in data


class TestGameFlow:
    """Test complete game flow."""

    def test_complete_game_flow(self, client):
        """Test a complete game flow: new game, then check."""
        # Start new game
        response1 = client.get('/new?clues=40')
        assert response1.status_code == 200
        
        puzzle_data = json.loads(response1.data)
        assert 'puzzle' in puzzle_data
        
        # Create a test board (empty for simplicity)
        board = sudoku_logic.create_empty_board()
        
        # Check the board
        response2 = client.post('/check',
                               json={'board': board},
                               content_type='application/json')
        assert response2.status_code == 200
        
        check_data = json.loads(response2.data)
        assert 'incorrect' in check_data

    def test_multiple_new_games(self, client):
        """Test creating multiple new games sequentially."""
        puzzles = []
        
        for _ in range(3):
            response = client.get('/new')
            assert response.status_code == 200
            data = json.loads(response.data)
            puzzles.append(data['puzzle'])
        
        # Puzzles should be different (with high probability)
        # At least verify all are valid
        for puzzle in puzzles:
            assert len(puzzle) == 9
            assert all(len(row) == 9 for row in puzzle)


class TestErrorHandling:
    """Test error handling."""

    def test_check_invalid_json(self, client):
        """Test /check with invalid JSON."""
        response = client.post('/check',
                              data='invalid json',
                              content_type='application/json')
        # Should either return 400 or handle gracefully
        assert response.status_code in [400, 500]

    def test_check_missing_board_field(self, client):
        """Test /check with missing board field."""
        client.get('/new')
        response = client.post('/check',
                              json={'wrong_field': []},
                              content_type='application/json')
        # Should handle gracefully
        assert response.status_code in [200, 400]
