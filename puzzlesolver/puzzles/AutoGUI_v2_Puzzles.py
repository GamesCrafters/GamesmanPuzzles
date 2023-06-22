def getNPuzzle(variant_id):
    if variant_id == '2':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [2, 2],
                        "centers": [[0.5 + (i % 2), 0.5 + (i // 2)] for i in range(4)],
                        "piecesOverArrows": True,
                        "pieces": {
                            "1": {
                                "image": "npuzzle/1.svg",
                                "scale": 1
                            },
                            "2": {
                                "image": "npuzzle/2.svg",
                                "scale": 1
                            },
                            "3": {
                                "image": "npuzzle/3.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    else:
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "centers": [[0.5 + (i % 3), 0.5 + (i // 3)] for i in range(9)],
                        "piecesOverArrows": True,
                        "pieces": {
                            "1": {
                                "image": "npuzzle/1.svg",
                                "scale": 1
                            },
                            "2": {
                                "image": "npuzzle/2.svg",
                                "scale": 1
                            },
                            "3": {
                                "image": "npuzzle/3.svg",
                                "scale": 1
                            },
                            "4": {
                                "image": "npuzzle/4.svg",
                                "scale": 1
                            },
                            "5": {
                                "image": "npuzzle/5.svg",
                                "scale": 1
                            },
                            "6": {
                                "image": "npuzzle/6.svg",
                                "scale": 1
                            },
                            "7": {
                                "image": "npuzzle/7.svg",
                                "scale": 1
                            },
                            "8": {
                                "image": "npuzzle/8.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }

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
    if variant_id == '3_4':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/3_4_variant_grid.svg",
                        "centers": [[0.5 + (i % 3), 0.2 * (i // 3) + 1.6] for i in range(12)],
                        "arrowWidth": 0.06,
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
                            },
                            "D": {
                                "image": "hanoi/D.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '3_3':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/3_3_variant_grid.svg",
                        "centers": [[0.5 + (i % 3), 0.2 * (i // 3) + 1.8] for i in range(9)],
                        "arrowWidth": 0.06,
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
    if variant_id == '3_2':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/3_2_variant_grid.svg",
                        "centers": [[0.5 + (i % 3), 0.2 * (i // 3) + 2.0] for i in range(9)],
                        "arrowWidth": 0.06,
                        "pieces": {
                            "A": {
                                "image": "hanoi/B.svg",
                                "scale": 1
                            },
                            "B": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '3_1':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/3_1_variant_grid.svg",
                        "centers": [[0.5 + (i % 3), 0.2 * (i // 3) + 2.2] for i in range(9)],
                        "arrowWidth": 0.06,
                        "pieces": {
                            "A": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '2_1':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [3, 3],
                        "backgroundImage": "hanoi/2_1_variant_grid.svg",
                        "centers": [[1 + (i % 2), 0.2 * (i // 2) + 2.25] for i in range(9)],
                        "arrowWidth": 0.06,
                        "pieces": {
                            "A": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '4_1':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [4, 4],
                        "backgroundImage": "hanoi/4_1_variant_grid.svg",
                        "centers": [[0.5 + (i % 4), 0.2 * (i // 4) + 3.0] for i in range(16)],
                        "arrowWidth": 0.08,
                        "pieces": {
                            "A": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '4_2':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [4, 4],
                        "backgroundImage": "hanoi/4_2_variant_grid.svg",
                        "centers": [[0.5 + (i % 4), 0.2 * (i // 4) + 2.8] for i in range(16)],
                        "arrowWidth": 0.08,
                        "pieces": {
                            "A": {
                                "image": "hanoi/B.svg",
                                "scale": 1
                            },
                            "B": {
                                "image": "hanoi/C.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }
    if variant_id == '4_3':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [4, 4],
                        "backgroundImage": "hanoi/4_3_variant_grid.svg",
                        "centers": [[0.5 + (i % 4), 0.2 * (i // 4) + 2.6] for i in range(16)],
                        "arrowWidth": 0.08,
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
    if variant_id == '4_4':
        return {
                "defaultTheme": "regular",
                "themes": {
                    "regular": {
                        "backgroundGeometry": [4, 4],
                        "backgroundImage": "hanoi/4_4_variant_grid.svg",
                        "centers": [[0.5 + (i % 4), 0.2 * (i // 4) + 2.4] for i in range(16)],
                        "arrowWidth": 0.08,
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
                            },
                            "D": {
                                "image": "hanoi/D.svg",
                                "scale": 1
                            }
                        }
                    }
                }
            }

autoGUIv2DataFuncs = {
    "nqueens": getNQueens,
    "hanoi": getHanoi,
    "npuzzle": getNPuzzle
}

def get_autoguiV2Data(puzzle_id, variant_id):
    if puzzle_id in autoGUIv2DataFuncs:
        return autoGUIv2DataFuncs[puzzle_id](variant_id)
    return None