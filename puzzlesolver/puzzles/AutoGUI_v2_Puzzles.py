def getNQueens(variant_id):
    if variant_id == '4':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [4, 4],
                        "backgroundImage": "nqueens/grid.svg",
                        "centers": [[0.5 + (i % 4), 0.5 + (i // 4)] for i in range(16)],
                        "pieces": {
                            "q": {
                                "image": "chess/Q.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }

def getHanoi(variant_id):

    if variant_id == '3_3':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/3x3grid.svg",
                        "centers": [[0.5 + (i % 3), 0.5 + (i // 3)] for i in range(9)],
                        "pieces": {
                            "A": {
                                "image": "hanoi/A.svg",
                                "scale": 1
                            },
                            "B": {
                                "image": "hanoi/B.svg",
                                "scale": 1
                            },
                            "C": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }

autoGUIv2DataFuncs = {
    "nqueens": getNQueens,
    "hanoi": getHanoi
}

def get_autoguiV2Data(puzzle_id, variant_id):
    if puzzle_id in autoGUIv2DataFuncs:
        return autoGUIv2DataFuncs[puzzle_id](variant_id)
    return None