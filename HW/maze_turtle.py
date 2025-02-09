import turtle  # ใช้สำหรับการวาดเขาวงกตและการเคลื่อนที่ของเต่า
import time  # ใช้หน่วงเวลาในการเคลื่อนที่ของเต่า

# สัญลักษณ์ที่ใช้ในเขาวงกต
PART_OF_PATH = 'O'  # สัญลักษณ์สำหรับเส้นทางที่ถูกต้อง
TRIED = '.'         # สัญลักษณ์สำหรับจุดที่กำลังสำรวจ
OBSTACLE = '+'      # สัญลักษณ์สำหรับสิ่งกีดขวาง
DEAD_END = '-'      # สัญลักษณ์สำหรับเส้นทางตัน

class Maze:
    def __init__(self, maze_file_name):
        """โหลดเขาวงกตจากไฟล์และตั้งค่าต่าง ๆ"""
        self.maze_list = []  # รายการสองมิติสำหรับเก็บโครงสร้างเขาวงกต
        maze_file = open(f'HW/{maze_file_name}', 'r')  # เปิดไฟล์เขาวงกต
        rows_in_maze = 0  # ตัวนับจำนวนแถวของเขาวงกต
        
        # อ่านไฟล์ทีละบรรทัดเพื่อสร้างโครงสร้างเขาวงกต
        for line in maze_file:
            row_list = []  # สร้างรายการสำหรับแต่ละแถว
            for ch in line.strip():  # ลบช่องว่างที่ปลายแต่ละบรรทัด
                row_list.append(ch)  # เพิ่มตัวอักษรลงในแถว
                if ch == 'S':  # หากพบจุดเริ่มต้น
                    self.start_row = rows_in_maze  # เก็บพิกัดแถวของจุดเริ่มต้น
                    self.start_col = len(row_list) - 1  # เก็บพิกัดคอลัมน์ของจุดเริ่มต้น
                if ch == 'E':  # หากพบจุดสิ้นสุด
                    self.end_row = rows_in_maze  # เก็บพิกัดแถวของจุดสิ้นสุด
                    self.end_col = len(row_list) - 1  # เก็บพิกัดคอลัมน์ของจุดสิ้นสุด
            self.maze_list.append(row_list)  # เพิ่มแถวที่อ่านลงใน maze_list
            rows_in_maze += 1  # เพิ่มตัวนับจำนวนแถว

        # กำหนดจำนวนแถวและคอลัมน์สูงสุดของเขาวงกต
        self.rows_in_maze = rows_in_maze
        self.columns_in_maze = max(len(row) for row in self.maze_list)
        
        # ตั้งค่า turtle และหน้าจอ
        self.t = turtle.Turtle()  # สร้างเต่า (turtle)
        self.t.shape('turtle')  # ตั้งค่าให้เต่ามีรูปร่างเป็นเต่า
        self.t.color("blue")  # กำหนดสีเต่าเป็นสีน้ำเงิน
        self.wn = turtle.Screen()  # สร้างหน้าจอสำหรับแสดงผล
        # กำหนดขอบเขตของหน้าจอให้ตรงกับขนาดเขาวงกต
        self.wn.setworldcoordinates(-0.5, -self.rows_in_maze + 0.5, self.columns_in_maze - 0.5, 0.5)
        self.wn.bgcolor("lightblue")  # ตั้งค่าพื้นหลังของหน้าจอเป็นสีฟ้าอ่อน

    def draw_maze(self):
        """วาดเขาวงกตบนหน้าจอ"""
        self.t.speed(0)  # ตั้งความเร็วของเต่าเป็นเร็วสุด
        self.t.penup()  # ยกปากกาเพื่อไม่ให้เต่าวาดเส้นขณะเคลื่อนที่
        for y in range(self.rows_in_maze):  # วนลูปตามจำนวนแถว
            for x in range(len(self.maze_list[y])):  # วนลูปตามคอลัมน์ในแต่ละแถว
                if self.maze_list[y][x] == OBSTACLE:  # หากเป็นสิ่งกีดขวาง
                    self.draw_square(x, y, 'orange')  # วาดสี่เหลี่ยมสีส้ม
                elif self.maze_list[y][x] == 'E':  # หากเป็นจุดสิ้นสุด
                    self.draw_square(x, y, 'green')  # วาดสี่เหลี่ยมสีเขียว
        self.t.speed(0)  # ตั้งความเร็วของเต่าเป็นปกติ

    def draw_square(self, x, y, color):
        """วาดสี่เหลี่ยมที่ตำแหน่ง (x, y) ด้วยสีที่กำหนด"""
        self.t.up()  # ยกปากกา
        self.t.goto(x - 0.5, -y - 0.5)  # ย้ายไปที่มุมซ้ายบนของสี่เหลี่ยม
        self.t.color(color)  # ตั้งค่าสีเส้นขอบ
        self.t.fillcolor(color)  # ตั้งค่าสีภายในสี่เหลี่ยม
        self.t.setheading(90)  # ตั้งมุมมองของเต่าให้ชี้ขึ้น
        self.t.down()  # วางปากกา
        self.t.begin_fill()  # เริ่มต้นการเติมสี
        for _ in range(4):  # วาดสี่เหลี่ยม
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()  # สิ้นสุดการเติมสี
        self.t.up()  # ยกปากกา

    def move_turtle(self, x, y):
        """ย้ายเต่าไปยังตำแหน่ง (x, y)"""
        self.t.setheading(self.t.towards(x, -y))  # ตั้งทิศทางของเต่าไปยังตำแหน่งใหม่
        self.t.goto(x, -y)  # ย้ายเต่าไปยังตำแหน่งใหม่

    def update_position(self, row, col, val=None):
        """อัปเดตตำแหน่งของเต่าและ mark จุดในเขาวงกตด้วยสีต่าง ๆ"""
        if val:
            self.maze_list[row][col] = val  # อัปเดตค่าในรายการ maze_list
        self.move_turtle(col, row)  # ย้ายเต่าไปยังตำแหน่งใหม่
        if val == PART_OF_PATH:  # หากเป็นเส้นทางที่ถูกต้อง
            color = 'green'
        elif val == TRIED:  # หากเป็นจุดที่กำลังสำรวจ
            color = 'black'
        elif val == DEAD_END:  # หากเป็นทางตัน
            color = 'red'
        else:
            color = None
        if color:
            self.t.dot(10, color)  # วาดจุดที่ตำแหน่งนั้นด้วยสีที่กำหนด

    def dfs(self, row, col):
        """ใช้ DFS (Depth-First Search) เพื่อค้นหาเส้นทางออกจากเขาวงกต"""
        if row < 0 or row >= self.rows_in_maze or col < 0 or col >= self.columns_in_maze:
            return False  # หากอยู่นอกขอบเขตของเขาวงกต
        if self.maze_list[row][col] in (OBSTACLE, TRIED, DEAD_END):
            return False  # หากตำแหน่งเป็นสิ่งกีดขวางหรือเคยสำรวจแล้ว
        if (row, col) == (self.end_row, self.end_col):
            self.update_position(row, col, PART_OF_PATH)  # อัปเดตตำแหน่งสุดท้าย
            self.show_end_message()  # แสดงข้อความจบ
            return True  # พบทางออกแล้ว

        self.update_position(row, col, TRIED)  # อัปเดตตำแหน่งเป็น TRIED
        
        # สำรวจใน 4 ทิศทาง (ขวา, ล่าง, ซ้าย, ขึ้น)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if self.dfs(row + dr, col + dc):
                self.update_position(row, col, PART_OF_PATH)  # หากพบทางออก mark เป็นเส้นทาง
                return True

        self.update_position(row, col, DEAD_END)  # หากไม่พบทางออก mark เป็นทางตัน
        return False

    def show_end_message(self):
        """แสดงข้อความเมื่อพบทางออกและหยุดเต่า"""
        self.t.penup()
        self.t.goto(self.columns_in_maze // 2, -self.rows_in_maze - 1)
        self.t.color("blue")
        self.t.write(">>>>> ยินดีด้วย! พบทางออกแล้ว! <<<<<", align="center", font=("Arial", 16, "bold"))
        self.t.hideturtle()  # ซ่อนเต่า
        self.wn.exitonclick()  # รอให้ผู้ใช้คลิกเพื่อปิดหน้าจอ

def main():
    """ฟังก์ชันหลัก: โหลดเขาวงกตและเริ่มค้นหาเส้นทาง"""
    my_maze = Maze('maze_1.txt')
    my_maze.draw_maze()
    found = my_maze.dfs(my_maze.start_row, my_maze.start_col)
    if not found:
        print("ไม่พบทางออกในเขาวงกตนี้!")
    else:
        print("การค้นหาเส้นทางเสร็จสมบูรณ์")

if __name__ == '__main__':
    main()
