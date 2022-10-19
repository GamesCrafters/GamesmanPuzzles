def getNQueens(variant_id):
    if variant_id not in (4,):
        return None
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

autoGUIv2DataFuncs = {
    "nqueens": getNQueens
}

def get_autoguiV2Data(puzzle_id, variant_id):
    if puzzle_id in autoGUIv2DataFuncs:
        return autoGUIv2DataFuncs[puzzle_id](variant_id)
    return None