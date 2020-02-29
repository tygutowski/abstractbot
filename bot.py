import discord
import requests
import pathlib
import os
import re
from config import *
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient


face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
PATH = pathlib.Path().absolute()
client = discord.Client()


@client.event
async def on_reaction_add(reaction, user):
    if(reaction.count >= DOWNVOTES_REQUIRED):
        await reaction.clear()
        await reaction.message.delete()

@client.event
async def on_message(message):
    if message.author == client.user:
        await message.add_reaction("👎")
        return
    if(message.channel.name == (CHANNEL_NAME)):   
        url = re.findall(r'https?://\S+', message.content.lower()) 
        if(len(url)>0):
            for x in range(0, len(url)):
                url = str(url[x])
                print(message.author.name + "("+str(message.author.id)+") sent a link in bot-testing.")
                img_data = requests.get(url).content
                with open('image.jpg', 'wb') as handler:
                    handler.write(img_data)
        
                    open_image = open((os.path.join(PATH, "image.jpg")),'r+b')
                    faces = face_client.face.detect_with_stream(open_image)
                    if(len(faces)>0):
                        print("Face detected in " + url)
                        await message.channel.send("<@"+str(message.author.id) + '>, it seems you posted an image that has a face.  #' + CHANNEL_NAME + ' is non-representational.  We recommend you delete it and show your work off in another text channel.')
                        break
                        if(len(faces)==0):
                            print("No face detected in " + url)


        if (message.attachments):
            print(message.author.name + "("+str(message.author.id)+") sent an attachment in bot-testing.")
            longattachment = str(message.attachments[0])
            url = longattachment.split('url=')[-1]
            url = url[1:-2]
            img_data = requests.get(url).content
            with open('image.jpg', 'wb') as handler:
                handler.write(img_data)
            
                open_image = open((os.path.join(PATH, "image.jpg")),'r+b')
                faces = face_client.face.detect_with_stream(open_image)
                if(len(faces)>0):
                    print("Face detected in " + url)
                    await message.channel.send("<@"+str(message.author.id) + '>, it seems you posted an image that has a face. #' + CHANNEL_NAME + ' is non-representational.  We recommend you delete it and show your work off in another text channel.')
                    if(len(faces)==0):
                        print("No face detected in " + url)

            
@client.event
async def on_ready():
    print('USER: '+client.user.name)
    print('ID: '+str(client.user.id))
    print('\n')

client.run(TOKEN)