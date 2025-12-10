import sys
from ortools.linear_solver import pywraplp

max_depth = 100

class Machine:
    power_on_combination = None

    def __init__(self, id: int, instruction_line: str):
        self.id = id
        parts = instruction_line.split()
        if parts[0].startswith('[') and parts[0].endswith(']'):
            self.lights_target = [c == '#' for c in parts[0][1:-1]]
        else:
            raise ValueError("Invalid format for lights")
        
        self.buttons = []
        for button_str in parts[1:-1]:
            if button_str.startswith('(') and button_str.endswith(')'):
                self.buttons.append([int(x) for x in button_str[1:-1].split(',')])
            else:
                raise ValueError("Invalid format for button")

        if parts[-1].startswith('{') and parts[-1].endswith('}'):
            self.joltage_target = [int(x) for x in parts[-1][1:-1].split(',')]
        else:
            raise ValueError("Invalid format for joltage")

        # Initialize current state to all lights off
        self.lights_state = [False] * len(self.lights_target)


    def lights_state_as_string(self) -> str:
        return ''.join('#' if light else '.' for light in self.lights_state)


    def duplicate(self):
        new_machine = Machine.__new__(Machine)
        new_machine.id = self.id
        new_machine.lights_target = self.lights_target[:]
        new_machine.lights_state = self.lights_state[:]
        new_machine.buttons = [btn[:] for btn in self.buttons]
        new_machine.joltage_target = self.joltage_target[:]
        return new_machine


    def press_button_to_power_on(self, button_index: int) -> bool:
        if button_index < 0 or button_index >= len(self.buttons):
            raise IndexError("Button index out of range")

        for light_index in self.buttons[button_index]:
            self.lights_state[light_index] = not self.lights_state[light_index]


    def set_power_on_combination(self, presses: list[int]):
        if self.power_on_combination is None or len(presses) < len(self.power_on_combination):
            self.power_on_combination = presses


def check_for_repeated_state(seen_states: dict, state: str, buttons_pressed: int) -> bool:
    if state in seen_states:
        if buttons_pressed >= seen_states[state]:
            return True  # State has been visited before

    seen_states[state] = buttons_pressed
    return False


def find_power_on_combination(seen_states: dict, original_machine: Machine, machine: Machine, buttons_so_far: list[int], button_to_press: int):    
    if len(buttons_so_far) == max_depth:
        return None # Give up after reaching max depth
    elif original_machine.power_on_combination is not None and len(buttons_so_far) >= len(original_machine.power_on_combination):
        return None # No need to continue if we already have a better combination

    # This is the Jingleverse - clone before pressing anything
    new_machine = machine.duplicate()
    new_machine.press_button_to_power_on(button_to_press)

    if (new_machine.lights_state == new_machine.lights_target):
        original_machine.set_power_on_combination(buttons_so_far + [button_to_press])

    if not check_for_repeated_state(seen_states, new_machine.lights_state_as_string(), len(buttons_so_far) + 1):
        for button in range(len(machine.buttons)):
            find_power_on_combination(seen_states, original_machine, new_machine, buttons_so_far + [button_to_press], button)


with open(sys.argv[1], "r") as f:
    machines = []
    for idx, line in enumerate(f):
        machine = Machine(idx, line.strip())
        machines.append(machine)

minimum_jolatage_presses = 0
for machine in machines:
    seen_states = dict()
    print(f"Solving machine {machine.id + 1} out of {len(machines)}")
    for button in range(len(machine.buttons)):
        find_power_on_combination(seen_states, machine, machine, [], button)
    if machine.power_on_combination is None:
        raise ValueError(f"No power_on_combination found for machine {machine.id + 1}")

    # Part two is linear algebra
    # I had no idea how to do this, so thanks to 'yolocheezwhiz' for 'support'
    # https://github.com/yolocheezwhiz/adventofcode/blob/main/2025/day10.py
    # I had to learn what linear algebra was first
    lp_solver = pywraplp.Solver.CreateSolver('SCIP')
    button_variables = [lp_solver.IntVar(0, lp_solver.infinity(), f'machine_button_{i}') for i in range(len(machine.buttons))]

    # Add a constraint that the sum of all usable buttons must equal the target joltage
    for joltage_idx in range(len(machine.joltage_target)):
        usable_buttons = []
        for idx, button in enumerate(machine.buttons):
            if joltage_idx in button:
                usable_buttons.append(button_variables[idx])
        lp_solver.Add(sum(usable_buttons) == machine.joltage_target[joltage_idx])

    # Objective: minimize the total number of button presses
    lp_solver.Minimize(sum(button_variables))

    # And away we go!
    lp_solver.Solve()

    # Sum up the presses from each button
    minimum_jolatage_presses += int(sum(button.solution_value() for button in button_variables))

total_power_on_combination_presses = sum(len(machine.power_on_combination) for machine in machines)
print(f"Total power_on_combination presses: {total_power_on_combination_presses}")
print(f"Minimum joltage presses: {minimum_jolatage_presses}")
