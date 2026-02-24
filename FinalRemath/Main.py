import tkinter as tk
from tkinter import ttk, messagebox
import random

main = tk.Tk()
main.title("Remath")
main.geometry("615x750")
main.resizable(False, False)

# ---------------- Notebook ----------------
nb = ttk.Notebook(main)
fr, fr2, fr3 = ttk.Frame(nb), ttk.Frame(nb), ttk.Frame(nb)
nb.add(fr, text="Rules")
nb.add(fr2, text="Play Game")
nb.add(fr3, text="Credits")
nb.pack(fill='both', expand=True)

# Assets
rulebg = tk.PhotoImage(file="Assets/Image/Rule.png")
gamebg = tk.PhotoImage(file="Assets/Image/Gamebg.png")
creditbg = tk.PhotoImage(file="Assets/Image/Credit.png")

canvas1 = tk.Canvas(fr, width=615, height=750, highlightthickness=0)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=rulebg, anchor="nw")

canvas2 = tk.Canvas(fr2, width=615, height=750, highlightthickness=0)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, image=gamebg, anchor="nw")

canvas3 = tk.Canvas(fr3, width=615, height=750, highlightthickness=0)
canvas3.pack(fill="both", expand=True)
canvas3.create_image(0, 0, image=creditbg, anchor="nw")

# ---------------- GAME DATA ----------------
ShapeExample = ["rectangle","oval","triangle","circle",
                "diamond","pentagon","hexagon",
                "star","heart","parallelogram"]

colors = ["red","blue","green","yellow","pink","orange",
          "purple","brown","black","white","gray","cyan",
          "magenta","lime","navy","teal","maroon","olive",
          "gold","silver","beige","coral","turquoise",
          "violet","indigo","lavender","salmon","khaki"]

Question_List = []
Res_Question_List = []
Shape_List = []

SHAPE_SIZE = 100
streak = 0
current_id = 0
time_left = 10.0
recall_index = 0

# ---------------- TRANSPARENT SCORE & TIMER ----------------
score_text = canvas2.create_text(
    265, 50,
    text="Score: 0",
    font=("Tahoma", 16, "bold"),
    fill="white"
)

timer_text = canvas2.create_text(
    490, 50,
    text="0.0s",
    font=("Tahoma", 22, "bold"),
    fill="white"
)

def update_score():
    canvas2.itemconfig(score_text, text=f"Score: {streak}")

def update_timer(text, color="white"):
    canvas2.itemconfig(timer_text, text=text, fill=color)

# ---------------- TIMER ----------------
def start_countdown(next_phase_func):
    global time_left
    if time_left > 0:
        time_left -= 0.1
        update_timer(f"{time_left:.1f}s")
        main.after(100, lambda: start_countdown(next_phase_func))
    else:
        update_timer("0.0s", "red")
        next_phase_func()

# ---------------- QUESTION GENERATION ----------------
def shapeQuestionsGen():
    global current_id

    shape_type = random.choice(ShapeExample)
    color = random.choice(colors)
    operator = random.choice(["-","*"])
    a = random.randint(-5,20)
    b = random.randint(-5,20)

    if operator == "*":
        correct_answer = a*b
    else:
        correct_answer = a-b

    question_text = f"{a} {operator} {b} = ?"

    Shape_List.append([shape_type,color,current_id])
    Question_List.append([question_text,correct_answer,current_id])
    current_id += 1

# ---------------- MEMORIZE PHASE ----------------
def memorize_phase():
    global time_left
    canvas2.delete("shape","question","ui")

    new_shape = Shape_List[-1]
    new_ques = Question_List[-1]

    x,y = 275,250

    draw_shape_logic(new_shape[0],new_shape[1],x,y)

    canvas2.create_text(307,180,
                        text=new_ques[0],
                        font=("Tahoma",28,"bold"),
                        fill="white",
                        tags="question")

    time_left = 7.0
    update_timer("", "white")
    start_countdown(recall_phase_init)

# ---------------- RECALL PHASE ----------------
def recall_phase_init():
    global Res_Question_List, recall_index
    canvas2.delete("shape", "question")
    
    # Take the whole history and scramble it
    Res_Question_List = list(Question_List)
    random.shuffle(Res_Question_List)
    
    recall_index = 0
    show_next_recall_shape()

