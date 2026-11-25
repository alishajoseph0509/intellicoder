// script.js - SimpleWebCalculator core logic
(() => {
  const display = document.getElementById('display');
  let expr = '';

  const update = () => {
    display.value = expr || '0';
  };

  const clear = () => {
    expr = '';
    update();
  };

  const backspace = () => {
    expr = expr.slice(0, -1);
    update();
  };

  const evaluate = () => {
    if (!expr) return;
    try {
      // Replace any accidental multiple operators
      const sanitized = expr.replace(/[^0-9.+\-*/]/g, '');
      // eslint-disable-next-line no-new-func
      const result = Function(`'use strict';return (${sanitized})`)();
      expr = String(result);
    } catch {
      expr = 'Error';
    }
    update();
  };

  const handleInput = (char) => {
    if (char === 'C') return clear();
    if (char === '←') return backspace();
    if (char === '=') return evaluate();
    // Prevent multiple consecutive operators (except minus for negative)
    if (/[+\-*/]/.test(char) && /[+\-*/]$/.test(expr) && !(char === '-' && !/[+\-*/]$/.test(expr.slice(-2)))) {
      expr = expr.slice(0, -1);
    }
    expr += char;
    update();
  };

   // Button clicks
  document.querySelectorAll('.buttons button').forEach(btn => {
    btn.addEventListener('click', () => {
      const action = btn.dataset.action;
      if (action === 'clear') return handleInput('C');
      if (action === 'backspace') return handleInput('←');
      if (action === 'equals') return handleInput('=');
      handleInput(btn.dataset.value);
    });
  });

  // Keyboard support
  document.addEventListener('keydown', e => {
    const key = e.key;
    if (/\d/.test(key) || key === '.' || /[+\-*/]/.test(key)) {
      handleInput(key);
    } else if (key === 'Enter' || key === '=') {
      handleInput('=');
    } else if (key === 'Backspace') {
      handleInput('←');
    } else if (key === 'Escape') {
      handleInput('C');
    }
  });

  // Initialize display
  update();
})();