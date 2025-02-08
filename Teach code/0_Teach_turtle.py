import turtle  # นำเข้าโมดูล turtle เพื่อใช้วาดกราฟิก

# สร้างหน้าต่างวาดรูป
screen = turtle.Screen()  
screen.title("Turtle Example")  # ตั้งชื่อหน้าต่าง อาจไม่ตั้งก็ได้

# สร้างตัวเต่า (ตัวชี้วาด)
t = turtle.Turtle()  

# วาดสี่เหลี่ยมจัตุรัส
for _ in range(4):  # ทำซ้ำ 4 รอบ
    t.forward(100)  # เดินหน้าตรงไป 100 หน่วย
    t.right(90)     # หมุนขวา 90 องศา
    
# print(t.heading()) # ดูองศาว่าตอนนี้อยู่องศาเท่าไหร่
# t.forward(100)
# t.right(90)
# print(t.heading())
# t.forward(150)
# t.left(44)
# print(t.heading())
# t.forward(50)

# ปิดหน้าต่างเมื่อคลิก
screen.exitonclick()