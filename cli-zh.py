# coding=UTF-8

import os, random, threading, time

try :
    with open(os.path.abspath("config.pyt"), encoding="utf-8") as config :
        exec(config.read())
except FileNotFoundError :
    with open(os.path.abspath("config.pyt"), "w", encoding="utf-8") as config :
        config.write("""# The config file of Flappy.

# Skin config start
roll_skin = "|"
p_skin = "O"
blank_skin = " "
v_border = ""
h_border = "-"
# Skin config end

# Gameplay config start
width = 79
height = 18
speed_v = 20
speed_h = 4
roll_range = 3
cooldown_tile = 16
high = 15
# Gameplay config end""")
    with open(os.path.abspath("config.pyt"), encoding="utf-8") as config :
        exec(config.read())

grav = 0
is_pausing = 0
score = 0
gameover = 0
spawned = 0
checkerboard = [0] * width

def add_fly() :
    global high, grav, is_pausing
    while not gameover :
        try :
            input()
            if is_pausing :
                is_pausing = 0
            else :
                grav = 0
                high += 1
                if type(speed_h) == type("") :
                    time.sleep(1.0/eval(speed_h)/4)
                else :
                    time.sleep(1.0/speed_h/4)
                high += 1
                if type(speed_h) == type("") :
                    time.sleep(1.0/eval(speed_h)/4)
                else :
                    time.sleep(1.0/speed_h/4)
                high += 1
        except (KeyboardInterrupt, EOFError) :
            pass
def ffall() :
    global high, grav
    while not gameover :
        try :
            if not is_pausing :
                if grav < 4 :
                    grav += 1
                if type(speed_h) == type("") :
                    time.sleep(1.0/eval(speed_h)/grav)
                else :
                    time.sleep(1.0/speed_h/grav)
                high -= 1
        except KeyboardInterrupt :
            pass
enter_key = threading.Thread(target=add_fly)
enter_key.setDaemon(True)
enter_key.start()
p_fall = threading.Thread(target=ffall)
p_fall.setDaemon(True)
p_fall.start()
start_time = time.time()

while not gameover :
    try :
        showc = (time.strftime("%Y-%m-%d %a %H:%M:%S")+" 游戏运行总时间: %f 纵向速度: %f 横向速度: %f 柱子范围: %d 分: %d") % (time.time()-start_time, eval(str(speed_v)), eval(str(speed_h)), eval(str(roll_range)), score)
        for i in range(height) :
            showc += "\n"
            if height - high == i :
                showc += p_skin
            for j in range(height-high==i, width) :
                if checkerboard[j] :
                    showc += (blank_skin, roll_skin)[i not in range(height-checkerboard[j]-eval(str(roll_range))+1, height-checkerboard[j]+eval(str(roll_range)))]
                else :
                    showc += blank_skin
            showc += v_border
        if h_border != "" :
            showc += "\n" + h_border * width
        os.system(("clear", "cls")[os.name=="nt"])
        print(showc)
        if type(speed_v) == type("") :
            time.sleep(1.0/eval(speed_v))
        else :
            time.sleep(1.0/speed_v)
        if spawned == 0 :
            checkerboard.append(random.choice((0,)*height*2+tuple(range(1, height+1))))
            if checkerboard[-1] :
                spawned = eval(str(cooldown_tile))
        else :
            checkerboard.append(0)
            spawned -= 1
        del checkerboard[0]
        if (checkerboard[0] != 0 and height-high not in range(height-checkerboard[0]-eval(str(roll_range))+1, height-checkerboard[0]+eval(str(roll_range)))) or high <= 0 :
            gameover = 1
        elif checkerboard[0] != 0 :
            score += 1
    except KeyboardInterrupt :
        is_pausing = 1
        print("已暂停,按下enter键继续,或再次按下Ctrl-C退出")
        try :
            while is_pausing :
                pass
        except KeyboardInterrupt :
            print("已退出")
            break

print("游戏结束!")
