# coding=utf-8
import os
import time
import sys


def tap(x, y):
    os.system('adb shell input tap {} {}'.format(x, y))


def sleep(sec):
    if sec < 1:
        print('sleep {}ms '.format(1000 * sec))
        time.sleep(sec)
    else:
        while sec != 0:
            sys.stdout.write('\rsleep {}m {}s '.format((int(sec / 60)), (sec % 60)))
            sys.stdout.flush()
            time.sleep(1)
            sec = sec - 1
        print('')


def up():
    print("up")
    os.system('adb shell input tap 540 870')


def down():
    print("down")
    os.system('adb shell input tap 540 1150')


def right():
    print("right")
    os.system('adb shell input tap 880 1000')


def left():
    print("left")
    os.system('adb shell input tap 200 1000')


def right_up():
    print("right up")
    os.system('adb shell input tap 900 880')


def btn1_1():
    os.system('adb shell input tap 200 1350')


def btn1_2():
    os.system('adb shell input tap 530 1350')


def btn1_3():
    os.system('adb shell input tap 860 1350')


def btn2_1():
    os.system('adb shell input tap 200 1460')


def btn2_2():
    os.system('adb shell input tap 530 1460')


def btn2_3():
    os.system('adb shell input tap 860 1460')


def into_checkpoint():
    print("enter the checkpoint")
    os.system('adb shell input tap 790 1470')
    sleep(2)


def dialog_btn_center():
    os.system('adb shell input tap 540 1000')


def dialog_btn_1():
    os.system('adb shell input tap 540 1000')


def dialog_btn_2():
    os.system('adb shell input tap 540 1100')


def dialog_btn_3():
    os.system('adb shell input tap 540 1200')


def dialog_btn_4():
    os.system('adb shell input tap 540 1300')


def dialog_btn_5():
    os.system('adb shell input tap 540 1400')


def full_screen_btn_1():
    os.system('adb shell input tap 530 1300')


def full_screen_btn_2():
    os.system('adb shell input tap 530 1450')


def end_fighting():
    print("leave fighting")
    os.system('adb shell input tap 600 1800')


def status_btn():
    os.system('adb shell input tap 78 270')


def leave_checkpoint():
    print("leave checkpoint")
    os.system('adb shell input tap 1000 280')
    os.system('adb shell input tap 550 1500')


def back_right():
    os.system('adb shell input tap 1000 280')


def back_left():
    os.system('adb shell input tap 60 270')


def reply_hp(times, is_life=0):
    print("start to reply hp")
    status_btn()
    os.system('adb shell input tap 872 1150')
    j = 0
    while j < times:
        if is_life == 1:
            os.system('adb shell input tap 500 1157')
        os.system('adb shell input tap 211 1157')
        sleep(2)
        j += 1
    status_btn()


def tap_with_hp():
    i = 0
    while 1:
        btn2_1()
        # sleep(1)
        dialog_btn_1()
        # sleep(1)
        i += 1
        if i % 60 == 0:
            reply_hp(10)
        print(i)
        print("经验 : %d" % (i * 30))


def tap_without_hp():
    i = 0
    while 1:
        btn1_1()
        dialog_btn_1()
        i += 1
        print(i)
        print("学费 : %d" % (i * 3000))
        print("经验 : %d" % (i * 600))


def task1_2():
    i = 0
    while 1:
        for j in range(3):
            os.system('adb shell input tap 500 600')
            sleep(0.5)
        os.system('adb shell input tap 500 850')
        i += 1
        print("经验 : %d" % (i * 15))


def kowtow():
    i = 0
    while 1:
        os.system('adb shell input tap 890 1427')
        i += 1
        print("潜能 : %d" % (i * 5))
        sleep(1)


def task_nanyang():
    interval = 10
    for i in range(3):
        os.system('adb shell input tap 860 1130')
        os.system('adb shell input tap 530 1400')
        os.system('adb shell input tap 890 1427')
        into_checkpoint()
        # reply_hp(10, 1)
        up()
        btn1_2()
        dialog_btn_center()
        for j in range(7):
            up()
        btn1_1()
        dialog_btn_1()
        full_screen_btn_1()
        right_up()
        right_up()
        right_up()
        btn1_1()
        dialog_btn_3()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        up()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        up()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        up()
        up()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        full_screen_btn_1()
        sleep(interval)
        end_fighting()
        leave_checkpoint()
        back_right()
        os.system('adb shell input tap 870 1100')
        full_screen_btn_1()
        sleep(300)


def tishui():
    i = 0
    while 1:
        btn1_2()
        dialog_btn_1()
        btn1_2()
        dialog_btn_1()
        btn1_1()
        dialog_btn_1()
        os.system('adb shell input tap 314 1400')
        os.system('adb shell input tap 314 1400')
        os.system('adb shell input tap 241 1943')
        i += 1
        if i % 25 == 0:
            os.system('adb shell input tap 85 296')
            sleep(1)
            os.system('adb shell input tap 872 1150')
            sleep(1)
            j = 0
            while j < 10:
                os.system('adb shell input tap 211 1157')
                sleep(2)
                j += 1
            os.system('adb shell input tap 211 1157')
        print(i)


def tiaoxi(min):
    while 1:
        tap(830, 2000)
        sleep(min * 60 + 10)


def run():
    tiaoxi(10)


if __name__ == '__main__':
    run()
