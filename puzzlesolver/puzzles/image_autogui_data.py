"""
===== STEP 1 ===== 
Create a function that returns Image AutoGUI Data for your puzzle, given a variant of that puzzle.
Return None if there is no Image AutoGUI Data for the given variant.

get_<puzzle>(variant_id) should return JSON of the following form:

    {
        "defaultTheme": <name of default theme>,
        "themes": {
            <name of theme1>: {
                "space": [<width>, <height>],
                "centers": [ [<x0>,<y0>], [<x1>, <y1>], [<x2>, <y2>], [<x3>, <y3>], ... ],
                "background": <optional, path to background image>,
                "foreground": <optional, path to foreground image>,
                "entities": {
                    <char1>: {"image": <path to entity image>, "scale": <image scale>},
                    <char2>: { ... }
                    ...
                },
                "circleButtonRadius: <optional, radius of all default circle move buttons>,
                "lineWidth": <optional, width of all line move buttons>,
                "arrowWidth": <optional, width of all arrow move buttons>,
                "entitiesOverArrows": <optional, Boolean, whether entities are drawn over arrows>,
                "sounds": <optional> {
                    <char1>: <string, path to sound file>,
                    <char2>:
                }
                "animationType": <optional, string, animation type>,
                "defaultAnimationWindow": [start, end] <optional>
            },
            <name of theme2>: {
                ...
            },
            ...
        }
    }

(Scroll all the way down for Step 2).

"""

def get_bishop(variant_id):
    if variant_id in ["4x5_8", "4x7_4", "6x7_6"]:
        rows = int(variant_id[0])
        cols = int(variant_id[2])
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [cols, rows],
                    "centers": [[0.5 + i // rows, 0.5 + i % rows] for i in range(rows * cols)],
                    "background": f"bishop/{variant_id}.svg",
                    "entities": {
                        "X": {"image": "chess/wikipedia/B.svg", "scale": 1},
                        "O": {"image": "chess/wikipedia/bb.svg", "scale": 1},
                    },
                    "entitiesOverArrows": True,
                    "arrowWidth": 0.1,
                    "sounds": {"x": "general/slide.mp3"},
                    "animationType": "simpleSlides"
                }
            }
        }
    return None

def get_toadsandfrogspuzzle(variant_id):
    if variant_id.isdigit():
        board_length = int(variant_id) + 1
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [board_length, 3],
                    "centers": [[i + 0.5, 2] for i in range(board_length)],
                    "background": f"toadsandfrogs/pond{variant_id}.svg",
                    "entities": {
                        "x": {"image": "toadsandfrogs/bluefrog.svg", "scale": 0.9},
                        "o": {"image": "toadsandfrogs/redfrog.svg", "scale": 0.9},
                        "h": {"image": "general/basichitbox.svg", "scale": 0.9}
                    },
                    "sounds": {"x": "animals/frog.mp3"},
                    "animationType": "simpleSlides"
                }
            }
        }
    return None

def get_hanoi(variant_id):
    if not (len(variant_id) == 3 and variant_id[0].isdigit() and variant_id[-1].isdigit()):
        return None
    num_poles = int(variant_id[0])
    num_disks = int(variant_id[-1])
    alpha = "ABCDEFGHIJK"
    pieces = {
        alpha[c]: {"image": f"hanoi/{alpha[c]}.svg", "scale": 1} for c in range(num_disks)
    }

    regularTheme = {
        "space": [3, 3] if num_poles <= 3 else [4, 4],
        "background": f"hanoi/{num_poles}_{num_disks}_variant_grid.svg",
        "entities": pieces,
        "arrowWidth": 0.06 if num_poles <= 3 else 0.08,
        "sounds": {"x": "general/slideThenRemove.mp3"},
        "animationType": "simpleSlides",
    }

    if variant_id == '3_4':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 1.605] for i in range(12)]
    elif variant_id == '3_3':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 1.805] for i in range(9)]
    elif variant_id == '3_2':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 2.005] for i in range(9)]
    elif variant_id == '3_1':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 2.205] for i in range(9)]
    elif variant_id == '2_1':
        regularTheme["centers"] = [[1 + (i % 2), 0.2 * (i // 2) + 2.25] for i in range(9)]
    elif variant_id == '4_1':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.98] for i in range(16)]
    elif variant_id == '4_2':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.78] for i in range(16)]
    elif variant_id == '4_3':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.58] for i in range(16)]
    elif variant_id == '4_4':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.38] for i in range(16)]
    else:
        return None
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": regularTheme
        }
    }

