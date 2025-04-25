import base64
from discord import app_commands, Interaction

def setup_utility_commands(client):
    @client.tree.command(name="b64", description="Encode (1) and decode (2) base64")
    async def b64(interaction: Interaction, message: str, option: str):
        if option == "encode":
            message = base64.b64encode(message.encode()).decode()
            await interaction.response.send_message(message)
        elif option == "decode":
            message = base64.b64decode(message.encode()).decode()
            await interaction.response.send_message(message)

    @client.tree.command(name="ping", description="Shows the ping!")
    async def ping(interaction: Interaction):
        bot_latency = round(client.latency * 1000)
        await interaction.response.send_message(f"Pong! ... {bot_latency}ms")
