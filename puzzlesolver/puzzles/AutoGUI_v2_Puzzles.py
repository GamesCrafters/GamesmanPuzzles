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

def getRushHour(variant_id):
    return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [8, 6],
                    "backgroundImage": "rushhour/grid.svg",
                    "arrowWidth": 0.1,
                    "centers": [[0.5 + (i % 6), 0.5 + (i // 6)] for i in range(36)] + [[6.5, 2.5], [7.5, 2.5]],
                    "pieces": {
                        "L": {
                            "image": "rushhour/left.svg",
                            "scale": 1
                        },
                        "m": {
                            "image": "rushhour/horizontal.svg",
                            "scale": 1
                        },
                        "R": {
                            "image": "rushhour/right.svg",
                            "scale": 1
                        },
                        "T": {
                            "image": "rushhour/top.svg",
                            "scale": 1
                        },
                        "M": {
                            "image": "rushhour/vertical.svg",
                            "scale": 1
                        },
                        "B": {
                            "image": "rushhour/bottom.svg",
                            "scale": 1
                        },
                        "1": {
                            "image": "rushhour/left_red.svg",
                            "scale": 1
                        },
                        "2": {
                            "image": "rushhour/right_red.svg",
                            "scale": 1
                        }
                    }
                }
            }
        }

autoGUIv2DataFuncs = {
    "nqueens": getNQueens,
    "hanoi": getHanoi,
    "rushhour": getRushHour
}

def get_autoguiV2Data(puzzle_id, variant_id):
    if puzzle_id in autoGUIv2DataFuncs:
        return autoGUIv2DataFuncs[puzzle_id](variant_id)
    return None