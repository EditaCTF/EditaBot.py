def setup_leaderboard_commands(client, db):
    @client.tree.command(name="score", description="Check your score")
    async def score(interaction, username: str):
        if username in db["user_details"]:
            user_score = db["user_details"][username]["score"]
            await interaction.response.send_message(f"Your score is {user_score}")
        else:
            await interaction.response.send_message("User not found. Please make sure you have submitted at least one flag.")

    @client.tree.command(name="leaderboard", description="To display leaderboard")
    async def leaderboard(interaction):
        users = db["user_details"]
        if not users:
            await interaction.response.send_message("No users found.")
            return
        leaderboard_text = "User Leaderboard:\n"
        sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
        for user_name, user_data in sorted_users:
            user_score = user_data["score"]
            leaderboard_text += f"{user_name}: {user_score} points\n"
        await interaction.response.send_message(leaderboard_text)

    @client.tree.command(name="team_leaderboard", description="To display team leaderboard")
    async def team_leaderboard(interaction):
        teams = db["teams"]
        if not teams:
            await interaction.response.send_message("No teams found.")
            return
        leaderboard_text = "Team Leaderboard:\n"
        for team_name, team_data in teams.items():
            team_members = team_data["members"]
            total_team_score = 0
            counted_questions = set()
            for member in team_members:
                if member in db["user_details"]:
                    member_scores = db["user_details"][member]["qs"]
                    for question in member_scores:
                        if question not in counted_questions:
                            total_team_score += 1
                            counted_questions.add(question)
            leaderboard_text += f"{team_name}: {total_team_score} points\n"
        await interaction.response.send_message(leaderboard_text)
