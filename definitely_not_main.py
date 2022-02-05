import asyncio

import discord
from discord.ext import commands
import pandas as pd
import numpy as np
Intents = discord.Intents.all()
bot = commands.Bot(command_prefix="V!", description="This is a TTAV Cleanup bot",intents = Intents)



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,  * , reason: str="Definitely afk "):

    roles_dict={}

    df = pd.DataFrame(np.nan, index=[0], columns=['ROLE_NAME','ROLE_ID'])

    for role_srv in ctx.guild.roles:
        i =1
        df.loc[len(df.index)] = [str(role_srv.name), str(role_srv.id)]
        i+=1




    df = df.iloc[2: , :].reset_index(drop=True)



    embed_role_msg=discord.Embed(title="Roles List !",description=f"There are the following Roles in the server : ",  color=0xa53df0) #purple is life
    embed_role_msg.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar_url)
    embed_role_msg.set_thumbnail(url="https://www.timevillains.xyz/assets/MAIN_VILLAIN_STROKE%201.732accfc.png") #A TTAV Pic

    dict_len =  len(df.index)
    print(df)
    for index in range(0,dict_len):
        embed_role_msg.add_field(name="\u200b", value=f"{ str(index) + ' : ' + str(df['ROLE_NAME'][index])}", inline=False)


    embed_role_msg.add_field(name="Please Type the corresponding number to select the role you want", value="\u200b", inline=False)

    embed_role_msg.set_footer(text="Kick command requested by: {}".format(ctx.author.display_name))

    message = await ctx.send(embed = embed_role_msg)
    channel  = message.channel.id
    global Chosen_index
    def check(m):
        int(m.content)
        if m.author != ctx.author:
            return False

        try:
            int(m.content)  # if the value typed by the user is a number, then it passes
            global Chosen_index
            Chosen_index = int(m.content)
            return True

        except ValueError:
            return False

    try:


        msg = await bot.wait_for('message', check=check, timeout=30)
        Chosen_Role_Name = df.iloc[Chosen_index,0]
        Chosen_Role_ID = df.iloc[Chosen_index,1]

        try:
            if Chosen_index in range(0,dict_len):


                embed=discord.Embed(title="Confirmation !",description=f"You are about to delete any user without the follow role(s) : {Chosen_Role_Name}",  color=0xa53df0) #purple is life
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
                    else:
                        return False



                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=7.0, check=check)


                except :
                    await ctx.reply("Command canceled")
                else:
                    Counter = 0
                    members = ctx.guild.members
                    for member in  members:
                        if not member.bot:
                            if (Chosen_Role_ID not in member.roles) : # does member have the specified role?
                                await ctx.guild.kick(member, reason=reason)
                                Counter+=1
                    await ctx.reply( str(Counter) + " Users kicked!   **Evil laugh intensifies!** ")
                    Counter = 0

            else:
                await ctx.reply("Please write the corresponding number from the choices above")
        except Exception:
            await ctx.reply("Please write a **number** within the scope of the given numbers above")

    except ValueError:
        await ctx.reply("Value error ! please type only the **number** corresponding to your choice")
    except   Exception:
        await ctx.reply("Command Canceled, please re use the kick command to start another operation")









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