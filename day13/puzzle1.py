
class Machine:
    def __init__(self):
        self.a = None
        self.b = None
        self.prize = None

    def set_a(self, x: int, y: int):
        self.a = (x, y)

    def set_b(self, x: int, y: int):
        self.b = (x, y)

    def set_prize(self, x: int, y: int):
        self.prize = (x, y)

    def is_complete(self) -> bool:
        return self.a is not None and self.b is not None and self.prize is not None

    def __repr__(self):
        return f"Machine(A={self.a}, B={self.b}, Prize={self.prize})"

class Matrix_2x2:
    def __init__(self, v1: float, v2: float, v3: float, v4: float):
        self.data = [
            [v1, v2],
            [v3, v4]
        ]

    def det(self) -> float:
        return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

    def inverse(self):
        det = self.det()
        if det == 0:
            return None

        return Matrix_2x2(
            self.data[1][1] / det, -self.data[0][1] / det,
            -self.data[1][0] / det, self.data[0][0] / det
        )

    def mul(self, other):
        if isinstance(other, tuple):
            return (self.data[0][0] * other[0] + self.data[0][1] * other[1], self.data[1][0] * other[0] + self.data[1][1] * other[1])
        else:
            raise Exception("Not required for now")
    
    def __repr__(self):
        return f"Matrix_2x2({self.data[0]}, {self.data[1]})"

def read_input(file: str) -> list:
    # Read the file
    f = open(file, "r")
    lines = f.readlines()

    machines = []
    current_machine = None

    for line in lines:
        cleaned_line = line.strip()

        # Commit the current machine
        if cleaned_line == "":
            if current_machine is not None:
                if current_machine.is_complete():
                    machines.append(current_machine)
                    current_machine = None
                else:
                    print("Machine is incomplete", current_machine)

            continue

        # Start a new machine if required
        if current_machine is None:
            current_machine = Machine()

        if cleaned_line.startswith("Button "):
            is_btn_a = cleaned_line.startswith("Button A:")
            assert is_btn_a or cleaned_line.startswith("Button B:")

            str_x, str_y = cleaned_line.split(": ")[1].split(", ")
            x = int(str_x[2:]) # Remove the "X+" part
            y = int(str_y[2:]) # Remove the "Y+" part
            
            if is_btn_a:
                current_machine.set_a(x, y)
            else:
                current_machine.set_b(x, y)
        elif cleaned_line.startswith("Prize"):
            str_x, str_y = cleaned_line.split(": ")[1].split(", ")
            x = int(str_x[2:]) # Remove the "X=" part
            y = int(str_y[2:]) # Remove the "Y=" part

            current_machine.set_prize(x, y)
        else:
            raise Exception("Invalid line")

    if current_machine is not None and current_machine.is_complete():
        machines.append(current_machine)

    return machines

def solve_machine(machine: Machine) -> tuple:
    # This problem can be solved by finding the intersection of the two lines using matrices
    # Hence, AX = B where A is the matrix of the two lines, X is the intersection point and B is the vector of the two lines
    # The solution is X = A^-1 * B

    A_inv = Matrix_2x2(machine.a[0], machine.b[0], machine.a[1], machine.b[1]).inverse()
    if A_inv is None:
        return None
    solution = A_inv.mul(machine.prize)

    # Make sure that the solution doesn't envolve pressing the button over 100 times and isn't negative
    if solution[0] < 0 or solution[1] < 0 or solution[0] > 100 or solution[1] > 100:
        return None

    # Make sure that the solution is an integer (keeping in mind that Python is very inaccurate with floats)
    if abs(solution[0] - round(solution[0])) > 0.0001 or abs(solution[1] - round(solution[1])) > 0.0001:
        return None
    else:
        return (round(solution[0]), round(solution[1]))

machines = read_input("input.txt")
solutions = [solve_machine(machine) for machine in machines]
token_count = sum([(3 * solution[0]) + (1 * solution[1]) for solution in solutions if solution is not None])
print("To win, you need", token_count, "tokens")
