import discord, asyncio, json
from discord.ext import commands


class Embeds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        ## ==> READ VALUES
        with open("Configuration/config.json") as f:
            cfg = json.load(f)
            self.fail_emoji = cfg["fail_emoji"]
            self.success_emoji = cfg["success_emoji"]
            embed_color = cfg["embed_color"]
            self.r = embed_color[0]
            self.g = embed_color[1]
            self.b = embed_color[2]

    @commands.command(
        help="""
` `- **To send Custom Embed to <text_channel>**
` `- You will be prompted for values
` `
` `- **Requires Administrator Permission**
"""
    )
    @commands.has_permissions(administrator=True)
    async def Embed(self, ctx: commands.Context, text_channel: commands.TextChannelConverter) -> None:
        
        ## ==> TITLE OF THE EMBED
        ##############################################################################################
        
        await ctx.send("Enter the title of the Embed:")
        try: 
            title = await self.bot.wait_for("message", timeout=25.0, check=lambda message: message.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
            return
        title = title.content
        
        ##############################################################################################
        
        ## ==> DESCRIPTION OF THE EMBED
        ##############################################################################################
        
        await ctx.send("Enter the Discription of the Embed:")
        
        try:
            description = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
            return
        description = description.content if description.content.strip().lower() != "none" else None
        
        ##############################################################################################
        
        ## ==> NUMBER OF FIELDS OF THE EMBED
        ##############################################################################################
        
        await ctx.send("Enter the Number of Fields in the Embed:")
        try:
            _no_of_fields = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
            return
        try:
            _no_of_fields = int(_no_of_fields.content) if _no_of_fields.content.strip().lower() != "none" else 0
        except ValueError:
            await ctx.send(
                embed=discord.Embed(
                    title="Whoops!",
                    description="Please enter the number of fields in an Integer format!\nExiting Command; Please run the command again",
                    color=discord.Color.from_rgb(46,49,54)
                )
            )
            
            return
        
        ##############################################################################################
        
        ## ==> PROMPT FOR FIELDS
        ##############################################################################################
        
        fields = []
        
        for i in range(_no_of_fields):
            ## ==> HEAD OF THE FIELD
            ##############################################################################################
            
            await ctx.send(f"Enter Head of Field {i+1}:")
            try:
                f_head = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
                return
            f_head = f_head.content
            
            ##############################################################################################
            
            ## ==> VALUE OF FIELD
            ##############################################################################################
            
            await ctx.send(f"Enter Value of Field {i+1}:")
            try:
                f_value = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
                return
            f_value = f_value.content
            
            ## ==> INLINE OR NOT
            ##############################################################################################
            
            await ctx.send(f"Is Field {i+1} inline? (y/n):")
            try:
                f_inline = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
                return
            f_inline = True if f_inline.content.strip().lower() == 'y' else False
            
            ##############################################################################################
            
            ##############################################################################################
            
            ## ==> APPEND FIELD HEAD AND FIELD VALUE AS A TUPLE
            ##############################################################################################
            
            fields.append((f_head, f_value, f_inline))
            
            ##############################################################################################
            
        ##############################################################################################         
            
        ## ==> FOOTER OF THE EMBED
        ##############################################################################################
        
        await ctx.send("Enter Footer of the Embed:")
        try:
            footer = await self.bot.wait_for("message", timeout=25.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(f"Exiting command as {ctx.author.name} didn't respond in time")
            return
        footer = footer.content if footer.content.strip().lower() != "none" else None
        
        ##############################################################################################
        
        ## ==> SENDING THE EMBED
        ##############################################################################################
        
        if description is not None: 
            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.from_rgb(self.r, self.g, self.b)
            )
        else:
            embed=discord.Embed(
                title=title,
                color=discord.Color.from_rgb(self.r, self.g, self.b)
            )
        if footer is not None:
            embed.set_footer(text=footer)
        for i in fields: embed.add_field(name=i[0], value=i[1], inline=i[2])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        channel = self.bot.get_channel(text_channel.id)
        await channel.send(embed=embed)
        
        ##############################################################################################
        

def setup(bot:commands.Bot) -> None:
    bot.add_cog(Embeds(bot))