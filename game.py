from tkinter import Toplevel, Button, Label, Text, END, LEFT, BOTH, X, Y, TOP, BOTTOM
from main import player, DiceRoll, check_gang_members
import time
import random
import sqlite3


def QuickRoll(result, other=None):
    if other is not None:
        return f"Die 1: {result}, Die 2: {other}"
    if isinstance(result, (tuple, list)) and len(result) >= 2:
        return f"Die 1: {result[0]}, Die 2: {result[1]}"
    return f"Roll: {result}"


def leaderboard(parent):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("SELECT username, score FROM LEADERBOARD ORDER BY score DESC")
    rows = c.fetchall()
    conn.close()
    leaderboard_win = Toplevel(parent)
    leaderboard_win.title("Leaderboard")
    leaderboard_win.transient(parent)
    leaderboard_win.resizable(False, False)
    Label(leaderboard_win, text="Leaderboard", font=("Segoe UI", 11, "bold")).pack(padx=12, pady=(10, 6))
    for idx, row in enumerate(rows, start=1):
        Label(leaderboard_win, text=f"{idx}. {row[0]} - {row[1]}").pack(anchor='w', padx=12)


def RollAnimation(result, parent, quick=False, colour="black", times=10, delay=0.08):
    if quick:
        lbl = Label(parent, text=QuickRoll(result), font=("Segoe UI", 10, "bold"), fg=colour)
        lbl.pack(padx=12, pady=12)
        parent.update()
        parent.after(2000, lbl.destroy)
    else:
        lbl = Label(parent, text="Rolling...", font=("Segoe UI", 10, "bold"), fg=colour)
        lbl.pack(padx=12, pady=12)

        for _ in range(times):
            temp_roll = DiceRoll()
            lbl.config(text=f"Rolling... {temp_roll}")
            parent.update()
            time.sleep(delay)

        lbl.config(text=f"Final Roll: {result}")
        parent.update()
        parent.after(2000, lbl.destroy)


