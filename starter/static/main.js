// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let hintCells = new Set();
let currentDifficulty = 'medium';

// ===== DARK MODE FUNCTIONS =====

/**
 * Initialize dark mode based on localStorage preference
 * or system preference if not previously saved
 */
function initializeDarkMode() {
  const savedTheme = localStorage.getItem('sudokuTheme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // Use saved preference, or system preference, default to light mode
  const isDarkMode = savedTheme ? savedTheme === 'dark' : prefersDark;
  
  if (isDarkMode) {
    enableDarkMode();
  } else {
    disableDarkMode();
  }
}

/**
 * Enable dark mode by adding class to body
 */
function enableDarkMode() {
  document.body.classList.add('dark-mode');
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const themeIcon = themeToggle.querySelector('.theme-icon');
    if (themeIcon) {
      themeIcon.textContent = '☀️';
    }
    themeToggle.title = 'Switch to light mode';
  }
  localStorage.setItem('sudokuTheme', 'dark');
}

/**
 * Disable dark mode by removing class from body
 */
function disableDarkMode() {
  document.body.classList.remove('dark-mode');
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const themeIcon = themeToggle.querySelector('.theme-icon');
    if (themeIcon) {
      themeIcon.textContent = '🌙';
    }
    themeToggle.title = 'Switch to dark mode';
  }
  localStorage.setItem('sudokuTheme', 'light');
}

/**
 * Toggle between light and dark modes
 */
function toggleDarkMode() {
  if (document.body.classList.contains('dark-mode')) {
    disableDarkMode();
  } else {
    enableDarkMode();
  }
}

// ===== SCOREBOARD FUNCTIONS =====

/**
 * Save a score to localStorage
 * @param {string} name - Player name
 * @param {number} completionTime - Time in seconds
 * @param {string} difficulty - Game difficulty
 * @param {number} hintsUsed - Number of hints used
 */
function saveScore(name, completionTime, difficulty, hintsUsed) {
  const scores = JSON.parse(localStorage.getItem('sudokuScores')) || [];
  
  const newScore = {
    name: name || 'Anonymous',
    time: completionTime,
    difficulty: difficulty,
    hints: hintsUsed,
    timestamp: new Date().getTime()
  };
  
  scores.push(newScore);
  localStorage.setItem('sudokuScores', JSON.stringify(scores));
}

/**
 * Get top 10 scores sorted by completion time
 * @returns {Array} Array of top 10 scores
 */
function getTopScores() {
  const scores = JSON.parse(localStorage.getItem('sudokuScores')) || [];
  
  // Sort by time (ascending - fastest times first)
  return scores
    .sort((a, b) => a.time - b.time)
    .slice(0, 10);
}

/**
 * Display the scoreboard modal with top 10 scores
 */
