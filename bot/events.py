import discord

def setup_events(client, chat):
    @client.event
    async def on_ready():
        await client.tree.sync()
        print(f'We have logged in as {client.user}')
        response = chat.send_message(
            '''You are Edita bot. You are here to assist us with our queries in field of cyberesecurity. 
            You are in a cyber security discord server. Edita bot can do the following!

            (See /bot help for command list)
            '''
        )
        print("ready")

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        await client.process_commands(message)
