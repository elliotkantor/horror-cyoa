import random
from os import system, name

# colors
black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
magenta = "\033[0;35m"
cyan = "\033[0;36m"
white = "\033[0;37m"
bright_black = "\033[0;90m"
bright_red = "\033[0;91m"
bright_green = "\033[0;92m"
bright_yellow = "\033[0;93m"
bright_blue = "\033[0;94m"
bright_magenta = "\033[0;95m"
bright_cyan = "\033[0;96m"
bright_white = "\033[0;97m"

# player data
class Player:
    def __init__(self):
        self.hp = 10
        self.weapon = None
        self.name = None

    def take_damage(self, amount):
        self.hp -= amount


class Game:
    def clear(self):
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    def roll(self, target=10, adv=False, dis=False):
        """Roll a d20 with advantage or disadvantage and return whether it hit the target or not"""
        r1 = random.randint(1, 20)
        r2 = random.randint(1, 20)
        if adv:
            r1 = max(r1, r2)
        if dis:
            r1 = min(r1, r2)
        return r1 >= target

    def pb(self, block):
        """Print a block of text, one paragraph at a time with ENTER in between"""
        for par in block.split("\n"):
            print("\n" + par)
            input("Press ENTER to continue")
            self.clear()

    def i(self, prompt=">> ", accepted=None) -> str:
        """Get user input with only some accepted answers"""
        if accepted:
            while True:
                out = input(prompt)
                if out in accepted:
                    break
                else:
                    print("Sorry, that's not a valid response.\n")
        else:
            out = input(prompt)
        return out

    def po(self, options):
        """Print options"""
        for i, o in enumerate(options):
            print(f"[{i+1}] {o}")


if __name__ == "__main__":
    p = Player()
    g = Game()