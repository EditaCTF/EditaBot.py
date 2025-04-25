import discord
from discord import app_commands, Interaction

def setup_question_commands(client, db, save_data):
    @client.tree.command(name="display_all_questions", description="Displays all question numbers available")
    async def display_all_questions(interaction: Interaction):
        question_numbers = list(db["question"])
        if not question_numbers:
            await interaction.response.send_message("No questions found.")
            return
        embed = discord.Embed(title="All Question Numbers", color=discord.Color.blue())
        question_list = "\n".join(question_numbers)
        embed.add_field(name="Question Numbers", value=question_list)
        await interaction.response.send_message(embed=embed)

    @client.tree.command(name="display_question", description="Displays question")
    async def display_question(interaction: Interaction, question_number: str):
        question_dict = db["question"]
        if question_number in question_dict:
            question = question_dict[question_number]["question"]
            author = question_dict[question_number]["author"]
            embed = discord.Embed(title=f"Question {question_number}", description=question, color=discord.Color.blue())
            embed.set_footer(text=f"Author: {author}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Question {question_number} not found")

    @client.tree.command(name="flag", description="Submit your flag")
    async def flag(interaction: Interaction, task: str, flag: str):
        if flag.startswith("flag{") and flag.endswith("}"):
            username = str(interaction.user)
            team_name = db["user_details"][username]["team"]
            if team_name == []:
                await interaction.response.send_message("You are not in a team", ephemeral=True)
                return
            if flag == db["question"][task]["flag"][0]:
                await interaction.response.send_message("Your flag is correct!", ephemeral=True)
                if task not in db["user_details"][username]["qs"]:
                    db["user_details"][username]["qs"].append(task)
                    db["user_details"][username]["score"] += 1
                    team_name = db["user_details"][username]["team"][0]
                    team_members = db["teams"][team_name]["members"]
                    counted_questions = db["teams"][team_name]["qs"]
                    for member in team_members:
                        if member in db["user_details"]:
                            member_scores = db["user_details"][member]["qs"]
                            for question in member_scores:
                                if question not in counted_questions:
                                    counted_questions.append(question)
                    save_data(db)
            else:
                await interaction.response.send_message("Incorrect flag. Try again!", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid flag format. Make sure it starts with 'flag{' and ends with '}'.", ephemeral=True)