class Game:
    def __init__(self, player_obj: player, master=None):
        self.player = player_obj
        self.day = int(self.player.stats.get('Day', 1))
        self.ammo = int(self.player.stats.get('Ammo', 20) or 20)
        self.food = int(self.player.stats.get('Food', 20) or 20)
        self.survivors = int(self.player.stats.get('Survivors', 1) or 1)
        self.dog = bool(self.player.stats.get('Dog', 1))
        core_val = self.player.stats.get('Gang', '')
        self.core = '' if core_val in (None, 'None') else core_val
        self.gang_display = ', '.join(check_gang_members(self.player.username))
        self.master = Toplevel() if master is None else Toplevel(master)
        self.master.title(f"Survival: {self.player.username}")
        self.cooldown = False

        self._build_ui()
        self._recruit_on_start()
        self._update_ui()

    def _build_ui(self):
        self.lbl_day = Label(self.master, text="")
        self.lbl_day.pack(fill=X, padx=8, pady=4)

        self.lbl_stats = Label(self.master, text="", justify=LEFT)
        self.lbl_stats.pack(fill=X, padx=8, pady=4)

        self.msg = Text(self.master, height=10, wrap='word')
        self.msg.pack(fill=BOTH, expand=True, padx=8, pady=4)
        
        self.btn_next = Button(
            self.master,
            text="Next Day",
            command=self._next_day_handler)
        self.btn_next.pack(side=BOTTOM, fill=X, padx=8, pady=6)

    def _next_day_handler(self):
        if self.cooldown:
            return
        self.cooldown = True
        self.btn_next.config(state="disabled")
        self.next_day(check_gang_members(self.player.username))
        self.master.after(500, self._enable_button)

    def _enable_button(self):
        self.cooldown = False
        self.btn_next.config(state="normal")

    def _append_msg(self, text: str):
        try:
            self.msg.insert(END, text + "\n\n")
            self.msg.see(END)
        except Exception:
            pass
    
    def _update_ui(self):
        self.lbl_day.config(text=f"Day: {self.day}")
        stats_text = (
            f"Ammo: {self.ammo}    Food: {self.food}    Survivors: {self.survivors}\n"
            f"Scooby-Doo: {'Alive' if self.dog else 'Gone'}    Gang: {self.gang_display}"
        )
        self.lbl_stats.config(text=stats_text)

    def save_to_player(self):
        self.player.stats['Day'] = self.day
        self.player.stats['Ammo'] = self.ammo
        self.player.stats['Food'] = self.food
        self.player.stats['Survivors'] = self.survivors
        self.player.stats['Gang'] = self.core if self.core else 'None'
        self.player.stats['Dog'] = 1 if self.dog else 0

        try:
            conn = sqlite3.connect('game_data.db')
            c = conn.cursor()
            c.execute(
                "UPDATE PLAYER_DATA SET food = ?, ammo = ?, survivors = ?, core = ?, dog = ? WHERE username = ?",
                (self.player.stats['Food'], self.player.stats['Ammo'], self.player.stats['Survivors'],
                 self.player.stats['Gang'], self.player.stats['Dog'], self.player.username)
            )
            conn.commit()
        finally:
            conn.close()

    def reset_game(self):
        self.day = 1
        self.ammo = 20
        self.food = 20
        self.survivors = 1
        self.dog = True
        self.core = ''
        self.gang_display = ''
        self._update_ui()
        self.save_to_player()

    def calculate_score(self, win: bool):
        survivors_score = self.survivors * 100
        food_score = self.food * 5
        ammo_score = self.ammo * 2
        day_score = self.day * 10
        dog_score = 200 if self.dog else 0
        gang_count = len(self.core) if self.core else 0
        gang_score = gang_count * 150
        win_score = 1000 if win else 0

        total = survivors_score + food_score + ammo_score + day_score + dog_score + gang_score + win_score

        score_win = Toplevel(self.master)
        score_win.title("Final Score")
        score_win.transient(self.master)
        score_win.resizable(False, False)

        Label(score_win, text=f"Final Score for {self.player.username}", font=("Segoe UI", 11, "bold")).pack(padx=12, pady=(10, 6))
        Label(score_win, text=f"Survivors: {self.survivors} x 100 = {survivors_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Food: {self.food} x 5 = {food_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Ammo: {self.ammo} x 2 = {ammo_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Days survived: {self.day} x 10 = {day_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Dog bonus: {dog_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Gang ({gang_count}): {gang_score}").pack(anchor='w', padx=12)
        Label(score_win, text=f"Win bonus: {win_score}").pack(anchor='w', padx=12)
        Label(score_win, text="-------------------------------").pack(padx=12, pady=(6, 0))
        Label(score_win, text=f"Total Score: {total}", font=("Segoe UI", 10, "bold")).pack(padx=12, pady=(6, 12))
        self.reset_game()

        def close():
            score_win.destroy()
            leaderboard(self.master)

        Button(score_win, text="Close", command=close).pack(pady=(0, 12))
        try:
            conn = sqlite3.connect('game_data.db')
            c = conn.cursor()
            c.execute("SELECT score FROM LEADERBOARD WHERE username = ?", (self.player.username,))
            row = c.fetchone()
            if row is None:
                c.execute("INSERT OR REPLACE INTO LEADERBOARD (username, score) VALUES (?, ?)", (self.player.username, total))
            else:
                prev = row[0] or 0
                if total > prev:
                    c.execute("UPDATE LEADERBOARD SET score = ? WHERE username = ?", (total, self.player.username))
            conn.commit()
        finally:
            conn.close()

        return total

    def _recruit_on_start(self, quickroll=False):
        if not self.core:
            member = self.recruit_members(quick=quickroll)
            if member:
                self._append_msg(f"You recruited {member} at game start!")
            else:
                self._append_msg("No recruits found at game start.")
        self.gang_display = ', '.join(check_gang_members(self.player.username))

    def recruit_members(self, quick=False):
        d1 = DiceRoll(4)
        RollAnimation(d1, self.master, quick=quick, colour="green")

        code_map = {"Fred": "F", "Daphne": "D", "Shaggy": "S"}
        recruited = None
        if d1 == 2:
            recruited = "Fred"
        elif d1 == 3:
            recruited = "Daphne"
        elif d1 == 4:
            recruited = "Shaggy"

        if not recruited:
            return None

        code = code_map[recruited]
        if code not in self.core:
            self.core += code
            try:
                conn = sqlite3.connect('game_data.db')
                c = conn.cursor()
                c.execute("UPDATE PLAYER_DATA SET core = ? WHERE username = ?", (self.core, self.player.username))
                conn.commit()
            finally:
                conn.close()
            self.player.stats['Gang'] = self.core
            self.gang_display = ', '.join(check_gang_members(self.player.username))
            self._update_ui()
            return recruited
        else:
            return None

    def next_day(self, gang_members, quickroll=False):
        if self.day >= 100:
            self._append_msg("You have survived 100 days — you win!")
            self.btn_next.config(state="disabled")
            self.cooldown = True
            try:
                self.calculate_score(win=True)
            except Exception:
                pass
            return

        self.day += 1
        d1 = DiceRoll()
        d2 = DiceRoll()
        RollAnimation((d1, d2), self.master, quick=quickroll)
        self._append_msg(f"First die: {d1}, Second die: {d2}")
        if d1 in (1, 3):
            zombies = random.randint(1, 4)
            self._append_msg(f"Zombie encounter! {zombies} zombies attack.")
            if "Fred" in gang_members:
                d3 = DiceRoll()
                RollAnimation(d3, self.master, quick=quickroll, colour="red")
                if d3 >= 4:
                    self._append_msg("Fred rushes at the zombies, taking out a group of zombies!")
                    zombies = max(0, zombies - 4)
                elif d3 == 1:
                    self._append_msg("Fred fails in his attack, and he is lost in the horde")
                    try:
                        gang_members.remove("Fred")
                    except ValueError:
                        pass
            if self.ammo >= zombies:
                self.ammo -= zombies
                self._append_msg(f"You used {zombies} ammo to fend them off.")
            else:
                losses = max(1, zombies - self.ammo)
                self._append_msg(f"Not enough ammo. You lose {losses} survivor(s).")
                self.survivors = max(0, self.survivors - losses)
                self.ammo = 0
        elif d1 == 2:
            found = random.randint(5, 8)
            self._append_msg(f"You scavenge and find {found} ammo.")
            if self.dog is True:
                d4 = DiceRoll()
                RollAnimation(d4, self.master, quick=quickroll, colour="blue")
                if d4 >= 5:
                    found += 4
                    self._append_msg("Scooby-Doo sniffs out extra ammo!")
                else:
                    self._append_msg("Scooby fails to find anything.")
            self.ammo += found
        elif d1 == 4:
            found = random.randint(5, 8)
            self._append_msg(f"You scavenge and find {found} food.")
            if "Shaggy" in gang_members:
                d3 = DiceRoll()
                RollAnimation(d3, self.master, colour="blue")
                if d3 >= 5:
                    found += 4
                    self._append_msg("Shaggy's keen senses help you find extra food!")
                else:
                    self._append_msg("Shaggy fails to find anything.")
            self.food += found
        elif d1 == 5:
            if d2 % 2 == 0:
                self.recruit_members()
            else:
                self._append_msg("A quiet day. Survivors rest and recover morale.")
        elif d1 == 6:
            if d2 % 2 == 0:
                self.survivors += 1
                self._append_msg("You recruit a wandering survivor.")
            else:
                if self.food > 2:
                    if "Daphne" in gang_members:
                        self.food = max(0, self.food - 3)
                        self.ammo += 8
                        self._append_msg("A survivor trades 3 food for 5 ammo.")
                        self._append_msg("Daphne negotiates a better trade: 3 food for 8 ammo.")
                    else:
                        self.food = max(0, self.food - 3)
                        self.ammo += 5
                        self._append_msg("A survivor trades 3 food for 5 ammo.")
                else:
                    self._append_msg("A survivor offers a trade but you have no food.")

        daily_food_needed = max(1, self.survivors + len(gang_members) // 2)
        if self.food >= daily_food_needed:
            self.food -= daily_food_needed
            self._append_msg(f"Your group consumed {daily_food_needed} food today.")
        else:
            if "Shaggy" in gang_members:
                d3 = DiceRoll()
                RollAnimation(d3, self.master, quick=quickroll, colour="blue")
                if d3 >= 4:
                    self._append_msg("Shaggy searches for more food, and successfully prevents starvation.")
                elif d3 == 1:
                    self._append_msg("Shaggy searches for more food, but never returns.")
                    self.survivors = max(0, self.survivors - 1)
                    self._append_msg("Food is low. A survivor is lost to starvation.")
                    try:
                        gang_members.remove("Shaggy")
                    except ValueError:
                        pass
                else:
                    self._append_msg("Shaggy fails to find any more food.")
                    self.survivors = max(0, self.survivors - 1)
                    self._append_msg("Food is low. A survivor is lost to starvation.")
            else:
                lost = 1
                self._append_msg("Food is low. A survivor is lost to starvation.")
                self.survivors = max(0, self.survivors - lost)
                self.food = 0

        if self.dog and random.random() < 0.02:
            self.dog = False
            self._append_msg("Tragically, you lost Scooby during the night.")

        self._update_ui()
        self.save_to_player()

        if self.survivors <= 0:
            self._append_msg(f"You survived until Day {self.day} but were wiped out. Game over.")
            self.btn_next.config(state="disabled")
            self.cooldown = True
            try:
                self.calculate_score(win=False)
            except Exception:
                pass


def launch_game(player_obj: player, master=None):
    Game(player_obj, master)