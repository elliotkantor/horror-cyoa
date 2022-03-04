import random
from os import system, name
import re
import sys
from time import sleep

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
        self.attacks = {"sword": 6, "bow": 4}
        self.blocks = {"heavy": 3, "light": 1}

    def take_damage(self, amount):
        self.hp -= amount

    def attack(self):
        return self.attacks.get(self.weapon) + random.randint(-1, 1)

    def block(self):
        return self.blocks.get(self.armor) + random.randint(-1, 1)


class Game:
    def __init__(self) -> None:
        self.p = Player()
        self.visited = {"Horde": False, "Feast": False, "Trophy": False}

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
        return r1 >= target, r1

    def c(self, text="Press ENTER to continue"):
        """Continue by pressing ENTER"""
        input(f"\n{text}\n")

    def pb(self, block, trailing=True):
        """Print a block of text, one paragraph at a time with ENTER in between
        trailing: true to clear at end, false to not clear"""
        text = block.strip().split("\n")
        for i, par in enumerate(text):
            last = i == len(text) - 1
            print("\n" + par)
            if not (last and not trailing):
                input("\nPress ENTER to continue")
                self.clear()
            # else:
            #     print()

    def i(self, prompt=">> ", accepted=None, empty=True) -> str:
        """Get user input with only some accepted answers
        accepted: list of allowed answers
        empty: allows empty strings"""
        if accepted:
            while True:
                out = input(prompt).strip()
                if out in accepted:
                    break
                else:
                    print("Sorry, that's not a valid response.\n")
        elif not empty:
            while True:
                out = input(prompt).strip()
                if out:
                    break
                else:
                    print("Sorry, you need to enter something.\n")
        else:
            out = input(prompt)
        return out

    def po(self, options):
        """Print options and return choice"""
        dic = {str(i + 1): o for i, o in enumerate(options)}
        accepted = dic.keys()  # accept only numbers
        for i, o in dic.items():
            print(f"[{i}] {o}")
        return dic[self.i(accepted=accepted)]

    def combat(
        self, intro="Beginning combat!", enemy="monster", enemy_hp=10, enemy_strength=3
    ):
        """Return true if you die, else enemy died"""

        def end():
            """Check if you should end"""
            if self.p.hp <= 0 or enemy_hp <= 0:
                return True
            return False

        print(intro)
        print(
            f"""
Your stats: 
- Health: {self.p.hp}
- Armor: {self.p.armor}
- Weapon: {self.p.weapon}"""
        )

        total_damage = 0
        while True:
            print(f"It's your turn, {self.p.name}. Hit ENTER to roll for damage.")
            input(">> ")
            attack = self.p.attack()
            print(f"\nYou hit the {enemy} with {attack} points of damage!")
            enemy_hp -= attack
            if end():
                break

            print(f"\nIt's now the {enemy}'s turn. Hit ENTER to see its roll...")
            input(">> ")
            attack = enemy_strength + random.randint(-1, 1)
            block = self.p.block()
            damage = attack - block
            if damage < 0:
                damage = 0
            total_damage += damage
            print(
                f"\nIt attacks with {attack} points of damage, but you block {block} points. Take {damage} points of damage."
            )
            self.p.take_damage(damage)
            if end():
                break
        if self.p.hp <= 0:
            die = True
        else:
            die = False
        return die, total_damage

    def intro(self):

        # intro stuff
        print(
            "Welcome, brave adventurer! What shall we call you? Type your name and hit ENTER."
        )
        self.p.name = self.i(empty=False)
        print(
            f"\nAlright, {self.p.name}. Pick a main weapon. Type a number and hit ENTER."
        )
        self.p.weapon = self.po(["Bow", "Sword"]).lower()
        print("\nPick your armor type.")
        self.p.armor = self.po(["Light", "Heavy"]).lower()

        read_intro = self.po(["Skip intro", "Read intro"]).startswith("Read")
        self.clear()
        if read_intro:
            # backstory
            self.pb(
                f"""
    You are on your way to the Tomb of Zar, the king of this land from eons ago. The path you've trodden was frequented by adventurers like yourself many years ago. They, like you, are on a quest for Zar's Eye of Phlegm, which is rumored to give the owner a magical view of the future. Obviously, a treasure such as this would be priceless, so with its power and wealth you may just have your banishment lifted from your home in Perth.
    Shortly after Zar's death, thousands flooded into the cavern you find yourself delving into now, yet none emerged. Before his death, the king hired some of the finest engineers in the North, from the industrious town of Heluven, to trap his tomb from the grave robbers he predicted would come. The Heluven engineers claimed that the tomb was impenetrable, but you'll soon test that yourself.
    Snap, snap. Your boots clap on the ground as you descend deeper into the cavern. It's getting colder now. A slippery patch of moss here, an ankle-rolling crack there. Stay attentive, {self.p.name}. Your two-week journey has left you exhausted, and that encounter with the Night Hounds last night robbed you of a week's worth of rations. In your hazy state, you fail to notice the soft footfalls following behind you."""
            )

    def noises(self):
        self.pb(
            """
After an hour or two of spelunking, you become aware of the deep rumbling of the earth surrounding you. Thus far the journey has been simple, placid. But now you’ve become acutely aware of the gaping mouth of earth slowly consuming you. 
To your right, you hear a distant wail. Silence. Then, laughing. A chill runs over you, straight through your clothing. You continue on, with nothing but the sound of the earth and your thoughts to accompany you."""
        )

    def left(self):
        self.pb(
            f"""As you descend down the left path, you begin to hear the sloshing of water below. The path is getting steeper, as you can see with your dimming torch. 
After twenty minutes, you hit a dead end. There is a small pool of water, no more than a meter across, that descends into black beneath the rock. What do you do?""",
            False,
        )
        choice = self.po(
            ["Try to swim through it", "Turn around and take the other path"]
        )
        if choice.startswith("Try"):
            self.swim()
        else:
            self.right()

    def swim(self):
        self.pb(
            f"""
You dip your toes into the pool. Frigid. You shed your {self.p.weapon} and armor, and plunge in.
As you descend deeper, you begin swimming forward, trying to dive under the obstacle. After thirty seconds, you decide to try resurfacing. 
Bonk.
You hit your head on the rock above you. Okay, let’s try going further. You swim farther forward, float up, and...
Bonk.
Panic starts to set in. What do you do?""",
            False,
        )
        choice = self.po(["Try to turn around", "Keep swimming farther"])
        if choice.startswith("Try"):
            self.turn_around()
            self.right()
        else:
            self.keep_swimming()

    def turn_around(self):
        self.pb(
            """
You tumble underwater, turn in the direction that seems backward, and swim full speed, lungs searing with pain. 
Crack! Your head smashes into the rock ahead of you and you finally surface, gasping for breath. Your torch is laying on the damp ground, still alight like dying coals. As you yank yourself out of the freezing pool, you notice the steady flow of dark blood from your head. Take 3 damage. 
After a moment, you prepare for the journey back. You begin the steep ascent, weakened from your head injury. 
"""
        )
        self.p.take_damage(3)

        if self.roll(8)[0]:
            self.cave_monster()

    def cave_monster(self):
        self.pb(
            "Before you can comprehend anything, a dark blur comes flying at your face! Its sharp talons claw into your cheeks, and all you see is the manic motion of glowing red eyes in front of you. Begin combat!"
        )
        die, pts = self.combat(
            intro="Begin cave monster battle!",
            enemy="cave monster",
            enemy_hp=7,
            enemy_strength=2,
        )
        self.c()
        self.clear()
        if die:
            self.pb(
                "The monster ripped your face apart, strip by strip, blood oozing in a large oblong puddle on the floor. You have joined the thousands of unlucky adventurers in death."
            )
            sys.exit()
        else:
            self.pb(
                f"With a final attack, the monster falls dead beneath your {self.p.weapon}. You sustained {pts} points of damage, and finally make your way back to the fork in the tunnel. You have no choice but to take the other path."
            )

    def keep_swimming(self):
        self.pb(
            """
Determined not to let the icy water take you, you give a few last kicks in what you can only hope is forward. You feel the surface tension of water on your head, and rip your head upwards to take in a much-needed breath. As you drag yourself out of the water, you become aware of the cavernous room you are in, lit dimly by white moonlight. """
        )
        self.pick_room()

    def right(self):
        self.pb(
            """
You continue down the rightmost path, and after half an hour of walking you realize you’ve been walking in circles. A spiral. The smell of metal is pungent in the air. The spiral is getting tighter, you notice, as you can see the curve of the wall growing nearer to you in the flickering light. 
Suddenly, a freezing breeze extinguishes your torch completely. Total darkness. With nothing better to do, you fumble for the wall and follow it with your hand. 
In the absence of light, your memory starts to take a hold of you. You recall the only other time you’ve experienced such rich blackness, on an Education trip into the Quarries of Perth. With your accolades huddled in the middle of a cathedral-like hollow, the guide had shut off the last light, letting total darkness take over. 
That was before. Everything is different now. 
When the spiral has gotten so tight that you can scarcely believe you’re even getting anywhere, you finally see a steady white light down the hallway. 
At the end of the hallway, you find the mouth to a huge opening, larger than the one you visited so many years ago. """
        )

        self.pick_room()

    def pick_room(self):
        if not (self.visited["Horde"] or self.visited["Feast"]):
            # pick one of the two next rooms
            if random.randint(1, 2) == 1:
                room = "Horde"
            else:
                room = "Feast"
        elif self.visited["Horde"]:
            # feast or trophy
            if random.randint(1, 2) == 1:
                room = "Trophy"
            else:
                room = "Feast"
        elif self.visited["Feast"]:
            # horde or trophy
            if random.randint(1, 2) == 1:
                room = "Horde"
            else:
                room = "Trophy"
        else:
            # trophy
            room = "Trophy"
        self.visited[room] = True

        if room == "Trophy":
            self.trophy()
        elif room == "Horde":
            self.horde()
        else:
            self.feast()
        return room

    def trophy(self):
        self.pb(
            """
When you catch your breath, you stand up to find yourself in a smaller room than before, this time lit with gold lighting from some unknown location. Ahead, beneath a massive tapestry of the Zenith Wars, is an iridescent obsidian coffin. You take a step closer.
As your ruined boots clack on the rock, you see that there are no boot marks anywhere in the room. When you reach the coffin, you use your last remaining strength to push the lid ajar. Inside, you see the bony face, with a single glowing purple eye. Closing your own eyes, you reach in and pry out the surprisingly round and hard eye from its leathery socket. 
Turning away from the coffin, you take a moment to look at the eye. It feels cool, like stone, and emits a faint, steady glow in your hands. As you steel yourself for the return journey, you take a moment to reflect on what this means for you now. Wealth beyond your wildest dreams, praise from your family and nobles alike. 
You smile for the first time since setting off on the perilous journey. You start walking toward the door. In your excitement, you fail to notice the body in the coffin slowly, ever so silently, lift itself upright and turn to you."""
        )

    def horde(self):
        self.pb(
            """
You step into the large space. Without warning, the entire perimeter roars alight with flame! Your eyes, used to the darkness of torch and moonlight, sear with pain. When your eyes finally adjust, you notice the horde of figures lumbering toward you. 
What do you do?""",
            False,
        )
        choice = self.po(["Run", "Hide", "Fight"])
        if choice == "Run":
            self.pb(
                """
You bolt off running, the horde following you. In the glances you get as you run to the opposite end of the chamber, you notice that they look like they belong here. They wear adventure gear, worn down to the threads, and they hold spelunking gear. 
Their faces… They are pale and gray, tight against the bone. They move jerkily, like puppets. As they close in from the right and left, you bolt toward the dark opening on the far side of the room. Roll for an acrobatics check."""
            )
            success, roll = self.roll(10, dis=self.p.armor == "heavy")
            print(f"You rolled a(n) {roll}!")
            if success:
                self.pb(
                    """
You sprint straight through the horde, crusty hands clawing at your limbs as you pass. You break free, and dive headfirst into the dark. You find yourself gliding down a long slide, into the deep darkness. The slide is surprisingly smooth for something so old.
At the bottom, you find yourself in a new room."""
                )
                self.pick_room()
            else:
                self.pb(
                    """
Halfway across the room, you stumble and fall on your face! You slide a few feet, and the moment you regain your awareness, a strong arm grabs the collar of your shirt. Another reaches for your neck, grabs.
In a swift motion, it has ripped out your throat. You immediately go limp, dead. """
                )
                sys.exit()
        elif choice == "Hide":
            self.pb(
                """
You duck behind a rock, concealing yourself from their sight. But you didn’t anticipate their sense of smell. Back against the earth, you see red light thrown onto the opposite wall. You wait.
Silence.
Suddenly, a silhouette of a figure on the wall in front of you! You look up in terror and see a rotting face looking down at you, smiling.
Before you can do anything, you find yourself surrounded, bony hands ripping at your clothing, surprisingly strong. With no time to reach for your weapon, they have torn you to pieces, ripping off your face and limbs with their brittle teeth. 
You died."""
            )
            sys.exit()
        else:
            died, damage = self.combat(
                intro="Time to fight!", enemy="horde", enemy_hp=15, enemy_strength=4
            )
            self.c()
            self.clear()
            if died:
                self.pb(
                    "In one deft blow, a zombified adventurer knocks you unconscious. When you awake moments later, you find yourself surrounded by the figures. Your scream echoes in the chamber as they bite into your neck. Then, blackness. You died."
                )
                sys.exit()
            else:
                self.pb(
                    f"With the final attack, you’ve cleared yourself a path to what can only be the exit at the far end of the room! In all the chaos, you’ve escaped to the back of the room with only {damage} points of damage and dive into the darkness. A rock slides into place behind you, locking you inside but protecting you from the monsters behind. You walk a few paces ahead and find yourself in another room."
                )
                self.pick_room()

    def feast(self):
        self.pb(
            """
When you finally right yourself, you notice you’re in a fabulous banquet hall! You become aware of the smell of roast duck, exquisitely prepared beef wellington, and aromatic desserts. The slender white candles on the table are burning as bright as ever, as if they had just been lit. The long table extends hundreds of feet in either direction, farther than you can see from here. 
There’s only one thing: the entire feast is absent of any people. It’s as if all the guests had stepped outside seconds before your arrival. You can still see the hot steam rising from the poultry. Your stomach growls and seizes. What do you do?"""
        )
        choice = self.po(["Start feasting", "Walk around the table"])
        if choice.startswith("Start"):
            self.pb(
                """
You rush toward the table, tearing off a duck leg. It’s been weeks since you’ve eaten a proper meal. You stuff your face with mashed potatoes, steak tartare, and creamed broccoli. You cannot stop!
You cannot stop. You really cannot stop. Something is terribly wrong. Your stomach starts to spasm uncontrollably, but you can’t stop your hands from impulsively cramming food in your mouth. It feels like lava is pooling in your stomach! You scream in pain, but it’s muffled with the food you cannot resist from eating. 
Hours go past, agonizing beyond belief, with no control whatsoever. When you begin coughing up blood, it comes as a relief. Within a few hours, you physically wither away, your stomach dissolving itself and you from the inside out. You tumble to the ground, a pile of bloated skin and bones. You died. """,
                False,
            )
            sys.exit()
        else:
            self.pb(
                """
This doesn’t feel right. You sidestep around the table, keeping your distance. You hurriedly walk toward the end of the table, just at the edge of your sight. In your haste, you don’t notice the tripwire that you stumble into until you trip and fall. 
You immediately hear a low groan of rock shifting, then the sound of water from behind you. What do you do?"""
            )
            choice = self.po(["Run", "Investigate"])
            if choice == "Investigate":
                self.pb(
                    "Rising to your knees, you look at the tripwire you just triggered. It runs along the length of the huge room, and is connected through the rock. Fantastic engineering, you think. As you turn around, you notice the thirty foot wall of water rushing toward you. Run!"
                )
            else:
                self.pb(
                    "You surge forward, away from the rushing water. You’re nearly at the end of the table, and just beyond is a gaping hole, a huge stone acting as an open door. When you look over your shoulder, you see a wall of water 50 feet behind you, it’s gaining on you!"
                )
            self.pb("Roll for an athletics check!")
            survive, roll = self.roll(dis=choice == "Investigate")
            print(f"You rolled a(n) {roll}!")
            if survive:
                self.pb(
                    """
In a surge of athleticism, you sprint faster than ever before and scramble into the dark room beyond. As soon as you step through, the massive rock, thousands of pounds, no doubt, slides effortlessly into place behind you with a thud. Less than a second after, you hear the deep crash of tons of water against rock. You quickly step back from the door, unsure of how strong it is. As you back up, you bump into a great wooden door. It’s unlocked.
When you unlock it, you find yourself once again in a new room."""
                )
                self.pick_room()
            else:
                self.pb(
                    """
You are running as fast as you can, but your limited diet the past few weeks has left you starving and weak. You slow down, and immediately the water sweeps you off of your feet, and you tumble in the strong current of thousands of tons of water. 
In the near-complete darkness from the extinguished candles, you roll in all directions, running out of breath. Right before you run out of breath, the water mercifully smashes you into the rock wall at the end of the room, killing you instantly. You died. """,
                    False,
                )
                sys.exit()

    def play(self):

        self.intro()
        self.noises()

        # branch
        print(
            f"You’ve found a fork in the tunnel, {self.p.name}! In your exhausted stupor you’ve almost missed it. Quickly, pick a direction to go in."
        )
        direction = self.po(["Left", "Right"])
        if direction == "Left":
            self.left()
        else:
            self.right()

        # Credits
        self.clear()
        print(
            f"Thanks for playing, {self.p.name}! This game was created for an English assignment, and the bulk of the work was done within 48 hours. Not bad for a game, eh?"
        )
        self.c("Press ENTER to show your support for how great Elliot is!")
        self.clear()
        print(
            "Please play again to get more endings, I promise there's more than one! There is also a chance of encountering new/different rooms! And perhaps even easter eggs! Thanks for playing!"
        )


if __name__ == "__main__":
    g = Game()
    g.play()