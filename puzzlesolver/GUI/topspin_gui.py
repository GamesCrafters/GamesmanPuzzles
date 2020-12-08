import tkinter as tk
from ..puzzles import TopSpin
from ..solvers import SqliteSolver
from ..util import *


GAME_AREA = ((50,200),(500,500))

class TsGUI(tk.Frame):
    def __init__(self, master = None, game = TopSpin(), width = 950, height = 600, title = 'TopSpin GUI', color = 'white'):
        super().__init__(master)
        self.master = master
        self.color = color
        self.height = height
        self.width = width
        self.game = game
        self.solver = SqliteSolver
        self.bestmove_display = False

        self.canvas = tk.Canvas(master, width = width, height = height, background = color)
        self.write_intro()
        self.coords = self.def_coords()
        self.draw_spinner()
        self.draw_line()
        self.draw_background()
        self.draw_track()
        self.restart_btn()
        self.quit_btn()
        self.hide_btn()
        self.best_move_btn()
        self.canvas.pack()

        self.master.bind('<Key>',self.controls)
        self.master.title(title)
        self.pack()

    def write_intro(self):
        text = "To play {}, use the right arrow key to move the beads clockwise by 1, the left arrow key to move the beads counterclockwise by 1, and hit 'return' to flip the beads. Here is the description of the puzzle: {} This puzzle is created by {}.".format(self.game.puzzle_name, self.game.description, self.game.author)
        self.canvas.create_text(75,20, text = text, width = 500, anchor = 'nw')
        info = "Primitive: " + self.game.primitive() + '\n' + "Remoteness: " + str(self.solver(self.game).getRemoteness(self.game))
        self.canvas.create_text(680,100, text = info , width = 500, anchor = 'nw', tag = 'info')
    
    def def_coords(self, r = 40):
        top_num = self.game.spin + 1
        bottom_num = self.game.size - top_num 
        width = GAME_AREA[1][0] - GAME_AREA[0][0]
        height = GAME_AREA[1][1] - GAME_AREA[0][1]
        pos = []
        for i in range(1, top_num):
            pos.append((r + width//top_num*i, GAME_AREA[0][1]))
        pos.append((GAME_AREA[1][0]- r, GAME_AREA[0][1] + height//2))
        for j in range(1, bottom_num)[::-1]:
            pos.append((r + width//bottom_num*j, GAME_AREA[1][1]))
        pos.append((GAME_AREA[0][0]+r, GAME_AREA[0][1] + height//2))
        return pos

    def draw_background(self, r = 40):
        for item in self.coords:
            x0 = item[0] - r
            y0 = item[1] - r
            x1 = item[0] + r
            y1 = item[1] + r
            self.canvas.create_oval(x0, y0, x1,y1, fill = "black")

    def draw_track(self):
        for i in range(self.game.size):
            self.canvas.create_text(self.coords[i][0], self.coords[i][1], 
                                    text = self.game.loop[i], 
                                    font= ('Arial',24), 
                                    fill = "white", 
                                    tag = "num")

    def draw_line(self):
        self.canvas.create_line(650,0,650,600, width = 2)
    
    def draw_spinner(self, r = 40):
        x0 = self.coords[0][0] - r - r//2
        y0 = GAME_AREA[0][1] - r - r//2
        x1 = self.coords[self.game.spin-1][0] + r + r//2
        y1 = self.coords[self.game.spin-1][1] + r + r//2
        self.canvas.create_rectangle(x0,y0,x1,y1, fill = 'grey')

    def restart_btn(self):
        restart = tk.Button(self.master, text = 'Restart', command = self.restart_game,height=2, width = 10)
        self.canvas.create_window(680,300,window =restart,anchor='nw')

    def quit_btn(self):
        quitbtn = tk.Button(self.master, text = 'Quit Game', command = self.master.destroy, height = 2, width = 10)
        self.canvas.create_window(680, 400, window = quitbtn, anchor = 'nw')

    def best_move_btn(self):
        bm_btn = tk.Button(self.master, text = "Show Best Move", command = self.show_best_move, height = 2, width = 15)
        self.canvas.create_window(680,200, window= bm_btn, anchor = 'nw')

    def hide_btn(self):
        hide = tk.Button(self.master, text = 'hide', command = self.hide_best_move, height = 2, width = 5)
        self.canvas.create_window(870, 200, window = hide, anchor = 'nw')


    def restart_game(self):
        self.canvas.delete("num")
        self.game = TopSpin()
        self.draw_track()
        self.run_solver()

    def controls(self, event):
        if event.keysym == 'Right':
            self.game = self.game.doMove((1,'clockwise'))
        elif event.keysym == 'Left':
            self.game = self.game.doMove((5,'clockwise'))
        elif event.keysym == 'Return':
            self.game = self.game.doMove(('flip'))
        self.canvas.delete('num')
        self.draw_track()
        self.run_solver()

    def run_solver(self):
        puzzle_val = self.game.primitive()
        remoteness = self.solver(self.game).getRemoteness(self.game)
        info = "Primitive: " + puzzle_val + '\n' +"Remoteness: " + str(remoteness) + '\n'
        self.canvas.delete('info')
        self.canvas.create_text(680,100, text = info, width = 500, anchor = 'nw',tag='info')
        if self.bestmove_display:
            self.canvas.delete('bm_info')
            self.show_best_move()

    def best_move(self):
        if self.solver(self.game).getValue(self.game) == PuzzleValue.UNSOLVABLE: return None
        if self.game.primitive() == PuzzleValue.SOLVABLE: return None
        remotes = {
            self.solver(self.game).getRemoteness(self.game.doMove(move)) : move 
            for move in self.game.generateMoves(movetype="legal")
        }
        if PuzzleValue.UNSOLVABLE in remotes:
            del remotes[PuzzleValue.UNSOLVABLE]
        return remotes[min(remotes.keys())]

    def transate_best_move(self):
        bestmove = self.best_move()
        if bestmove:
            if len(bestmove) == 2:
                return '{} --> first slot in spinner'.format(self.game.loop[self.game.size - bestmove[0]])
            else:
                return 'flip'
        else:
            return 'You solved it!'

    def show_best_move(self):
        bm_info = self.transate_best_move()
        self.bestmove_display = True
        self.canvas.create_text(680,250, text = bm_info, width = 500, anchor = 'nw',tag='bm_info')
        self.hide_btn()

    def hide_best_move(self):
        self.canvas.delete('bm_info')
        self.bestmove_display = False

root = tk.Tk()
app = TsGUI(master=root)
app.mainloop()
    
    
