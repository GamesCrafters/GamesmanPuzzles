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
        "animationType": "simpleSlidePlaceRemove"
    }

    if variant_id == '3_4':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 1.6] for i in range(12)]
    elif variant_id == '3_3':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 1.8] for i in range(9)]
    elif variant_id == '3_2':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 2.0] for i in range(9)]
    elif variant_id == '3_1':
        regularTheme["centers"] = [[0.5 + (i % 3), 0.2 * (i // 3) + 2.2] for i in range(9)]
    elif variant_id == '2_1':
        regularTheme["centers"] = [[1 + (i % 2), 0.2 * (i // 2) + 2.25] for i in range(9)]
    elif variant_id == '4_1':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 3.0] for i in range(16)]
    elif variant_id == '4_2':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.8] for i in range(16)]
    elif variant_id == '4_3':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.6] for i in range(16)]
    elif variant_id == '4_4':
        regularTheme["centers"] = [[0.5 + (i % 4), 0.2 * (i // 4) + 2.4] for i in range(16)]
    else:
        return None
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": regularTheme
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
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }

def get_nqueens(variant_id):
    if variant_id == '4':
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [4, 4],
                    "centers": [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)],
                    "background": "nqueens/grid.svg",
                    "entities": {
                        "q": {"image": "chess/Q.svg", "scale": 1}
                    }
                }
            }
        }
    return None

def get_rushhour(variant_id):
    pieces = {
        "L": "left", "m": "horizontal", "R": "right", "T": "top",
        "M": "vertical", "B": "bottom", "1": "left_red", "2": "right_red"
    }
    centers = [[i % 6 + 0.5, i // 6 + 0.5] for i in range(36)] + [[6.5, 2.5], [7.5, 2.5]]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [8, 6],
                "centers": centers,
                "background": "rushhour/grid.svg",
                "entities": {
                    p: {"image": f"rushhour/{pieces[p]}.svg", "scale": 1} for p in pieces
                },
                "arrowWidth": 0.1,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "multipleSlides"
            }
        }
    }

"""
===== STEP 2 ===== 
Add your function to the image_autogui_data_funcs dict in alphabetical order by puzzle_id.
"""

image_autogui_data_funcs = {
    "hanoi": get_hanoi,
    "npuzzle": get_npuzzle,
    "nqueens": get_nqueens,
    "rushhour": get_rushhour
}

def get_image_autogui_data(puzzle_id, variant_id):
    if puzzle_id in image_autogui_data_funcs:
        return image_autogui_data_funcs[puzzle_id](variant_id)
    return None