from os import listdir
from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pygame.mixer import Sound, stop
from os import startfile
from pygame import display, init, time, event, image, FULLSCREEN
from pygame.transform import scale

init()
is_death_screen = False


def sound(var):
    stop()
    if var != "стоп":
        Sound("sounds/" + var).play(0)


def movie(var):
    startfile("movies\\" + var)


def exe(var):
    startfile("apps\\" + var)


def death_screen(val):
    global is_death_screen
    if val == "включить":
        Sound("other\\death_sound.mp3").play()
        win = display.set_mode((1920, 1080), flags=FULLSCREEN)
        win.fill((0, 0, 0))
        win.blit(scale(image.load("other\\death screen.jpg"), (1550, 875)), (0, 0))
        display.set_caption("death screen")
        is_death_screen = True
        while is_death_screen:
            display.flip()
            time.Clock().tick(30)
            event.pump()
    elif val == "отключить":
        is_death_screen = False


class UI(object):
    # выбор третьего уровня
    @staticmethod
    def troll_screen():
        put_buttons(buttons=["включить", "отключить"],
                    onclick=death_screen, scope="third")

    # выбор второго уровня
    @staticmethod
    def sound():
        clear("second")
        clear("third")
        put_text("Воспроизвести звук", scope="second")
        put_buttons(listdir("sounds") + ["стоп"], sound, scope="second")

    @staticmethod
    def video():
        clear("second")
        clear("third")
        put_text("Воспроизвести видео", scope="second")
        put_buttons(listdir("movies"), movie, scope="second")

    def script(self):
        clear("second")
        clear("third")
        put_text("Воспроизвести сценарий", scope="second")
        put_buttons(buttons=["экран смерти"],
                    onclick=[self.troll_screen], scope="second")

    def app(self):
        clear("second")
        clear("third")
        put_text("Запустить программу", scope="second")
        put_buttons(listdir("apps"), exe, scope="second")

    # выбор первого уровня
    def troll(self):
        clear("first")
        clear("second")
        clear("third")
        put_buttons(buttons=["звук", "видео", "сценарий", "программа"],
                    onclick=[self.sound, self.video, self.script, self.app], scope="first")

    @staticmethod
    def send_file():
        clear("first")
        clear("second")
        clear("third")
        tp = radio("Выберите тип файла", ["Музыка", "Видео", "Приложение"])
        match tp:
            case "Музыка":
                tp = 0
            case "Видео":
                tp = 1
            case "Приложение":
                tp = 2
        file = file_upload("Загрузите файл", accept=["audio/mp3", "video/mp4", None][tp])
        with open(["sounds\\", "movies\\", "apps\\"][tp] + file["filename"], "wb") as f:
            f.write(file["content"])

    # главный выбор
    def main(self):
        set_scope("main")
        set_scope("first")
        set_scope("second")
        set_scope("third")
        put_buttons(buttons=["утилиты", "отправить файл"],
                    onclick=[self.troll, self.send_file], scope="main")


if __name__ == "__main__":
    start_server(applications=UI().main, port=80, host="192.168.0.166")
    config(title="Удаленный доступ")
