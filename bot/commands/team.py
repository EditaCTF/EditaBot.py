import discord
from discord import app_commands, Interaction

def setup_team_commands(client, db, save_data):
    @client.tree.command(name="create_team", description="To create team")
    async def create_team(interaction: Interaction, team_name: str, password: str):
        username = str(interaction.user)
        teams = db["teams"]
        if username not in db["user_details"]:
            db["user_details"][username] = {"score": 0, "qs": [], "team": [], "cash": 0}
        if team_name not in teams:
            if db["user_details"][username]["team"] == []:
                guild = interaction.guild
                team_role = await guild.create_role(name=team_name)
                await team_role.edit(mentionable=True)
                teams[team_name] = {"members": [username], "password": [password], "score": 0, "qs": [], "role_id": team_role.id, "team_cash": 0}
                db["user_details"][username]["team"].append(team_name)
                await interaction.user.add_roles(team_role)
                save_data(db)
                await interaction.response.send_message(f"Team {team_name} created successfully", ephemeral=True)
            else:
                await interaction.response.send_message("You are already in a team", ephemeral=True)
        else:
            await interaction.response.send_message(f"Team {team_name} already exists")

    @client.tree.command(name="join_team", description="To join team")
    async def join_team(interaction: Interaction, team_name: str, password: str):
        username = str(interaction.user)
        teams = db["teams"]
        if username not in db["user_details"]:
            db["user_details"][username] = {"score": 0, "qs": [], "team": [], "cash": 0}
            save_data(db)
        if team_name in teams:
            if db["user_details"][username]["team"] == []:
                team_members = teams[team_name]["members"]
                cpassword = teams[team_name]["password"][0]
                team_role_id = teams[team_name]["role_id"]
                if username not in team_members:
                    if cpassword == password:
                        guild = interaction.guild
                        user = interaction.user
                        team_role = guild.get_role(team_role_id)
                        if team_role:
                            await user.add_roles(team_role)
                        team_members.append(username)
                        db["user_details"][username]["team"].append(team_name)
                        save_data(db)
                        await interaction.response.send_message(f"You have joined team {team_name}")
                    else:
                        await interaction.response.send_message("Incorrect password. Please try again.", ephemeral=True)
                else:
                    await interaction.response.send_message("User already exists in the team")
            else:
                await interaction.response.send_message("You are already in a team", ephemeral=True)
        else:
            await interaction.response.send_message(f"Team {team_name} not found")

    @client.tree.command(name="leave_team", description="To leave team")
    async def leave_team(interaction: Interaction, team_name: str):
        username = str(interaction.user)
        teams = db["teams"]
        if team_name in teams:
            team_members = teams[team_name]["members"]
            if username in team_members:
                guild = interaction.guild
                team_role_id = teams[team_name]["role_id"]
                team_role = guild.get_role(team_role_id)
                if team_role:
                    await interaction.user.remove_roles(team_role)
                team_members.remove(username)
                db["user_details"][username]["team"].remove(team_name)
                save_data(db)
                await interaction.response.send_message(f"You have left team {team_name}")
            else:
                await interaction.response.send_message(f"User not found in team {team_name}")
        else:
            await interaction.response.send_message(f"Team {team_name} not found")

    @client.tree.command(name="delete_team", description="To delete team")
    async def delete_team(interaction: Interaction, team_name: str):
        username = str(interaction.user)
        teams = db["teams"]
        if username in ["frenzyvjn", "drunkencloud", "hotaru_hspr"]:
            if team_name in teams:
                team_members = teams[team_name]["members"]
                for member in team_members:
                    if member in db["user_details"] and team_name in db["user_details"][member]["team"]:
                        db["user_details"][member]["team"].remove(team_name)
                guild = interaction.guild
                team_role_id = teams[team_name]["role_id"]
                team_role = guild.get_role(team_role_id)
                if team_role:
                    await team_role.delete()
                del teams[team_name]
                save_data(db)
                await interaction.response.send_message(f"Team {team_name} deleted successfully")
            else:
                await interaction.response.send_message(f"Team {team_name} not found")