def show_next_recall_shape():
    global recall_index, time_left
    canvas2.delete("shape","question")
    order_number = recall_index + 1
    if recall_index < len(Res_Question_List):

        q_id = Res_Question_List[recall_index][2]
        
        for s in Shape_List:
            if s[2] == q_id:
                draw_shape_logic(s[0],s[1],275,250)
        
        canvas2.create_text(
            325, 200,
            text=f"Shape #{order_number}!",
            font=("Arial", 16, "bold"),
            fill="red",
            tags="question"
        )
        
        recall_index += 1
        time_left = 2.0
        start_countdown(show_next_recall_shape)
    else:
        answer_phase_ui()

# ---------------- ANSWER PHASE ----------------
def answer_phase_ui():
    update_timer("GO!","green")

    global answer_box
    answer_box = tk.Entry(fr2,font=("Arial",14),justify="center")
    canvas2.create_window(307,600,window=answer_box,width=300,tags="ui")
    answer_box.focus_set()

    submit_btn = tk.Button(fr2,text="CONFIRM",
                           command=answer_check)
    canvas2.create_window(307,650,window=submit_btn,tags="ui")

def answer_check():
    global streak
    try:
        user_input = answer_box.get()
        player_answers = list(map(int, user_input.split()))
        correct_answers = [q[1] for q in Res_Question_List]

        if player_answers == correct_answers:
            streak += 1
            update_score()
            messagebox.showinfo("Success!", "Correct! Get ready for the next one.")
            start_game()
        else:
            game_over()
    except:
        messagebox.showerror("Error","Enter numbers separated by spaces.")

# ---------------- SHAPE DRAW ----------------
def draw_shape_logic(stype, scolor, x, y):
    size = SHAPE_SIZE

    if stype == "rectangle":
        canvas2.create_rectangle(
            x, y, x + size, y + size,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "oval" or stype == "circle":
        canvas2.create_oval(
            x, y, x + size, y + size,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "triangle":
        canvas2.create_polygon(
            x + size/2, y,
            x, y + size,
            x + size, y + size,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "diamond":
        canvas2.create_polygon(
            x + size/2, y,
            x, y + size/2,
            x + size/2, y + size,
            x + size, y + size/2,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "pentagon":
        canvas2.create_polygon(
            x + size/2, y,
            x, y + size/3,
            x + size/4, y + size,
            x + 3*size/4, y + size,
            x + size, y + size/3,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "hexagon":
        canvas2.create_polygon(
            x + size/4, y,
            x + 3*size/4, y,
            x + size, y + size/2,
            x + 3*size/4, y + size,
            x + size/4, y + size,
            x, y + size/2,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "star":
        canvas2.create_polygon(
            x + size/2, y,
            x + size*0.6, y + size*0.35,
            x + size, y + size*0.35,
            x + size*0.68, y + size*0.57,
            x + size*0.8, y + size,
            x + size/2, y + size*0.75,
            x + size*0.2, y + size,
            x + size*0.32, y + size*0.57,
            x, y + size*0.35,
            x + size*0.4, y + size*0.35,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

    elif stype == "heart":
        canvas2.create_polygon(
            x + size/2, y + size,
            x, y + size/2,
            x + size/4, y + size/4,
            x + size/2, y + size/2,
            x + 3*size/4, y + size/4,
            x + size, y + size/2,
            fill=scolor,
            outline="black",
            width=2,
            smooth=True,
            tags="shape"
        )

    elif stype == "parallelogram":
        canvas2.create_polygon(
            x + size/4, y,
            x + size, y,
            x + 3*size/4, y + size,
            x, y + size,
            fill=scolor,
            outline="black",
            width=2,
            tags="shape"
        )

# ---------------- GAME CONTROL ----------------
def start_game():
    shapeQuestionsGen()
    memorize_phase()

def game_over():
    global streak, Question_List, Shape_List, current_id
    messagebox.showerror("Game Over",
                         f"Final Streak: {streak}")
    streak = 0
    current_id = 0
    Question_List.clear()
    Shape_List.clear()
    update_score()
    canvas2.delete("shape","question","ui")
    

def btclick():
    if not Shape_List:
        start_game()

# ---------------- START BUTTON ----------------
def pixel_start_button(x,y):
    btn = canvas2.create_rectangle(x,y,x+120,y+50,
                                   fill="#ff9800",
                                   tags="startbtn")
    txt = canvas2.create_text(x+60,y+25,
                              text="▶ START",
                              fill="white",
                              font=("Courier",12,"bold"),
                              tags="startbtn")
    canvas2.tag_bind("startbtn","<Button-1>",
                     lambda e: btclick())

pixel_start_button(40,30)

main.mainloop()