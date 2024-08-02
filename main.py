import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.games_played = 0

    def update_stats(self, goals_for, goals_against):
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.games_played += 1
        if goals_for > goals_against:
            self.points += 3  # Win
        elif goals_for == goals_against:
            self.points += 1  # Draw
        # No points for a loss (goals_for < goals_against)

    def __str__(self):
        return f"{self.name}: {self.games_played} games, {self.goals_for} GF, {self.goals_against} GA, {self.points} points"

class Group:
    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team_name):
        if team_name not in self.teams:
            self.teams[team_name] = Team(team_name)

    def record_match(self, team1_name, team1_goals, team2_name, team2_goals):
        if team1_name in self.teams and team2_name in self.teams:
            self.teams[team1_name].update_stats(team1_goals, team2_goals)
            self.teams[team2_name].update_stats(team2_goals, team1_goals)
        else:
            messagebox.showerror("Error", "One or both teams are not in the group.")

    def display_standings(self):
        standings = sorted(self.teams.values(), key=lambda x: x.points, reverse=True)
        return standings

class FootballApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Euro2024 Manager")
        self.geometry("800x600")

        self.groups = {}

        # Load background image
        self.background_image = Image.open("Euro2024Logo.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.create_widgets()

    def create_widgets(self):
        # Create canvas and set background image
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Widgets are placed directly on the canvas with specific coordinates
        self.group_label = tk.Label(self.canvas, text="Group Name:", bg="lightgrey")
        self.canvas.create_window(100, 30, window=self.group_label)

        self.group_entry = tk.Entry(self.canvas)
        self.canvas.create_window(250, 30, window=self.group_entry)

        self.create_group_button = tk.Button(self.canvas, text="Create Group", command=self.create_group)
        self.canvas.create_window(400, 30, window=self.create_group_button)

        self.team_label = tk.Label(self.canvas, text="Team Name:", bg="lightgrey")
        self.canvas.create_window(100, 70, window=self.team_label)

        self.team_entry = tk.Entry(self.canvas)
        self.canvas.create_window(250, 70, window=self.team_entry)

        self.group_combobox_label = tk.Label(self.canvas, text="Select Group to Add Team:", bg="lightgrey")
        self.canvas.create_window(250, 110, window=self.group_combobox_label)

        self.group_combobox_for_teams = ttk.Combobox(self.canvas)
        self.canvas.create_window(250, 140, window=self.group_combobox_for_teams)

        self.add_team_button = tk.Button(self.canvas, text="Add Team", command=self.add_team)
        self.canvas.create_window(250, 180, window=self.add_team_button)

        self.match_label = tk.Label(self.canvas, text="Enter Match Result:", bg="lightgrey")
        self.canvas.create_window(250, 220, window=self.match_label)

        self.group_selection_label = tk.Label(self.canvas, text="Select Group:", bg="lightgrey")
        self.canvas.create_window(100, 250, window=self.group_selection_label)

        self.group_combobox = ttk.Combobox(self.canvas, state="readonly")
        self.canvas.create_window(250, 250, window=self.group_combobox)
        self.group_combobox.bind("<<ComboboxSelected>>", self.on_group_select)

        self.team1_label = tk.Label(self.canvas, text="Team 1:", bg="lightgrey")
        self.canvas.create_window(100, 290, window=self.team1_label)

        self.team2_label = tk.Label(self.canvas, text="Team 2:", bg="lightgrey")
        self.canvas.create_window(350, 290, window=self.team2_label)

        self.team1_combobox = ttk.Combobox(self.canvas)
        self.canvas.create_window(100, 315, window=self.team1_combobox)

        self.team1_goals_entry = tk.Entry(self.canvas, width=5)
        self.canvas.create_window(200, 315, window=self.team1_goals_entry)

        self.vs_label = tk.Label(self.canvas, text="vs", bg="white")
        self.canvas.create_window(225, 315, window=self.vs_label)

        self.team2_combobox = ttk.Combobox(self.canvas)
        self.canvas.create_window(350, 315, window=self.team2_combobox)

        self.team2_goals_entry = tk.Entry(self.canvas, width=5)
        self.canvas.create_window(250, 315, window=self.team2_goals_entry)

        self.record_match_button = tk.Button(self.canvas, text="Record Match", command=self.record_match)
        self.canvas.create_window(225, 370, window=self.record_match_button)

        self.standings_text = tk.Text(self.canvas, bg="yellow", height=10, width=60)
        self.canvas.create_window(250, 480, window=self.standings_text)

        self.display_standings_button = tk.Button(self.canvas, text="Display Standings", command=self.display_standings)
        self.canvas.create_window(250, 560, window=self.display_standings_button)

        self.save_to_excel_button = tk.Button(self.canvas, text="Save to Excel", command=self.save_to_excel)
        self.canvas.create_window(600, 30, window=self.save_to_excel_button)

    def create_group(self):
        group_name = self.group_entry.get()
        if group_name and group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
            self.group_combobox['values'] = list(self.groups.keys())
            self.group_combobox_for_teams['values'] = list(self.groups.keys())
            messagebox.showinfo("Success", f"Group '{group_name}' created.")
        elif not group_name:
            messagebox.showerror("Error", "Group name cannot be empty.")
        else:
            messagebox.showerror("Error", f"Group '{group_name}' already exists.")
        self.group_entry.delete(0, tk.END)

    def add_team(self):
        group_name = self.group_combobox_for_teams.get()
        team_name = self.team_entry.get()
        if group_name in self.groups:
            if team_name:
                self.groups[group_name].add_team(team_name)
                if self.group_combobox.get() == group_name:
                    self.update_team_comboboxes(group_name)
                messagebox.showinfo("Success", f"Team '{team_name}' added to group '{group_name}'.")
            else:
                messagebox.showerror("Error", "Team name cannot be empty.")
        else:
            messagebox.showerror("Error", "Group does not exist.")
        self.team_entry.delete(0, tk.END)

    def record_match(self):
        group_name = self.group_combobox.get()
        team1_name = self.team1_combobox.get()
        team1_goals = self.team1_goals_entry.get()
        team2_name = self.team2_combobox.get()
        team2_goals = self.team2_goals_entry.get()

        if group_name in self.groups:
            try:
                team1_goals = int(team1_goals)
                team2_goals = int(team2_goals)
                self.groups[group_name].record_match(team1_name, team1_goals, team2_name, team2_goals)
                messagebox.showinfo("Success", "Match result recorded.")
            except ValueError:
                messagebox.showerror("Error", "Goals must be integers.")
        else:
            messagebox.showerror("Error", "Group does not exist.")

        self.team1_combobox.set('')
        self.team1_goals_entry.delete(0, tk.END)
        self.team2_combobox.set('')
        self.team2_goals_entry.delete(0, tk.END)

    def display_standings(self):
        group_name = self.group_combobox.get()
        if group_name in self.groups:
            standings = self.groups[group_name].display_standings()
            self.standings_text.delete(1.0, tk.END)
            for team in standings:
                self.standings_text.insert(tk.END, str(team) + "\n")
        else:
            messagebox.showerror("Error", "Group does not exist.")

    def update_team_comboboxes(self, group_name):
        teams = list(self.groups[group_name].teams.keys())
        self.team1_combobox['values'] = teams
        self.team2_combobox['values'] = teams

    def on_group_select(self, event):
        group_name = self.group_combobox.get()
        if group_name in self.groups:
            self.update_team_comboboxes(group_name)

    def save_to_excel(self):
        data = []
        for group_name, group in self.groups.items():
            for team in group.teams.values():
                data.append({
                    "Group": group_name,
                    "Team": team.name,
                    "Games Played": team.games_played,
                    "Goals For": team.goals_for,
                    "Goals Against": team.goals_against,
                    "Points": team.points
                })
        df = pd.DataFrame(data)
        df.to_excel("Euro2024_Standings.xlsx", index=False)
        messagebox.showinfo("Success", "Data saved to Excel file 'Euro2024_Standings.xlsx'.")

if __name__ == "__main__":
    app = FootballApp()
    app.mainloop()
