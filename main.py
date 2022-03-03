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
        self.armor = None

    def take_damage(self, amount):
        self.hp -= amount


class RandomState:
    def __init__(self):
        self.noises = random.randint(0, 1)


class Game:
    def __init__(self) -> None:
        self.p = Player()

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

    def c(self):
        """Continue by pressing ENTER"""
        input("\nPress ENTER to continue\n")

    def pb(self, block):
        """Print a block of text, one paragraph at a time with ENTER in between"""
        for par in block.strip().split("\n"):
            print("\n" + par)
            input("\nPress ENTER to continue")
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
        dic = {str(i + 1): o for i, o in enumerate(options)}
        accepted = dic.keys()  # accept only numbers
        for i, o in dic.items():
            print(f"[{i}] {o}")
        return dic[self.i(accepted=accepted)]

    def intro(self):

        # intro stuff
        print(
            "Welcome, brave adventurer! What shall we call you? Type your name and hit ENTER. Leave empty to skip intro."
        )
        self.p.name = self.i()
        if self.p.name.strip() == "":
            return
        print(
            f"\nAlright, {self.p.name}. Pick a main weapon. Type a number and hit ENTER."
        )
        self.p.weapon = self.po(["Bow", "Sword"])
        print("\nPick your armor type.")
        self.p.armor = self.po(["Light", "Heavy"])
        self.c()
        self.clear()

        # backstory
        self.pb(
            f"""
You are on your way to the Tomb of Zar, the king of this land from eons ago. The path you've trodden was frequented by adventurers like yourself many years ago. They, like you, are on a quest for Zar's Eye of Phlegm, which is rumored to give the owner a magical view of the future. Obviously, a treasure such as this would be priceless, so with its power and wealth you may just have your banishment lifted from your home in Perth.
Shortly after Zar's death, thousands flooded into the cavern you find yourself delving into now, yet none emerged. Before his death, the king hired some of the finest engineers in the North, from the industrious town of Heluven, to trap his tomb from the grave robbers he predicted would come. The Heluven engineers claimed that the tomb was impenetrable, but you'll soon test that yourself.
Snap, snap. Your boots clap on the ground as you descend deeper into the cavern. It's getting colder now. A slippery patch of moss here, an ankle-rolling crack there. Stay attentive, {self.p.name}. Your two-week journey has left you exhausted, and that encounter with the Night Hounds last night robbed you of a week's worth of rations. In your hazy state, you fail to notice the soft footfalls following behind you."""
        )

    def play(self) -> bool:
        self.intro()
        print("\nWould you like to play again?")
        quit = self.po(["Yes", "No"])
        return quit == "No"


if __name__ == "__main__":
    while True:
        try:
            g = Game()
            s = RandomState()

            quit = g.play()
            if quit:
                print("\nThanks for playing!")
                break
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break
