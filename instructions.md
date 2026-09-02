# GitHub Copilot Instructions for Sudoku Refactoring Project

## Project Context
I am refactoring a legacy Python Flask Sudoku game into a modern, responsive web application. The application will include a difficulty selector, a timer, live input feedback, a hint system, and a top 10 scoreboard stored in local storage.

## Technology Stack
* Backend: Python, Flask
* Frontend: HTML, CSS, JavaScript (Vanilla)
* Testing: pytest

## Coding Guidelines & Style
* **Modularity:** Break down monolithic functions into smaller, reusable, and testable components.
* **Error Handling:** Include consistent and robust error handling on both the frontend and backend.
* **Comments & Documentation:** Provide clear, concise comments explaining the "why" behind complex Sudoku logic (e.g., backtracking algorithms, board generation).
* **Modern Standards:** Use modern Python practices (e.g., type hinting where appropriate) and ES6+ features for JavaScript.
* **Responsiveness:** Ensure UI components scale cleanly between desktop and mobile. Use CSS modules or plain CSS to style the 3x3 grids with alternating colors.
* **Accessibility:** Keep contrast and readability high for both Light and Dark modes.

## Interaction Rules
* When suggesting code, prioritize stability and ensure it does not break existing test cases.
* If a request is broad, break it down into smaller, iterative steps.
* Explain the logic behind complex Sudoku algorithms (like ensuring a unique solvable solution) before writing the code.