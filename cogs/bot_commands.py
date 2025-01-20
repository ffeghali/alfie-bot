import discord
from discord.ext import commands
from services import ollama_service, web_scrape_service

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send("Hello! I am Alfie")

    @commands.command(name="ask")
    async def ask(self, ctx, *, message):
        """
        Gets response from Ollama model.
        """
        system_content = 'You are a helpful assistant who provides answers to questions concisely in no more than 2000 characters'
        ollama_response = await ollama_service.get_response(system_content, message)
        await ctx.send(ollama_response)

    @commands.command(name="summarize")
    async def summarize(self, ctx):
        """
        Summarizes recent messages from the channel the user sent the command from.
        """
        await ctx.send("Summarizing channel history...")
        
        # Since the request is async, you need "async for" to iterate over asynchronous iterables or async genorators, 
        # which can yield promises or values asynchronously
        most_recent_messages = [ message.content async for message in ctx.channel.history(limit=10) ]

        system_content = 'You are a helpful assistant who summarizes the provided messages concisely in no more than 2000 characters'
        summarize_prompt = f"""
            Summarize the following messaged delimtied by 3 backticks:
            '''
            {most_recent_messages}
            '''
            """
        ollama_response = await ollama_service.get_response(system_content, summarize_prompt)
        await ctx.send(ollama_response)

    @commands.command(name="yt_tldr")
    async def yt_tldr(self, ctx, url):
        """
        Summarizes the given YouTube video's transcript.
        """
        await ctx.send("Fetching and summarizing the YouTube video...")
        
        try:
            full_transcript = web_scrape_service.get_yt_transcript(url)
        except Exception as e:
            await ctx.send(f"Error processing video. Please ask again and provide a different link.")
            print(str(e))
        else:
            system_content = '''
                        You are a helpful assistant who provides a concise summary of 
                        the provided YouTube transcript in bullet points 
                        in no more than 2000 characters.
                        '''
            ollama_response = await ollama_service.get_response(system_content, full_transcript)
            await ctx.send(ollama_response)


    @commands.command(name="cat")
    async def cat(self, ctx, url):
        """
        TODO method in works... tbd
        """
        await ctx.send("Fetching and categorizing the YouTube video...")
        # fetch_channels is an API call and will get most up-to-date list
        # channels attribute will not have latest server changes
        text_channels = [channel for channel in await ctx.guild.fetch_channels() if isinstance(channel, discord.TextChannel)]
        # print(text_channels)

        full_transcript = web_scrape_service.get_yt_transcript(url)

        # TODO asking via the chat api, no matter what i put in the system_content, 
        #   it is unable to put the video into one distinct genre... need to try something else
        system_content = '''
                    Your role is to analyze a transcript of a YouTube video and
                    return one 3-4 word long categorization of that video that
                    defines the genre of the video.
                    '''
        ollama_response = await ollama_service.get_response(system_content, full_transcript)
        await ctx.send(ollama_response)

async def setup(bot):
    await bot.add_cog(BotCommands(bot))