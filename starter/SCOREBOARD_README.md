# Sudoku Game - Top 10 Scoreboard Feature

## Overview
The scoreboard system uses vanilla JavaScript and the browser's `localStorage` to track and display the top 10 fastest puzzle completion times. When a player successfully completes a puzzle, they are prompted to save their score with their name.

## Features

### 1. **Congratulations Modal**
When a player successfully solves a puzzle:
- A celebratory modal appears showing the completion time
- Player is prompted to enter their name
- Options to "Save Score" or "Skip"
- Modal automatically disappears on completion or skip

### 2. **Score Storage**
Each score saved to localStorage includes:
- **Name**: Player's name (required, up to 30 characters)
- **Time**: Completion time in seconds
- **Difficulty**: Game difficulty level (easy, medium, hard)
- **Hints**: Number of hints used during the game
- **Timestamp**: When the score was recorded (UTC milliseconds)

### 3. **Scoreboard Display**
A "View Scores" button displays the top 10 scores in a modal with:
- Rank (1-10)
- Player Name
- Completion Time (formatted as MM:SS)
- Difficulty Level
- Number of Hints Used
- Scores sorted by fastest time
- Special highlighting for top 3 positions (gold, silver, bronze)

## Implementation Details

### JavaScript Functions

#### `saveScore(name, completionTime, difficulty, hintsUsed)`
Saves a new score to localStorage.
```javascript
// Example usage:
saveScore("John", 245, "medium", 3);
// Saves: {name: "John", time: 245, difficulty: "medium", hints: 3, timestamp: ...}
```

#### `getTopScores()`
Returns an array of the top 10 scores, sorted by fastest completion time.
```javascript
const topScores = getTopScores();
// Returns array of up to 10 score objects, sorted by time (ascending)
```

#### `displayScoreboard()`
Shows the scoreboard modal with all top 10 scores formatted in a table.
```javascript
displayScoreboard(); // Displays the scoreboard modal
```

#### `showCongratulationsModal()`
Displays the congratulations modal after puzzle completion.

#### `hideCongratulationsModal()`
Hides the congratulations modal.

#### `hideScoreboardModal()`
Hides the scoreboard modal.

### HTML Elements Added
- **Congratulations Modal**: `#congratulations-modal`
  - Player name input field
  - Save and Skip buttons
  
- **Scoreboard Modal**: `#scoreboard-modal`
  - Scores table with headers
  - Top 10 scores display
  - Close button

- **View Scores Button**: `#view-scores`
  - Opens the scoreboard modal

### CSS Styling
- Modal animations with slide-in effect
- Responsive table layout for scoreboard
- Special color highlighting for top 3 ranks
- Hover effects on table rows
- Mobile-friendly design

## Game Flow

1. **Player starts a new game**
   - Timer begins
   - Difficulty and hints tracker are initialized

2. **Player completes puzzle**
   - Clicks "Check Solution"
   - Puzzle is validated
   - If correct:
     - Success message displays
     - Timer stops
     - Congratulations modal appears

3. **Player enters name and saves score**
   - Enters their name (required)
   - Clicks "Save Score"
   - Score saved to localStorage
   - Modal closes with confirmation message

4. **Player views scoreboard**
   - Clicks "View Scores" button
   - Scoreboard modal opens
   - Top 10 scores displayed sorted by time

## localStorage Data Structure

```json
{
  "sudokuScores": [
    {
      "name": "Alice",
      "time": 185,
      "difficulty": "hard",
      "hints": 0,
      "timestamp": 1693526400000
    },
    {
      "name": "Bob",
      "time": 245,
      "difficulty": "medium",
      "hints": 3,
      "timestamp": 1693526500000
    }
  ]
}
```

## Browser Compatibility
- Works with all modern browsers that support:
  - `localStorage` API
  - ES6 JavaScript features
  - CSS Flexbox and Animations

## Clear Scoreboard
To clear all scores from localStorage (for testing), open browser console and run:
```javascript
localStorage.removeItem('sudokuScores');
```

## Testing Checklist
- [x] Congratulations modal appears after solving puzzle
- [x] Player name input validation
- [x] Score saves to localStorage
- [x] Scoreboard displays top 10 scores
- [x] Scores sorted by fastest time
- [x] Modal animations working
- [x] Close button and outside-click modals functionality
- [x] Hints counter tracked correctly
- [x] Difficulty level captured with score

## Future Enhancement Ideas
- Add date/time display for each score
- Filter scores by difficulty level
- Delete individual scores
- Export/import scoreboard data
- Leaderboard reset with confirmation
- Score statistics (average time, total games, etc.)
