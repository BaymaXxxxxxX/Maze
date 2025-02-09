import turtle

t = turtle.Turtle()
# ตั้งค่าความเร็วในการวาด
t.speed(5)
# วาดสี่เหลี่ยมจัตุรัส
for _ in range(4):  # ทำซ้ำ
    t.forward(100)  # เดินหน้า
    t.right(90)  #ขวา

turtle.done()
