import asyncio

import discord
from discord.ext import commands

Intents = discord.Intents.all()
bot = commands.Bot(command_prefix="V!", description="This is a TTAV Cleanup bot",intents = Intents)



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, role: discord.Role , reason: str="Definitely afk "):


    embed=discord.Embed(title="Confirmation !",description=f"You are about to delete any user without the follow role(s) : {role}",  color=0xa53df0) #purple is life
    embed.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar_url
    )
    embed.set_thumbnail(url="https://www.timevillains.xyz/assets/MAIN_VILLAIN_STROKE%201.732accfc.png") #A TTAV Pic
    embed.set_footer(text="Kick command requested by: {}".format(ctx.author.display_name))

    message = await ctx.send(embed = embed)

    await message.add_reaction('✅')
    await message.add_reaction('❌')
    msg_id = message.id

    def check(reaction, user):
        if(user == ctx.author and str(reaction.emoji) == '✅'):
            return True

        if(user == ctx.author and str(reaction.emoji) == '❌'):

            return False


    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=3.0, check=check)


    except :
        await ctx.reply("Command canceled")
        return
    else:
        Counter = 0
        members = ctx.guild.members
        for member in  members:
            if not member.bot:
                if (role not in member.roles) : # does member have the specified role?
                    await ctx.guild.kick(member, reason=reason)
                    Counter+=1
        await ctx.reply( str(Counter) + " Users kicked!   **Evil laugh intensifies!** ")
        Counter = 0





@kick.error
async def kick_error(ctx: commands.Context, error: commands.CommandError):

    if isinstance(error, commands.RoleNotFound):
        message = f"This role isnt found , please tag the correct Role"
    elif isinstance(error, commands.MissingPermissions):
        message = "You need to be an administrator to use such commands"
    elif isinstance(error, commands.MissingRequiredArgument):
        message = f"Missing a required argument: Role"
    elif isinstance(error, commands.ConversionError):
        message = str(error)
    else:
        message = "Oh no! Something went wrong while running the command!"




@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="timevillains.xyz"))
    print('Loading Evil : 10000%')

async def on_message(self, message):
    if message.author == self.user: #Avoid replying to his own message
        return


bot.run(TOKEN_HERE)