def get_lightsout(variant_id):
    if variant_id not in "2345678":
        return None
    
    sideLength = int(variant_id)
    sL2 = sideLength * sideLength

    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [sideLength, sideLength],
                "centers": [[i % sideLength + 0.5, i // sideLength + 0.5] for i in range(sL2)],
                "background": "lightsout/background.svg",
                "entities": {
                    c: {"image": f"lightsout/{c}.svg", "scale": 1} for c in "01t"
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }
    
def get_npuzzle(variant_id):
    if variant_id not in ("2", "3"):
        return None
    
    sideLength = int(variant_id)
    sL2 = sideLength * sideLength

    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [sideLength, sideLength],
                "centers": [[i % sideLength + 0.5, i // sideLength + 0.5] for i in range(sL2)],
                "entities": {
                    str(n): {"image": f"npuzzle/{n}.svg", "scale": 1} for n in range(1, sL2)
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_nqueens(variant_id):
    if variant_id.isdigit():
        N = int(variant_id)
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [N, N],
                    "centers": [[i % N + 0.5, i // N + 0.5] for i in range(N * N)],
                    "background": f"nqueens/grid{N}.svg",
                    "entities": {
                        "Q": {"image": "chess/wikipedia/Q.svg", "scale": 1},
                        "h": {"image": "general/basichitbox.svg", "scale": 1}
                    },
                    "sounds": {"x": "general/remove.mp3"},
                    "animationType": "entityFade"
                }
            }
        }
    return None

def get_pegsolitaire(variant_id):
    scale = 18
    arrowWidth = 2
    ctrs = []
    if variant_id == 'triangle':
        ctrs = [[50, 12.2398], [40.15, 29.3005], [59.85, 29.3005], [30.3, 46.3612], [50, 46.3612], [69.7, 46.3612], [20.45, 63.4219], [40.15, 63.4219], [59.85, 63.4219], [79.55, 63.4219], [10.6, 80.4826], [30.3, 80.4826], [50, 80.4826], [69.7, 80.4826], [89.4, 80.4826]]
    elif variant_id == 'star':
        ctrs = [[50, 12.2398], [20.45, 29.3005], [40.15, 29.3005], [59.85, 29.3005], [79.55, 29.3005], [30.3, 46.3612], [50, 46.3612], [69.7, 46.3612], [20.45, 63.4219], [40.15, 63.4219], [59.85, 63.4219], [79.55, 63.4219], [50, 80.4826]]
    elif variant_id == 'trapezoid':
        ctrs = [[28.7857, 29.1562], [42.9286, 29.1562], [57.0714, 29.1562], [71.2143, 29.1562], [21.7143, 41.4043], [35.8571, 41.4043], [50.0, 41.4043], [64.1429, 41.4043], [78.2857, 41.4043], [14.6429, 53.6523], [28.7857, 53.6523], [42.9286, 53.6523], [57.0714, 53.6523], [71.2143, 53.6523], [85.3571, 53.6523], [7.5714, 65.9004], [21.7143, 65.9004], [35.8571, 65.9004], [50.0, 65.9004], [64.1429, 65.9004], [78.2857, 65.9004], [92.4286, 65.9004]]
        scale = 13
        arrowWidth = 1.25
    # elif variant_id == 'cross':
    #     ctrs = [[35.8571, 7.5714], [50.0, 7.5714], [64.1429, 7.5714], [35.8571, 21.7143], [50.0, 21.7143], [64.1429, 21.7143], [7.5714, 35.8571], [21.7143, 35.8571], [35.8571, 35.8571], [50.0, 35.8571], [64.1429, 35.8571], [78.2857, 35.8571], [92.4286, 35.8571], [7.5714, 50.0], [21.7143, 50.0], [35.8571, 50.0], [50.0, 50.0], [64.1429, 50.0], [78.2857, 50.0], [92.4286, 50.0], [7.5714, 64.1429], [21.7143, 64.1429], [35.8571, 64.1429], [50.0, 64.1429], [64.1429, 64.1429], [78.2857, 64.1429], [92.4286, 64.1429], [35.8571, 78.2857], [50.0, 78.2857], [64.1429, 78.2857], [35.8571, 92.4286], [50.0, 92.4286], [64.1429, 92.4286]]
    #     scale = 6.5
    #     arrowWidth = 1.25
    else:
        return None
    return {
        'defaultTheme': 'regular',
        'themes': {
            "regular": {
                'space': [100, 100],
                'background': f'pegsolitaire/{variant_id}.svg',
                'centers': ctrs,
                'entities': {c: {'image': 'general/brownpiece.svg', 'scale': scale} for c in 'abcd'},
                'arrowWidth': arrowWidth,
                'sounds': {'x': 'general/slideThenRemove.mp3'},
                'animationType': 'simpleSlides'
            },
        }
    }

def get_rubiks(variant_id):
    # Color Centers
    centers = [
        [38.75, 41.25], [38.75, 31.25], [46.25, 43.75], [46.25, 33.75],
        [8.75, 28.75], [16.25, 26.5], [8.75, 18.75], [16.25, 16.5],
        [42.5, 25], [50, 22.5], [50, 27.5], [57.5, 25],
        [53.75, 33.75], [61.25, 31.25], [53.75, 43.75], [61.25, 41.25],
        [83.75, 16.5], [83.75, 26.5], [91.25, 18.75], [91.25, 28.75],
        [50, 67.5], [42.5, 70], [57.5, 70], [50, 72.5]
    ]

    # Arrow Endpoints
    centers += [
        [48.5,53.5],[33.5,48.5], [1,17],[1,33], [33.5,21.5],[48.5,16.5], [69, 27],[69, 43],
        [96.5,11.5],[81.5,6.5], [51.5,78.5],[66.5,73.5], [31, 27],[31, 43], [3.5,11.5],[18.5,6.5],
        [66.5,21.5],[51.5,16.5], [51.5,53.5],[66.5,48.5], [99,17],[99,33], [48.5,78.5],[33.5,73.5],
    ]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": centers,
                "foreground": "rubiks/fg.svg",
                "entities": {
                    c: {"image": f"rubiks/{c}.svg", "scale": 100} for c in 'abcdefghijklmnopqr'
                },
                "arrowWidth": 1,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_rushhour(variant_id):
    pieces = {
        "L": "left", "m": "horizontal", "R": "right", "T": "top",
        "M": "vertical", "B": "bottom", "1": "left_red", "2": "right_red"
    }
    scale, st = 12.375, 6.6875
    centers = [[st + i % 6 * scale, st + i // 6 * scale] for i in range(36)]
    centers += [[81.4375, 31.4375], [93.8125, 31.4375]] # Location of car when it escapes grid
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": centers,
                "background": "rushhour/grid.svg",
                "entities": {
                    p: {"image": f"rushhour/{pieces[p]}.svg", "scale": scale * 1.05} for p in pieces
                },
                "arrowWidth": 1,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

"""
===== STEP 2 ===== 
Add your function to the image_autogui_data_funcs dict in alphabetical order by puzzle_id.
"""

image_autogui_data_funcs = {
    "bishop": get_bishop,
    "hanoi": get_hanoi,
    "lights": get_lightsout,
    "npuzzle": get_npuzzle,
    "nqueens": get_nqueens,
    "pegsolitaire": get_pegsolitaire,
    "toadsandfrogspuzzle": get_toadsandfrogspuzzle,
    "rubiks": get_rubiks,
    "rushhour": get_rushhour
}

def get_image_autogui_data(puzzle_id, variant_id):
    if puzzle_id in image_autogui_data_funcs:
        return image_autogui_data_funcs[puzzle_id](variant_id)
    return None