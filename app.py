from flask import Flask, render_template, request
import math
import ast

app = Flask(__name__)

ALLOWED_NAMES = {
    "x": 0,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
}

ALLOWED_AST_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Call,
)


def safe_eval(expression, x_value):
    allowed = ALLOWED_NAMES.copy()
    allowed["x"] = x_value

    tree = ast.parse(expression, mode="eval")

    for node in ast.walk(tree):
        if type(node) not in ALLOWED_AST_NODES:
            raise ValueError("Expression contains unsupported or unsafe elements.")

        if isinstance(node, ast.Name):
            if node.id not in allowed:
                raise ValueError(f"Use of '{node.id}' is not allowed.")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in allowed:
                raise ValueError("Only allowed math functions can be used.")

    return eval(compile(tree, filename="<string>", mode="eval"), {"__builtins__": {}}, allowed)


def newton_raphson(function, derivative, x0, tolerance, max_iter):
    results = []
    x_current = x0

    for i in range(1, max_iter + 1):
        fx = safe_eval(function, x_current)
        dfx = safe_eval(derivative, x_current)

        if dfx == 0:
            raise ValueError("Derivative became zero. Method cannot continue.")

        x_next = x_current - (fx / dfx)
        error = abs(x_next - x_current)

        results.append({
            "iteration": i,
            "xn": round(x_current, 6),
            "fx": round(fx, 6),
            "dfx": round(dfx, 6),
            "x_next": round(x_next, 6),
            "error": round(error, 6)
        })

        if error < tolerance:
            return x_next, results

        x_current = x_next

    return x_current, results


@app.route("/", methods=["GET", "POST"])
def index():
    root = None
    results = []
    error = None

    if request.method == "POST":
        try:
            function = request.form.get("function", "")
            derivative = request.form.get("derivative", "")
            x0 = float(request.form.get("x0", 0))
            tolerance = float(request.form.get("tolerance", 0.0001))
            max_iter = int(request.form.get("max_iter", 20))

            root, results = newton_raphson(
                function, derivative, x0, tolerance, max_iter
            )

            root = round(root, 6)

        except Exception as e:
            error = str(e)

    return render_template(
    "index.html",
    root=root,
    results=results,
    error=error,
    values={
        "function": "x**3 - x - 2",
        "derivative": "3*x**2 - 1",
        "x0": "1.5",
        "tolerance": "0.0001",
        "max_iter": "20"
    }
)

if __name__ == "__main__":
    app.run(debug=True)