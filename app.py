import os
import discord
import ollama
import functools
import typing
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# THIS IS THE ONE IM USING TODO
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# Initialize instance of Alfie bot
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")

def to_thread(func: typing.Callable) -> typing.Coroutine:
    """
        TODO finish summary
        Threading for blocking functions
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def get_ollama_response(system_content, user_content):
    """
        TODO finish summary
        Learn about generate chat completion for ollama end points...
        Returns the ollama response.
        Is wrapped in a thread to ensure this function finishes and does not block the event loop.
    """
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role' : 'system',
            'content' : system_content
        },
        {
            'role': 'user',
            'content': user_content,
        },
    ])
    return response['message']['content'] 

@to_thread
def ollama_classify(system_content, input_text, categories):
    """
        TODO finish summary
    """
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role' : 'system',
            'content' : system_content
        },
        {
            'role': 'user',
            'messages': [
            {
                'type': 'input',
                'text': input_text
            }
            ],
            'classify': {
                'input_text': input_text,
                'categories': categories
            }
        }
    ])
    return response['message']['content']   

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello! I am Alfie")

@bot.command(name="ask")
#TODO look up on discord docs: ctx, * and message. i know the star is "takes in all parameters"
async def ask(ctx, *, message):
    """
    TODO method summary
    """
    system_content = 'You are a helpful assistant who provides answers to questions concisely in no more than 2000 characters'
    ollama_response = await get_ollama_response(system_content, message)
    await ctx.send(ollama_response)
  

@bot.command(name="summarize")
async def summarize(ctx):
    """
    TODO method summary
    """
    await ctx.send("Summarizing channel history...")
    # NOTE LEARNING:
    # Since the request is async, you need "async for" to iterate over asynchronous iterables or async genorators, 
    # which can yield promises or values asynchronously
    msgs = [ message.content async for message in ctx.channel.history(limit=10) ]

    summarize_prompt = f"""
        Summarize the following messaged delimtied by 3 backticks:
        '''
        {msgs}
        '''
        """
    # TODO Define
    system_content = 'You are a helpful assistant who summarizes the provided messages concisely in no more than 2000 characters'
    ollama_response = await get_ollama_response(system_content, summarize_prompt)
    await ctx.send(ollama_response)

@bot.command(name="yt_tldr")
async def yt_tldr(ctx, url):
    """
    TODO method summary
    """
    await ctx.send("Fetching and summarizing the YouTube video...")
    # Extract the video transcript
    video_id = url.split("v=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([item['text'] for item in transcript_list])

    # TODO make a try catch if the url given is not one that it can use 
    # This is the error given when it isn't split right:
    # video_id = url.split("v=")[1]
    # IndexError: list index out of range

    system_content = '''
                You are a helpful assistant who provides a concise summary of 
                the provided YouTube transcript in bullet points 
                in no more than 2000 characters.
                '''
    ollama_response = await get_ollama_response(system_content, full_transcript)
    await ctx.send(ollama_response)


@bot.command(name="cat")
async def cat(ctx, url):
    """
    TODO method summary
    """
    await ctx.send("Fetching and categorizing the YouTube video...")
    # fetch_channels is an API call and will get most up-to-date list
    # channels attribute will not have latest server changes
    # channels = [ channel.name async for channel in ctx.guild.fetch_channels() ] TODO SEE IF WORKS SAME
    text_channels = [channel for channel in await ctx.guild.fetch_channels() if isinstance(channel, discord.TextChannel)]
    # print(text_channels)

    # Extract the video transcript
    video_id = url.split("v=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([item['text'] for item in transcript_list])

    # TODO make a try catch if the url given is not one that it can use 
    # This is the error given when it isn't split right:
    # video_id = url.split("v=")[1]
    # IndexError: list index out of range

    system_content = '''
                Your role is to analyze a transcript of a YouTube video and
                return one 3-4 word long categorization of that video that
                defines the genre of the video.
                '''
    ollama_response = await get_ollama_response(system_content, full_transcript)
    await ctx.send(ollama_response)

bot.run(os.getenv("DISCORD_TOKEN"))
