import discord
from discord import app_commands, Interaction

def setup_admin_commands(client, db, save_data):
    @client.tree.command(name="announce", description="Admin use only")
    async def announce(interaction: Interaction, message: str):
        await interaction.response.send_message(message)

    @client.tree.command(name="add_question", description="Admin use only")
    async def add_question(interaction: Interaction, question_number: str, question: str, flag: str):
        author = str(interaction.user)
        if question_number not in db["question"]:
            db["question"][question_number] = {"question": question, "author": author, "flag": [flag]}
            save_data(db)
            embed = discord.Embed(title=f"Question {question_number}", description=question, color=discord.Color.blue())
            embed.set_footer(text=f"Author: {author}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Question already exists")

    @client.tree.command(name="delete_question", description="Admin use only")
    async def delete_question(interaction: Interaction, question_number: str):
        if question_number in db["question"]:
            del db["question"][question_number]
            save_data(db)
            await interaction.response.send_message(f"Question {question_number} deleted")
        else:
            await interaction.response.send_message("Question not found.")

    @client.tree.command(name="data", description="For admin use only")
    async def data(interaction: Interaction):
        username = str(interaction.user)
        if username in ["frenzyvjn", "drunkencloud"]:
            await interaction.response.send_message(str(db))
