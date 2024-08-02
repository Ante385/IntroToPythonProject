import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os

# Define the blue color for BG Image
blue_color_hex = '#143cda'


def read_standings(excel_file):
    if not os.path.isfile(excel_file):
        print(f"File not found: {excel_file}")
        return None, None

    try:
        df = pd.read_excel(excel_file)
        print("Excel file content:")
        print(df)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return None, None

    groups = df.groupby('Group')
    top_teams = {}
    third_placed_teams = []

    for name, group in groups:
        group_key = name.strip().upper()[-1]  # Normalize the group key to a single letter
        sorted_group = group.sort_values(by=['Points', 'Goals For', 'Goals Against'], ascending=[False, False, True])
        print(f"Group {group_key} sorted by Points:")
        print(sorted_group)
        if len(sorted_group) >= 3:
            top_teams[group_key] = [sorted_group.iloc[0]['Team'], sorted_group.iloc[1]['Team']]
            third_placed_teams.append(sorted_group.iloc[2])
        elif len(sorted_group) == 2:
            top_teams[group_key] = [sorted_group.iloc[0]['Team'], sorted_group.iloc[1]['Team']]
        else:
            print(f"Group {group_key} does not have enough teams.")
            return None, None

    print("Third placed teams before sorting:")
    for team in third_placed_teams:
        print(team)

    # Sort third-placed teams by points and other criteria, then select the top 4
    third_placed_teams = sorted(third_placed_teams, key=lambda x: (x['Points'], x['Goals For'], -x['Goals Against']),
                                reverse=True)[:4]

    print("Third placed teams after sorting and selecting top 4:")
    for team in third_placed_teams:
        print(team)

    # Take teams names for third-placed teams
    top_third_teams = [team['Team'] for team in third_placed_teams]

    print("Top teams advancing to knockout stage:")
    for group, teams in top_teams.items():
        print(f"Group {group}: {teams}")

    print("Top third-placed teams advancing to knockout stage:")
    print(top_third_teams)

    return top_teams, top_third_teams


def map_knockout_matchups(top_teams, top_third_teams):
    if len(top_third_teams) < 4:
        print("Not enough third-placed teams to form the round of 16.")
        return None

    # Define the fixed matchups due to complication in UEFA rules
    matchups = [
        ("Spain", "Georgia"),
        ("Germany", "Denmark"),
        ("Portugal", "Slovenia"),
        ("France", "Belgium"),
        ("Netherlands", "Romania"),
        ("Austria", "Turkey"),
        ("England", "Slovakia"),
        ("Switzerland", "Italy")
    ]

    return matchups


