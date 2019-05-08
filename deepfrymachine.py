import discord
import sys
import requests
import subprocess

client = discord.Client()

escape_character = "/df"

class fry_machine(discord.Client):

    @client.event
    async def on_ready(self):
        print('Logged on as {}!'.format(self.user))

    @client.event
    async def on_message(self, message):
        if message.author == self.user:
            return

        #if message.content.startswith(escape_character):
        for attachment in message.attachments:

            message_image = requests.get(attachment.url)
            answer_image_path = "/tmp/{}".format(attachment.filename)

            self.fry(message_image, attachment.filename)


    async def fry(self, image, filename):
        path = '/tmp/{}'.format(filename)
        input_file = open(path, 'w')
        await input_file.write(image)
        input_file.close()

        await subprocess.run("bash -c ./fry.sh /tmp/{}".format(filename))

        output_file = open(path, 'w')
        await output_file.write(output_image)

        if successful:
            await message.channel.send("Deepfried image, as requested by {0}.".format(message.author), file=output_file)
        else:
            await message.channel.send("Something went wrong for {0}'s requested image".format(message.author))

        output_file.close()

        await os.remove(path)


token_file = open('token.txt')
token = token_file.readlines()[0].strip("\n")
token_file.close()

# Deep Fry Machine
dfm = fry_machine()
dfm.run(token)
