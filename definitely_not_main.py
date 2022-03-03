import asyncio
import datetime

import discord
from discord.ext import commands
import pandas as pd
import numpy as np
import pandas as pd
import openpyxl

Intents = discord.Intents.all()
bot = commands.Bot(command_prefix="V!", description="This is a TTAV Cleanup bot",intents = Intents)



@bot.command(brief='Kick all users who dont have a specific role  ! BE CAREFUL WHEN USING THIS ! ', description=" 'V!kick")
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



@bot.command(brief=" first tag all the whitelist roles in one message, then tag all the free mint roles in another message", description=" V!fetch")
async def fetch(ctx):
    channel = ctx.channel

    #WHITELIST ROLES SECTION

    Step1_embed=discord.Embed(title="STEP 1/2",

                              description=" ",
                              color=discord.Color.purple())

    Step1_embed.set_thumbnail(url="https://www.timevillains.xyz/assets/WATCHDOGMAN%201.2453fe5b.png")

    Step1_embed.add_field(name="WHITELIST Role(s):" ,value="Please tag all the *Whitelist Roles* **in one message** ")

    await ctx.reply(embed=Step1_embed)


    WhitelistRoles=[]

    User_List = pd.DataFrame(columns=['Discord Username','Whitelist', 'Free Mint'])


    def checkWhitelist(m):
        return m.author == ctx.author and m.channel == channel


    try:
        msg = await bot.wait_for('message', check=checkWhitelist,timeout=20)

        WLTempList= msg.content.split(' ')


        #Data Handling :

        for role in WLTempList:
            WhitelistRoles.append(role[3:-1])

    except asyncio.TimeoutError:
        ctx.reply('You took too much time replying ! please use **V!fetch** again to restart')

    #FREE MINT ROLES SECTION

    FmRoles = []

    Step2_embed=discord.Embed(title="STEP 2/2",

                              description=" ",
                              color=discord.Color.from_rgb(255,184,191))

    Step2_embed.set_thumbnail(url="https://timevillains.xyz/assets/CYBORG_BLUE%201.9aea7354.png")

    Step2_embed.add_field(name="FREE MINT Role(s):" ,value="Now tag all the **Free Mint** Roles *in one message* ")

    await ctx.reply(embed=Step2_embed)


    def CheckFm(m):
        return m.author == ctx.author and m.channel == channel


    try:
        msg = await bot.wait_for('message', check=CheckFm , timeout=20)

        FmTempList= msg.content.split(' ')





    #Data Handling :

        for role in FmTempList:
            FmRoles.append(role[3:-1])

    except asyncio.TimeoutError:
        ctx.reply('You took too much time replying ! please use **V!fetch** again to restart')


    #Some trolling (disclaimer : this is a joke , pls dont sue me)


    trolling = await ctx.reply('Commencing Operation')
    await asyncio.sleep(0.2)
    await trolling.edit(content="Commencing Operation. (1/4) ")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Commencing Operation.. (1/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Commencing Operation... (1/4)")
    await asyncio.sleep(1)


    await trolling.edit(content="Awaiting Data (2/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Awaiting Data. (2/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Awaiting Data.. (2/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Awaiting Data... (2/4)")
    await asyncio.sleep(0.2)








    global line
    global WL_Status
    global FM_Status

    Global_members = ctx.guild.members
    for member in Global_members:
        index=0
        global line
        line = {}

        WL_Status= False
        FM_Status= False

        for Member_Role in member.roles:

            for Role in WhitelistRoles:

                if str(Role) == str(Member_Role.id):

                    line = {'Discord Username':[member],'Whitelist':['yes']}
                    WL_Status = True
                    break



            for FRole in FmRoles:

                if str(FRole) == str(Member_Role.id):
                        if(WL_Status):
                            line = {'Discord Username':[member],'Whitelist':['yes'],'Free Mint':['yes']}




                            FM_Status=True

                            break
                        else:


                            line =  {'Discord Username': [member],'Whitelist': ['No'],'Free Mint':['yes']}
                            FM_Status= True
                            break



                else:
                    if(WL_Status):
                        line = {'Discord Username': [member],'Whitelist': ['yes'],'Free Mint':['no']}
                        break


            if(WL_Status or FM_Status):
                dummy_df= pd.DataFrame(line)
                User_List = pd.concat([User_List,dummy_df],ignore_index = True)




    User_List = User_List.drop_duplicates(subset=['Discord Username'],ignore_index = True)






    await trolling.edit(content="robbing a bank. (3/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="robbing a bank.. (3/4)")
    #await asyncio.sleep(0.3)
    await trolling.edit(content="robbing a bank... (3/4)")
    await asyncio.sleep(0.5)

    User_List.to_excel('TTAV_WL_FreeMint.xlsx')

    await trolling.edit(content="Making TTAV great again (4/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Making TTAV great again. (4/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Making TTAV great again.. (4/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Making TTAV great again... (4/4)")
    await asyncio.sleep(0.2)
    await trolling.edit(content="Finished! Here is the file :")

    await ctx.channel.send(file=discord.File('TTAV_WL_FreeMint.xlsx'))



@bot.command(brief="You input the desired channel to send a msg to then the  list of users and it's send to the channel ", description="V!say #tag_channel")
async def say(ctx, channel: discord.TextChannel):


    def emb(nm, val):

        embed_general = discord.Embed(title="Confirmation", description=" ", color=discord.Color.purple())
        embed_general.set_thumbnail(url="https://www.timevillains.xyz/assets/MAIN_VILLAIN_STROKE%201.732accfc.png")

        embed_general.add_field(name=nm, value=val)

        embed_general.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        return embed_general


    embed_1 = emb("Please Type the List Of usernames + discriminant Ex: User#0000",
                  "Please type in the list of users you want to tag , (it can be in multiple messages if you want. * Please Write: **ready** when you write all the users* ")

    await ctx.send(embed=embed_1)

    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me


    def checkyes(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me

    Unmentionned=[]
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)

        all_users = msg.content

        while( str(msg.content).lower() != "ready"):
            curr_msg = await bot.wait_for('message', check=check, timeout=60)

            if( str(curr_msg.content).lower() == 'ready'):
                break

        all_users = all_users + '\n' + curr_msg.content


        final = str(all_users).split('\n')
        user_dict={}
        for user in final:
            try:
                temp = user.split('#')
                temp_dict = { temp[0]: temp[1] }
                user_dict.update(temp_dict)

            except Exception:
                Unmentionned.append(user)

        message = []

        for userdisc in user_dict:

            user_mention=[]
            try:
                userdc = discord.utils.get( ctx.author.guild.members, name=userdisc, discriminator=user_dict[userdisc] )
                user_mention = f'<@{userdc.id}>'
                message.append(user_mention)


            except Exception:
                Unmentionned = Unmentionned + [f' {userdisc}#{user_dict[userdisc]}']






        global already_send
        already_send= False
        if  Unmentionned!=[]:   #if the list is empty

                embed_warning = discord.Embed(title="Warning", description=" ", color=discord.Color.dark_red())
                embed_warning.set_thumbnail(url="https://www.timevillains.xyz/assets/MAIN_VILLAIN_STROKE%201.732accfc.png")

                embed_warning.add_field(name="The following users dont exist in the server anymore, the wont be mentionned in the message : ", value="----------", inline=False)
                i=1
                for unexisting_user in Unmentionned:

                    embed_warning.add_field(name=f'{i}', value=f"{unexisting_user}",inline=False)

                    i+=1

                embed_warning.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)


        embed_warning.add_field(name="Note: ", value="Type **Yes** to continue!")

        embed_warning.timestamp = datetime.datetime.utcnow()
        embed_warning.set_footer(text='\u200b',icon_url="https://i.imgur.com/uZIlRnK.png")

        await ctx.send(embed=embed_warning)


        try:
                    confirmation_final = await bot.wait_for('message', check=checkyes, timeout=60)


                    while( (str(confirmation_final.content).lower() != "yes") or (str(confirmation_final.content).lower() == "no")):
                        confirmation_final = await bot.wait_for('message', check=checkyes, timeout=60)

                        if( str(confirmation_final.content).lower() == 'yes'):
                                already_send = True
                                full_message = "List of all users that need to submit their whitelist: " + '\n'

                                for user_in_channel in message:
                                    print(user_in_channel)
                                    if message == []:
                                        break
                                    full_message= full_message + (user_in_channel + "\n")

                                await channel.send(full_message)

        except TimeoutError:
            await ctx.send("you took to much time confirming , please type 'yes' to confirm next time, please restart the command using V!say")

        if ( (not already_send) and (message)):

                full_message= "List of all users that need to submit their WL application! : \n "
                for user_in_channel in message:
                    print(user_in_channel)
                    full_message =  full_message + (user_in_channel + "\n")
                await channel.send(full_message)


    except TimeoutError:
            await ctx.send("you took to much time confirming , please type 'yes' to confirm next time, please restart the command using V!say")





    except asyncio.TimeoutError:
        await ctx.reply("You took too much time ! , command canceled")




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


@say.error
async def say_error(ctx: commands.Context, error: commands.CommandError):

    if isinstance(error, commands.CommandInvokeError):
        message = f"Cannot acces the channel please grant me permission to write in the channel"
        await ctx.send(message)
    else:
        message = "Oh no! Something went wrong while running the command!"


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="timevillains.xyz"))
    print('Loading Evil : 10000%')

async def on_message(self, message):
    if message.author == self.user: #Avoid replying to his own message
        return



bot.run(TOKEN HERE)