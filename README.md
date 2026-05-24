# Newton-Raphson Method Online Calculator

A Flask web application for the Newton-Raphson Method in Numerical Methods.

## Features
- Mathematical discussion
- Two worked examples
- Interactive Newton-Raphson calculator
- Iteration table
- Safe expression parsing using Python AST
- Responsive user interface

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

## Sample Input
Function: `x**3 - x - 2`  
Derivative: `3*x**2 - 1`  
Initial Guess: `1.5`  
Tolerance: `0.0001`  
Maximum Iterations: `20`
