""" Contains some random classes and functions for exploration """

import os, json
import plotly.graph_objects as go
from plotly import subplots
from random import randint

COLOR_MAP = {0: [0, 0, 0], 
             1: [255, 0, 0],
             2: [0, 255, 0],
             3: [0, 0, 255],
             4: [255, 255, 0],
             5: [255, 0, 255],
             6: [0, 255, 255],
             7: [255, 150, 0],
             8: [150, 0, 255],
             9: [127, 127, 127],
             
             -1: [255, 255, 255]
             }

def load_training_set():
    """ loads and returns the training set """
    folder_training = "repo/data/training/"
    problems = {} # <name>: <problem>
    for file in os.listdir(folder_training):
        problem = json.loads(open(folder_training+file).read())
        problems[file.split('.')[0]] = problem
    Problem._problems = problems
    return problems

class Visualizer:
    def _convert_grid_to_image(grid):
        new_grid = []
        for y in grid:
            new_grid.append([])
            for x in y:
                new_grid[-1].append(COLOR_MAP[x])
        return new_grid

    def plot_example(input_grid, output_grid=None, name=""):
        """ plots a specific example of a problem """
        fig = subplots.make_subplots(rows=1, cols=2)

        inp = Visualizer._convert_grid_to_image(input_grid)
        fig.add_trace(go.Image(z=inp), 1, 1)
        
        if output_grid != None:
            out = Visualizer._convert_grid_to_image(output_grid)
            fig.add_trace(go.Image(z=out), 1, 2)

        fig.update_layout(height=400, )
        if name != "": print(name)
        fig.show()
        
    def plot_problem(problems, key):
        """ plots the problem """
        problem = problems[key]
        print(f"Example: {key}")
        for i in range(len(problem['train'])):
            Visualizer.plot_example(
                problem['train'][i]['input'], problem['train'][i]['output'], 
                str(i))
        for i in range(len(problem['test'])):
            Visualizer.plot_example(
                problem['test'][i]['input'], problem['test'][i]['output'], 
                f'TEST {i} ------------------')
    
    def plot_objects(objects, title=""):
        fig = subplots.make_subplots(rows=len(objects), cols=1)

        for i in range(len(objects)):
            object = objects[i]
            w = 30
            h = 30
            grid = empty_grid(w, h, -1)
            for pixel in object:
                grid[pixel[1]][pixel[0]] = pixel[2]['color']
            grid = crop_grid(grid)
            img = Visualizer._convert_grid_to_image(grid)
            fig.add_trace(go.Image(z=img), i+1, 1)
        if title != "": print(title)
        fig.update_layout(height=300*len(objects), )
        fig.show()






class Problem:
    _problems = None
    def __init__(self, key, pick_random=False) -> None:
        if pick_random: 
            key = list(Problem._problems.keys())[randint(0, len(Problem._problems)-1)]
        self.key = key
        self.problem = Problem._problems[key]

        self.num_examples = len(self.problem['train'])
        self.num_tests = len(self.problem['test'])

        
    def get_inputs(self, get_examples=True):
        """ get_examples=True => examples, else tests """
        if get_examples:
            return [ex['input'] for ex in self.problem['train']]
        return [test['input'] for test in self.problem['test']]
    
    def get_outputs(self, get_examples=True):
        """ get_examples=True => examples, else tests """
        if get_examples:
            return [ex['output'] for ex in self.problem['train']]
        return [test['output'] for test in self.problem['test']]
        

def empty_grid(x, y, fill_value=None):
    return [[fill_value for _ in range(x)] for _ in range(y)]

def crop_grid(grid, crop_color=-1):
    """ crops to smaller grid if the external color is only crop_color
    """
    while True: # cropping first column
        flag = False
        if len(grid) == 0: break
        for y in range(len(grid)):
            if grid[y][0] != crop_color:
                flag = True; break
        if flag: break
        for y in range(len(grid)):
            grid[y] = grid[y][1:]
    while True: # cropping last column
        flag = False
        if len(grid) == 0: break
        for y in range(len(grid)):
            if grid[y][-1] != crop_color:
                flag = True; break
        if flag: break
        for y in range(len(grid)):
            grid[y] = grid[y][:-1]
    while True: # cropping first row
        if len(grid) == 0: break
        if set(grid[0]) == set([crop_color]):
            grid.pop(0)
        else: break
    while True:
        if len(grid) == 0: break
        if set(grid[-1]) == set([crop_color]):
            grid.pop(-1)
        else: break
    return grid

            
    

def get_w(grid):
    return len(grid[0])
def get_h(grid):
    return len(grid)

def can_go(grid, x, y):
    try:
        el = grid[y][x]
        return True
    except: pass
    return False

def get_objects_by_color(grid):
    """ generates list of objects defined by adjacent colors """
    def traverse(x, y, obj:list):
        obj.append((x, y, {"color": grid[y][x]}))
        covered[y][x] = True
        for xop in [1, 0, -1]:
            for yop in [1, 0, -1]:
                if xop == 0 and yop == 0: continue
                if can_go(grid, x+xop, y+yop) \
                    and grid[y][x] == grid[y+yop][x+xop] \
                        and not covered[y+yop][x+xop]:
                            traverse(x+xop, y+yop, obj)
    
    covered = empty_grid(get_w(grid), get_h(grid), False)
    objects = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if covered[y][x]: continue
            obj = []
            traverse(x, y, obj)
            objects.append(obj)
    
    return objects
        


