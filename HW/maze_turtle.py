import turtle
from tkinter import Tk, Toplevel, Canvas, Button
import time

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'

class Maze:
    def __init__(self, maze_file_name):
        self.maze_file_name = maze_file_name
        self.load_maze()

    def load_maze(self):
        self.maze_list = []
        maze_file = open(f'HW/{self.maze_file_name}', 'r')
        rows_in_maze = 0

        for line in maze_file:
            row_list = []
            for ch in line.strip():
                row_list.append(ch)
                if ch == 'S':
                    self.start_row = rows_in_maze
                    self.start_col = len(row_list) - 1
                if ch == 'E':
                    self.end_row = rows_in_maze
                    self.end_col = len(row_list) - 1
            self.maze_list.append(row_list)
            rows_in_maze += 1

        self.rows_in_maze = rows_in_maze
        self.columns_in_maze = max(len(row) for row in self.maze_list)
        
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.t.color("blue")
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-0.5, -self.rows_in_maze + 0.5, self.columns_in_maze - 0.5, 0.5)
        self.wn.bgcolor("lightblue")

    def draw_maze(self):
        self.t.speed(0)
        self.t.penup()
        for y in range(self.rows_in_maze):
            for x in range(len(self.maze_list[y])):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_square(x, y, 'black')
                elif self.maze_list[y][x] == 'E':
                    self.draw_square(x, y, 'green')
        self.t.speed(0)

    def draw_square(self, x, y, color):
        self.t.up()
        self.t.goto(x - 0.5, -y - 0.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()
        self.t.up()

    def move_turtle(self, x, y):
        self.t.setheading(self.t.towards(x, -y))
        self.t.goto(x, -y)

    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)
        if val == PART_OF_PATH:
            color = 'green'
        elif val == TRIED:
            color = 'gray'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None
        if color:
            self.t.dot(10, color)

    def dfs(self, row, col):
        if row < 0 or row >= self.rows_in_maze or col < 0 or col >= self.columns_in_maze:
            return False
        if self.maze_list[row][col] in (OBSTACLE, TRIED, DEAD_END):
            return False
        if (row, col) == (self.end_row, self.end_col):
            self.update_position(row, col, PART_OF_PATH)
            self.show_end_message(True)
            return True

        self.update_position(row, col, TRIED)
        
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if self.dfs(row + dr, col + dc):
                self.update_position(row, col, PART_OF_PATH)
                return True

        self.update_position(row, col, DEAD_END)
        return False

    def show_end_message(self, success):
        """แสดงป๊อปอัป UI พร้อมปุ่มลองใหม่และปุ่มปิดโปรแกรม"""
        root = Tk()
        root.withdraw()
        
        popup = Toplevel(root)
        popup.title("ผลลัพธ์")
        popup.geometry("400x250")
        popup.configure(bg="#f5f5f5")

        canvas = Canvas(popup, width=400, height=200, bg="#f5f5f5", highlightthickness=0)
        canvas.pack()

        message = "🎉 ยินดีด้วย! พบทางออกแล้ว! 🎉" if success else "❌ ไม่พบทางออกในเขาวงกตนี้! ❌"
        text_id = canvas.create_text(200, 80, text=message, font=("Arial", 16, "bold"), fill="green" if success else "red")

        for _ in range(20):
            canvas.move(text_id, 0, -2)
            popup.update()
            time.sleep(0.05)

        # ปุ่มลองใหม่ (เพิ่มขนาดและปรับสีให้ชัดเจน)
        btn_retry = Button(popup, text="ลองใหม่อีกครั้ง", command=lambda: self.reload_maze(root, popup),
                          bg="#1E90FF", fg="black", font=("Arial", 16, "bold"), bd=5, relief="raised")
        btn_retry.place(x=40, y=150, width=150, height=50)

        # ปุ่มปิดโปรแกรม (เพิ่มขนาดและสีที่ตัดกัน)
        btn_close = Button(popup, text="ปิดโปรแกรม", command=lambda: self.close_program(root, popup),
                           bg="#FF6347", fg="black", font=("Arial", 16, "bold"), bd=5, relief="raised")
        btn_close.place(x=210, y=150, width=150, height=50)

        root.mainloop()

    def reload_maze(self, root, popup):
        """รีโหลดเขาวงกตใหม่และเริ่มต้นการค้นหาอีกครั้ง"""
        popup.destroy()
        root.destroy()
        self.t.clear()
        self.t.reset()
        self.load_maze()
        self.draw_maze()
        self.dfs(self.start_row, self.start_col)

    def close_program(self, root, popup):
        """ปิดหน้าต่าง Tkinter และหน้าจอ turtle"""
        popup.destroy()
        root.destroy()
        self.wn.bye()

def main():
    my_maze = Maze('maze_1.txt')
    my_maze.draw_maze()
    found = my_maze.dfs(my_maze.start_row, my_maze.start_col)
    if not found:
        my_maze.show_end_message(False)

if __name__ == '__main__':
    main()