function displayScoreboard() {
  const topScores = getTopScores();
  const tbody = document.getElementById('scores-tbody');
  tbody.innerHTML = '';
  
  if (topScores.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">No scores yet. Start playing to get on the scoreboard!</td></tr>';
  } else {
    topScores.forEach((score, index) => {
      const row = document.createElement('tr');
      const minutes = Math.floor(score.time / 60);
      const seconds = score.time % 60;
      const timeStr = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
      
      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${score.name}</td>
        <td>${timeStr}</td>
        <td>${score.difficulty.charAt(0).toUpperCase() + score.difficulty.slice(1)}</td>
        <td>${score.hints}</td>
      `;
      tbody.appendChild(row);
    });
  }
  
  document.getElementById('scoreboard-modal').style.display = 'flex';
}

/**
 * Show the congratulations modal and prompt for name
 */
function showCongratulationsModal() {
  const minutes = Math.floor(elapsedSeconds / 60);
  const seconds = elapsedSeconds % 60;
  const timeStr = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
  
  document.getElementById('final-time').innerText = timeStr;
  document.getElementById('player-name').value = '';
  document.getElementById('player-name').focus();
  document.getElementById('congratulations-modal').style.display = 'flex';
}

/**
 * Hide the congratulations modal
 */
function hideCongratulationsModal() {
  document.getElementById('congratulations-modal').style.display = 'none';
}

/**
 * Hide the scoreboard modal
 */
function hideScoreboardModal() {
  document.getElementById('scoreboard-modal').style.display = 'none';
}

// ===== END SCOREBOARD FUNCTIONS =====

// ===== END DARK MODE FUNCTIONS =====

/**
 * Validate a number against row, column, and 3x3 box
 * Returns array of conflicting cell indices
 */
function getConflictingCells(row, col, value) {
  if (!value) return []; // No conflicts for empty cells
  
  const conflicts = [];
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const size = 9;
  
  // Check row for conflicts
  for (let j = 0; j < size; j++) {
    if (j !== col) {
      const idx = row * size + j;
      const cell = inputs[idx];
      if (cell && cell.value === value) {
        conflicts.push(idx);
      }
    }
  }
  
  // Check column for conflicts
  for (let i = 0; i < size; i++) {
    if (i !== row) {
      const idx = i * size + col;
      const cell = inputs[idx];
      if (cell && cell.value === value) {
        conflicts.push(idx);
      }
    }
  }
  
  // Check 3x3 box for conflicts
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let i = boxRow; i < boxRow + 3; i++) {
    for (let j = boxCol; j < boxCol + 3; j++) {
      if (i !== row || j !== col) {
        const idx = i * size + j;
        const cell = inputs[idx];
        if (cell && cell.value === value) {
          conflicts.push(idx);
        }
      }
    }
  }
  
  return conflicts;
}

/**
 * Clear all conflict highlights from the board
 */
function clearConflictHighlights() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let input of inputs) {
    input.classList.remove('conflict');
  }
}

/**
 * Update conflict highlights for a specific cell and its conflicts
 */
function updateConflictHighlights(changedInput) {
  const row = parseInt(changedInput.dataset.row);
  const col = parseInt(changedInput.dataset.col);
  const value = changedInput.value;
  
  // Clear all existing conflict highlights
  clearConflictHighlights();
  
  if (value) {
    // Get conflicting cells
    const conflicts = getConflictingCells(row, col, value);
    
    // Apply conflict class to current cell if there are conflicts
    if (conflicts.length > 0) {
      changedInput.classList.add('conflict');
    }
    
    // Apply conflict class to all conflicting cells
    const boardDiv = document.getElementById('sudoku-board');
    const inputs = boardDiv.getElementsByTagName('input');
    for (let idx of conflicts) {
      inputs[idx].classList.add('conflict');
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    rowDiv.dataset.row = i;
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      
      // Apply alternate-block class using the formula to create a checkerboard pattern
      // of alternating 3x3 sub-grids
      if ((Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 0) {
        input.classList.add('alternate-block');
      }
      
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        
        // Update conflict highlights immediately
        updateConflictHighlights(e.target);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function startTimer() {
  if (timerInterval) clearInterval(timerInterval);
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds++;
    updateTimerDisplay();
  }, 1000);
}

function updateTimerDisplay() {
  const minutes = Math.floor(elapsedSeconds / 60);
  const seconds = elapsedSeconds % 60;
  const timerElement = document.getElementById('timer');
  timerElement.innerText = 
    String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  currentDifficulty = difficulty;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  hintCells.clear();
  hideCongratulationsModal();
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    // Remove incorrect class but preserve box class
    inp.classList.remove('incorrect', 'hint');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    stopTimer();
    // Show congratulations modal after a brief delay
    setTimeout(() => {
      showCongratulationsModal();
    }, 500);
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

function getCandidates(board, row, col) {
  if (board[row][col] !== 0) return [];
  const candidates = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  
  // Remove numbers in the same row
  for (let j = 0; j < SIZE; j++) {
    candidates.delete(board[row][j]);
  }
  
  // Remove numbers in the same column
  for (let i = 0; i < SIZE; i++) {
    candidates.delete(board[i][col]);
  }
  
  // Remove numbers in the same 3x3 box
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let i = boxRow; i < boxRow + 3; i++) {
    for (let j = boxCol; j < boxCol + 3; j++) {
      candidates.delete(board[i][j]);
    }
  }
  
  return Array.from(candidates);
}

function provideHint() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  
  // Build current board state
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  
  // Find all empty cells with candidates
  const emptyCellsWithCandidates = [];
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === 0 && !hintCells.has(i * SIZE + j)) {
        const candidates = getCandidates(board, i, j);
        if (candidates.length > 0) {
          emptyCellsWithCandidates.push({ row: i, col: j, candidates });
        }
      }
    }
  }
  
  if (emptyCellsWithCandidates.length === 0) {
    const msg = document.getElementById('message');
    msg.style.color = '#d32f2f';
    msg.innerText = 'No more hints available.';
    return;
  }
  
  // Pick a random empty cell and fill it with a random candidate
  const hintCell = emptyCellsWithCandidates[
    Math.floor(Math.random() * emptyCellsWithCandidates.length)
  ];
  const value = hintCell.candidates[
    Math.floor(Math.random() * hintCell.candidates.length)
  ];
  
  const idx = hintCell.row * SIZE + hintCell.col;
  const inp = inputs[idx];
  inp.value = value;
  inp.disabled = true;
  // Add hint class while preserving box class
  inp.classList.remove('incorrect');
  inp.classList.add('hint');
  hintCells.add(idx);
  
  const msg = document.getElementById('message');
  msg.style.color = '#388e3c';
  msg.innerText = 'Hint provided!';
}

// Wire buttons - wait for DOM to be fully loaded
window.addEventListener('load', () => {
  // Initialize dark mode
  initializeDarkMode();
  
  // Theme toggle button - with error handling
  const themeToggleBtn = document.getElementById('theme-toggle');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleDarkMode);
  } else {
    console.warn('Theme toggle button not found');
  }
  
  const newGameBtn = document.getElementById('new-game');
  if (newGameBtn) {
    newGameBtn.addEventListener('click', newGame);
  }
  
  const checkSolutionBtn = document.getElementById('check-solution');
  if (checkSolutionBtn) {
    checkSolutionBtn.addEventListener('click', checkSolution);
  }
  
  const hintBtn = document.getElementById('hint-button');
  if (hintBtn) {
    hintBtn.addEventListener('click', provideHint);
  }
  
  const viewScoresBtn = document.getElementById('view-scores');
  if (viewScoresBtn) {
    viewScoresBtn.addEventListener('click', displayScoreboard);
  }
  
  // Congratulations modal buttons
  const saveScoreBtn = document.getElementById('save-score-btn');
  if (saveScoreBtn) {
    saveScoreBtn.addEventListener('click', () => {
      const playerName = document.getElementById('player-name').value.trim();
      const hintsUsed = hintCells.size;
      
      if (!playerName) {
        alert('Please enter your name');
        return;
      }
      
      saveScore(playerName, elapsedSeconds, currentDifficulty, hintsUsed);
      hideCongratulationsModal();
      
      // Show a brief success message
      const msg = document.getElementById('message');
      msg.style.color = '#388e3c';
      msg.innerText = '✓ Score saved!';
    });
  }
  
  const skipScoreBtn = document.getElementById('skip-score-btn');
  if (skipScoreBtn) {
    skipScoreBtn.addEventListener('click', () => {
      hideCongratulationsModal();
    });
  }
  
  // Scoreboard modal button
  const closeScoreboardBtn = document.getElementById('close-scoreboard-btn');
  if (closeScoreboardBtn) {
    closeScoreboardBtn.addEventListener('click', hideScoreboardModal);
  }
  
  // Close modal when clicking outside the modal content
  const congratsModal = document.getElementById('congratulations-modal');
  if (congratsModal) {
    congratsModal.addEventListener('click', (e) => {
      if (e.target.id === 'congratulations-modal') {
        hideCongratulationsModal();
      }
    });
  }
  
  const scoreboardModal = document.getElementById('scoreboard-modal');
  if (scoreboardModal) {
    scoreboardModal.addEventListener('click', (e) => {
      if (e.target.id === 'scoreboard-modal') {
        hideScoreboardModal();
      }
    });
  }
  
  // initialize
  newGame();
});