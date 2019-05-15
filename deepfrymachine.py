import discord
import sys
import requests
from subprocess import call
import os
import shutil
import threading
from imgfry import frier

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

            print("creating fry thread")
            thread = threading.Thread(None, self.fry, None, (message, attachment))
            thread.run()


    def fry(self, message, attachment):

        answer_image_path = "/tmp/{}".format(attachment.filename)
        filename = attachment.filename

        # download the image
        image = requests.get(attachment.url)

        # write it to a tmp file
        print("download the following image and write it to a tmp file\n" + image.url + "\n/tmp/" + filename)
        input_file_path = "/tmp/" + filename
        if image.status_code == 200:
            with open(input_file_path, 'wb') as f:
                f.write(image.content)

        # fry it and specify output path for fried image
        # make sure to open file in binary mode "wb"
        output_filename = filename + "_fried" + filename.split(".")[-1]
        output_file_path = filename + "/tmp/" + output_filename
        print("Opening frying process")

        frier.fry()

        returncode = call(["bash", "-c", "./fry.sh", input_file_path, output_file_path])

        # if it was successful, send the image to the channel where the message came in
        print("return code of conversion: " + str(returncode))
        """
        if returncode == 0:
            # send the image as an attachment, if that not works try the other way and send it seperate
            message.channel.send("Deepfried image, as requested by {0}.".format(message.author), file=output_file_path)
            # client.send_file(message.channel, '/tmp/{}_fried.png')
        else:
            message.channel.send("Something went wrong for {0}'s requested image".format(message.author))

        # remove files created earlier (clean up)

        os.remove(input_file_path, output_file_path)
        """


# read token from file
token_file = open('token.txt')
token = token_file.readlines()[0].strip("\n")
token_file.close()

# start the fry machine
dfm = fry_machine()
dfm.run(token)
