# SimpleWebCalculator

## Overview
SimpleWebCalculator is a lightweight, responsive web‑based calculator that performs basic arithmetic operations. It works on both desktop and mobile browsers and supports mouse clicks as well as keyboard input.

## Features
- **Operations:** addition, subtraction, multiplication, division  
- **Controls:** clear (C), backspace (←)  
- **Responsive UI:** adapts to various screen sizes  
- **Keyboard support:** type numbers, operators (`+ - * /`), `Enter` for =, `Esc` for clear, `Backspace` for delete  
- **Live display:** shows the current expression and the computed result  

## Setup
1. Clone or download the repository.  
2. Ensure you have a modern web browser (Chrome, Firefox, Edge, Safari).  
3. Open `index.html` directly in the browser – no server or build step is required.

```bash
# Example using git
git clone https://github.com/yourusername/SimpleWebCalculator.git
cd SimpleWebCalculator
open index.html   # macOS
# or double‑click index.html in Explorer/Finder
```

## Usage
- **Click** the buttons or **type** on the keyboard to build an expression.  
- Press **Enter** or click `=` to evaluate.  
- Press **Esc** or click `C` to clear the whole expression.  
- Press **Backspace** or click `←` to delete the last character.  

The display shows two rows:
1. **Expression** – the exact input string.  
2. **Result** – the evaluated value (or an error message for invalid input, e.g., division by zero).

## Project Structure
- `index.html` – HTML markup for the calculator UI.  
- `styles.css` – CSS for layout, styling, and responsive behavior.  
- `script.js` – JavaScript handling button clicks, keyboard events, and calculation logic.  

## License
This project is released under the MIT License. Feel free to use, modify, and distribute it.