class KnockoutStageApp(tk.Tk):
    def __init__(self, excel_file, bg_image_path):
        super().__init__()
        self.title("Euro2024 Knockout Stage")
        self.geometry("1600x900")
        self.round_labels = []

        self.bg_image_path = bg_image_path
        self.bg_image = Image.open(self.bg_image_path)
        self.bg_image = ImageTk.PhotoImage(self.bg_image.resize((1600, 900), Image.LANCZOS))

        top_teams, top_third_teams = read_standings(excel_file)

        if not top_teams or not top_third_teams or (len(top_teams) * 2 + len(top_third_teams)) < 16:
            messagebox.showerror("Error", "Not enough teams to form the round of 16.")
            self.quit()
        else:
            self.knockout_matchups = map_knockout_matchups(top_teams, top_third_teams)
            if self.knockout_matchups is None:
                messagebox.showerror("Error", "Failed to form knockout matchups.")
                self.quit()
            else:
                self.create_widgets()

    def create_widgets(self):
        # Set up the main frame and scrollbar
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame, width=1600, height=900)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=blue_color_hex)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas = canvas
        self.scrollable_frame = scrollable_frame

        # Create labels for initial matchups based on knockout_matchups
        self.match_labels = []
        self.result_entries = []
        self.vs_labels = []
        self.round_positions = {"Round of 16": 0, "Quarter-finals": 1, "Semi-finals": 2, "Final": 3}

        self.create_match_labels(self.knockout_matchups, round_name="Round of 16", column=0)

        # Button to record match results and update the next stage
        self.record_button = tk.Button(self.scrollable_frame, text="Record Results",
                                       command=lambda: self.record_results(self.knockout_matchups, 1),
                                       bg=blue_color_hex, fg='white')
        self.record_button.grid(row=2 + len(self.knockout_matchups), column=0, columnspan=5, pady=20)

        # Create a frame for the winner label
        self.winner_frame = tk.Frame(self, bg=blue_color_hex)
        self.winner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the winner frame

    def create_match_labels(self, match_positions, round_name, column):
        self.round_labels.append(round_name)
        round_label = tk.Label(self.scrollable_frame, text=round_name, font=("Helvetica", 16, "bold"), bg=blue_color_hex, fg='white')
        round_label.grid(row=0, column=column, padx=20, pady=20)

        for i, (team1, team2) in enumerate(match_positions):
            print(f"Creating label for match: {team1} vs {team2}")  # Debug information
            label = tk.Label(self.scrollable_frame, text=f"{team1} vs {team2}", font=("Helvetica", 14), bg=blue_color_hex, fg='white')
            entry1 = tk.Entry(self.scrollable_frame, width=5, bg='white')
            vs_label = tk.Label(self.scrollable_frame, text="vs", font=("Helvetica", 14), bg=blue_color_hex, fg='white')
            entry2 = tk.Entry(self.scrollable_frame, width=5, bg='white')

            label.grid(row=1 + i, column=column, padx=20, pady=5)
            entry1.grid(row=1 + i, column=column + 1, padx=5, pady=5)
            vs_label.grid(row=1 + i, column=column + 2, padx=5, pady=5)
            entry2.grid(row=1 + i, column=column + 3, padx=5, pady=5)

            self.match_labels.append(label)
            self.result_entries.append((entry1, entry2))
            self.vs_labels.append(vs_label)

    def record_results(self, match_positions, stage):
        winners = []
        start_index = len(self.result_entries) - len(match_positions)
        for i in range(len(match_positions)):
            entry1, entry2 = self.result_entries[start_index + i]
            team1_goals = entry1.get()
            team2_goals = entry2.get()

            try:
                team1_goals = int(team1_goals)
                team2_goals = int(team2_goals)
            except ValueError:
                messagebox.showerror("Error", "Goals must be integers.")
                return

            if team1_goals > team2_goals:
                winners.append(match_positions[i][0])
            elif team2_goals > team1_goals:
                winners.append(match_positions[i][1])
            else:
                messagebox.showerror("Error", "There must be a winner.")
                return

        print("Winners advancing to next stage:", winners)  # Debug information

        if stage == 1:
            self.update_next_stage(winners, "Quarter-finals", 5, stage + 1)
        elif stage == 2:
            self.update_next_stage(winners, "Semi-finals", 10, stage + 1)
        elif stage == 3:
            self.update_next_stage(winners, "Final", 15, stage + 1)
        else:
            self.show_winner(winners[0])

        self.make_entries_noneditable(self.result_entries[start_index:start_index + len(match_positions)])

    def make_entries_noneditable(self, entries):
        for entry1, entry2 in entries:
            entry1.config(state="disabled")
            entry2.config(state="disabled")

    def update_next_stage(self, winners, round_name, column, next_stage):
        if len(winners) == 8:
            match_positions = [
                (winners[0], winners[1]), (winners[2], winners[3]),
                (winners[4], winners[5]), (winners[6], winners[7])
            ]
            self.create_match_labels(match_positions, round_name=round_name, column=column)
            self.record_button.config(command=lambda: self.record_results(match_positions, next_stage))

        elif len(winners) == 4:
            match_positions = [
                (winners[0], winners[1]), (winners[2], winners[3])
            ]
            self.create_match_labels(match_positions, round_name=round_name, column=column)
            self.record_button.config(command=lambda: self.record_results(match_positions, next_stage))

        elif len(winners) == 2:
            match_positions = [
                (winners[0], winners[1])
            ]
            self.create_match_labels(match_positions, round_name=round_name, column=column)
            self.record_button.config(command=lambda: self.record_results(match_positions, next_stage))

    def show_winner(self, winner):
        winner_label = tk.Label(self.winner_frame, text=f"The winner is {winner}!", font=("Helvetica", 36, "bold"), bg=blue_color_hex, fg='white')
        winner_label.pack()


if __name__ == "__main__":
    excel_file = "Euro2024_Standings.xlsx"  # Path to the uploaded file
    bg_image_path = "Euro2024_BG_Knockouts.jpg"  # Path to background image
    app = KnockoutStageApp(excel_file, bg_image_path)
    app.mainloop()
