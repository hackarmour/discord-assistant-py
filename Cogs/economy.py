import asyncio
import discord
import json
from discord.ext import commands, tasks
import sqlite3
import random
import datetime
from discord.ext.commands.core import cooldown
from discord.ext.commands.errors import CommandOnCooldown
from discord_components import DiscordComponents,Button,ButtonStyle,InteractionType
places=['car','backyard','bed','toilet','discord','mailbox','hospital','pantry','bus']
conn = sqlite3.connect('Configuration/Balance.db')
c = conn.cursor()
phrases=['I am done with my work','Think outside the box','Time for git push','damn another bug','it is deployed','I like vscode']
class Economy(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

 ####################################################################################################
 ############## ==> on_message event handler to add users in database when they send message only if they don't exist in the database
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        c.execute(f"""SELECT * FROM userdata WHERE userid='{message.author.id}'""")  
        user= c.fetchone()
        try:
            user=list(user)
        except TypeError as e:
            c.execute(f"""INSERT INTO userdata VALUES(
                '{message.author.id}',
                '0',
                '0',
                '{message.guild.id}'
            )""")
            conn.commit()


####################################################################################################
########### ==> balance command to check the balance of author or mentioned user

    @commands.command(aliases=['bal'])
    async def balance(self,ctx, user: commands.MemberConverter = None):
        if user == None:
            User = ctx.author
        elif user.bot:
            return
        else:
            User = user

        c.execute(f"""SELECT * FROM userdata WHERE userid='{User.id}'""")
        data = c.fetchone()
        try:
            data = list(data)
        except TypeError as e:
            await ctx.reply(f"The account of **{User.name}** does not exist!")
            return
        embed = discord.Embed(title=f"{User.name}'s balance", color=0x1ee0eb,
                            description=f" **Wallet**  {data[1]} :coin: \n**Bank**  {data[2]} :coin: ")
        await ctx.reply(embed=embed)


##################################################################################################
########## ==> Earn command to let users earn some money every 30mins

    @commands.command(aliases=['earn', 'work'])
    @commands.cooldown(1,1800,commands.BucketType.user)
    async def _e(self,ctx):
        money = random.randrange(200, 10000)
        randomPhrase=random.choice(phrases)
        await ctx.send(f"Type the following Phrase:\n`{randomPhrase}`")
        try:
            res=await self.bot.wait_for('message',check=lambda x:x.author==ctx.author,timeout=30.0)
            if (res.content.lower()==randomPhrase.lower()):
                c.execute(
                    f"""UPDATE userdata SET walletAmt=walletAmt+'{money}' WHERE userid='{ctx.author.id}'""")
                conn.commit()
                await ctx.reply(f"You worked hard and earned {money}:coin:")
            else:
                await ctx.reply("You are too careless at work. Please comeback later")
                return
        except:
            await ctx.send("The user does not replied in given time. Please come back after 30mins to use this command again")
                


 ########################################################################################
 ############# ==> Deposit command to add money in user's bank account after deducting from their wallet
    @commands.command(aliases=['dep', 'deposit', 'deposite'])
    async def _deposit(self,ctx, amount):
        if amount == 'all':
            c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
            try:
                walletBal = list(c.fetchone())[1]
            except TypeError:
                await ctx.reply("Your account does not exist")
                return
            if walletBal == 0:
                await ctx.reply("You do not have enough money in your wallet")
                return
            c.execute(
                f"""UPDATE userdata SET bankAmt=bankAmt+'{walletBal}' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            c.execute(
                f"""UPDATE userdata SET walletAmt='0' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            await ctx.reply(f"Deposited {walletBal}:coin: in your BankAccount")
            return
        try:
            Amount = int(amount)
        except:
            await ctx.send("Please specify a valid number and try again")
            return
        c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
        walletBal = list(c.fetchone())[1]
        if walletBal == 0 or Amount>walletBal:
            await ctx.reply("You do not have enough money in your wallet")
            return
        c.execute(
            f"""UPDATE userdata SET bankAmt=bankAmt+'{Amount}' WHERE userid='{ctx.author.id}'""")
        conn.commit()
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt-'{Amount}' WHERE userid='{ctx.author.id}'""")
        conn.commit()

        await ctx.reply(f"Deposited {Amount}:coin: in your BankAccount")



###################################################################################################
############# ==> Rob Command to let user's another users

    @commands.command()
    async def rob(self,ctx, user: commands.MemberConverter):
        if user == None:
            await ctx.reply("Please specify a user.")
            return
        elif user.bot:
            await ctx.reply("Hey you noob.Why do you want to rob a bot")
            return
        elif user == ctx.author:
            await ctx.reply("Wow, What a dumbass, Why do you wanna rob yourself.")
            return
        else:
            User = user
            c.execute(f"""SELECT * FROM userdata WHERE userid='{User.id}'""")
            Userbal = c.fetchone()
            c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
            authorbal = list(c.fetchone())[1]
            try:
                Userbal = list(Userbal)[1]
            except TypeError:
                await ctx.reply("The account of user does not exist")
                return
            powerful = random.choice([True, False])
            if Userbal < 600:
                await ctx.reply("That user does not have enough money. Not worth it Man")
                return
            if (powerful == True):
                amount = random.randint(100, authorbal)
                await ctx.reply(f"{User.name} caught you.\n You gave {amount}:coin:")
                c.execute(
                    f"""UPDATE userdata SET walletAmt=walletAmt-'{amount}' WHERE userid='{ctx.author.id}'""")
                conn.commit()
                c.execute(
                    f"""UPDATE userdata SET walletAmt=walletAmt+'{amount}' WHERE userid='{User.id}'""")
                conn.commit()

            elif powerful == False:
                amount = random.randint(100, authorbal)
                await ctx.reply(f"You robbed {User.name} and got {amount}:coin:")
                c.execute(
                    f"""UPDATE userdata SET walletAmt=walletAmt-'{amount}' WHERE userid='{User.id}'""")
                conn.commit()
                c.execute(
                    f"""UPDATE userdata SET walletAmt=walletAmt+'{amount}' WHERE userid='{ctx.author.id}'""")
                conn.commit()

 #####################################################################################################
 ##### ==> Withdraw command so that users can withdraw money from their bank account and add them in their wallet
    @commands.command(aliases=['wd'])
    async def withdraw(self,ctx, value):
        if value == 'all':
            c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
            data = c.fetchone()
            try:
                data = list(data)
            except TypeError:
                await ctx.reply("Your Account does not exist")

            walletAmt = data[1]
            bankAmt = data[2]

            if bankAmt <= 0:
                await ctx.reply("You do not have enough money in your wallet to withdraw")
                return
            c.execute(
                f"""UPDATE userdata SET walletAmt=walletAmt+bankAmt WHERE userid='{ctx.author.id}'""")
            conn.commit()
            c.execute(
                f"""UPDATE userdata SET bankAmt='0' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            await ctx.reply(f"Successfully added {bankAmt}:coin: in your wallet")
            return
        try:
            Amount = int(value)
        except:
            await ctx.reply("Please enter a valid value")
        c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
        bankBal = list(c.fetchone())[2]
        if bankBal == 0 or Amount>bankBal:
            await ctx.reply("You do not have enough money in your bank")
            return
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt+'{Amount}' WHERE userid='{ctx.author.id}'""")
        conn.commit()
        c.execute(
            f"""UPDATE userdata SET bankAmt=bankAmt-'{Amount}' WHERE userid='{ctx.author.id}'""")
        conn.commit()
        await ctx.reply(f"Added {Amount}:coin: in your wallet")


######################################################################################33
 ##### ==> Daily command to give users a daily bonus
    @commands.command()
    @commands.cooldown(1, 864000, commands.BucketType.user)
    async def daily(self,ctx):
        c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
        data = c.fetchone()
        try:
            data = list(data)
        except TypeError:
            await ctx.reply("Your account does not exist, Please open your account first!")
            return
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt+'25000' WHERE userid='{ctx.author.id}'""")
        conn.commit()
        won = random.choice([True, False])
        if won == False:
            embed = discord.Embed(title=f"Here is your daily bonus {ctx.author.name}", color=ctx.author.color,
                                description="Successfully added **25000** :coin: in your Wallet as daily bonus. Please come back after 24hours to claim it again")
            embed.set_footer(text=f'🥳')
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=f"Here is your daily bonus {ctx.author.name}", color=ctx.author.color,
                                description="Successfully added **25000** :coin: in your Wallet as daily bonus. You are lucky today and got a Lucky Box.Please come back after 24hours to claim it again")
            embed.set_footer(text=f'🥳')
            await ctx.reply(embed=embed)
            c.execute(
                f"""UPDATE Inventory SET quantity=quantity+'1' WHERE userid='{ctx.author.id}' AND itemName='Lucky Box'""")
            conn.commit()


##########################################################################################################
######## ==> Another rob command to rob the bank account of mentioned user
    @commands.command(aliases=['brob'])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def bankrob(self,ctx, user: commands.MemberConverter):
        if user == None:
            await ctx.reply("Who are we robbing? Please mention a user and then try again")
            return
        elif user.bot:
            return
        elif user == ctx.author:
            await ctx.reply("Why do you want to rob yourself kiddo?")
            return
        c.execute(f"""SELECT * FROM userdata WHERE userid='{user.id}'""")
        data = c.fetchone()
        try:
            data = list(data)
        except TypeError:
            await ctx.reply(f"The account of {user.name} does not exist")
            return
        userBank = data[2]
        if userBank < 2000:
            await ctx.reply("The user does not have enough moeny in bank account.")
            return
        amtRobbed = random.randint(100, 5000)
        caught = random.choice([True, False])
        if caught == True:
            await ctx.reply(f"You tried to rob the {user.name}'s bank account and get caught by the police and paid **{amtRobbed}** :coin:")
            c.execute(
                f"""UPDATE userdata SET walletAmt=walletAmt-'{amtRobbed}' WHERE userid='{ctx.author.id}'""")
            conn.commit()
        else:
            await ctx.reply(f"You robbed the {user.name}'s bank account and got **{amtRobbed}** :coin:")
            c.execute(
                f"""UPDATE userdata SET walletAmt=walletAmt+'{amtRobbed}' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            c.execute(
                f"""UPDATE userdata SET bankAmt=bankAmt-'{amtRobbed}' WHERE userid='{user.id}'""")
            conn.commit()

 #################################################################################################
 #########==> Shop command to view what's in shop
    @commands.command()
    async def shop(self,ctx):
        c.execute(f"""SELECT * from shop""")
        data = c.fetchall()
        if len(data)==0:
            await ctx.send("The shop is empty")
            return
        items = len(data)
        da = list(data[0])
        emb = discord.Embed(title='Shop', color=ctx.author.color)
        for i in range(items):
            emb.add_field(
                name=f"{data[i][0]}", value=f"Price: ** {data[i][1]} **  :coin: \nDescription:` {data[i][2]} `\n Id: ` {data[i][3]} `\n Category: ` {data[i][4]} `\nSelling Price: `{data[i][5]} ` :coin: ", inline=False)
        await ctx.reply(embed=emb)

 ##############################################################################3
 ########### ==> Inventory command to view the user's or mentioned user's inventory
    @commands.command(aliases=['inv', 'inventory'])
    async def _inv(self,ctx, user: commands.MemberConverter = None):
        if user == None:
            User = ctx.author
        elif user.bot:
            return
        else:
            User = user
        c.execute(f"""SELECT * FROM Inventory WHERE userid='{User.id}'""")
        availableItems=[]
        data = c.fetchall()
        for item in data:
            if list(item)[1]>0:
                availableItems.append(item)
        if len(availableItems)==0:
            await ctx.send(f"""The inventory of {User.name} is empty""")
            return
        embed = discord.Embed(title=f"{User.name}'s Inventory", color=User.color)
        for i in availableItems:
            items = list(i)
            if items[1] > 0:
                embed.add_field(
                    name=f"{items[0]}", value=f" Quantity:{items[1]}", inline=False)
        await ctx.reply(embed=embed)

 ######################################################################################################### ==> use command to user items present  in your inventory

    @commands.command()
    async def use(self,ctx,*,itemname):
        c.execute(f"""SELECT * FROM Inventory WHERE itemName='{itemname}' OR itemId='{itemname}' AND userId='{ctx.author.id}'""")
        data=c.fetchone()
        try:
            data=list(data)
        except TypeError:
            await ctx.reply("Sorry, that item does not exist in your inventory!")
            return
        if (itemname.lower()) in ['luckybox','lucky box']:
            prize=random.randint(1000,7000)
            await ctx.send(f"You used {itemname} and got `{prize}`:coin:")
            c.execute(f"""UPDATE userdata SET walletAmt=walletAmt+'{prize}' WHERE userId='{ctx.author.id}'""")
            conn.commit()
            c.execute(f"""UPDATE Inventory SET quantity=quantity-'1' WHERE itemName='{itemname}' OR itemId='{itemname}' AND userid='{ctx.author.id}'""")
            conn.commit()
            return
        c.execute(f"""SELECT * FROM shop WHERE itemName='{itemname}' OR itemId='{itemname}'""")
        item=list(c.fetchone())
        prize=random.randint(item[1],50000)
        await ctx.send(f"You used {itemname} and got `{prize}`:coin:")
        c.execute(f"""UPDATE userdata SET walletAmt=walletAmt+'{prize}' WHERE userId='{ctx.author.id}'""")
        conn.commit()
        c.execute(f"""SELECT * FROM Inventory WHERE itemName='{itemname}' OR itemId='{itemname}' AND userId='{ctx.author.id}'""")
        item=list(c.fetchone())
        if (item[1]==1):
            c.execute(f"""DELETE FROM Inventory WHERE itemName='{itemname}' OR  itemId='{itemname}' AND userId='{ctx.author.id}'""")
            conn.commit()
            return
        try:
            c.execute(f"""UPDATE Inventory SET quantity=quantity-'1' WHERE itemName='{itemname}' OR itemId='{itemname}' AND userid='{ctx.author.id}'""")
            conn.commit()
        except Exception as e:
            pass


 #######################################################################
 ########## => This command let the bot's owner to add items in shop
    @commands.command()
    @commands.is_owner()
    async def push(self,ctx,itemName,cp,desc,id,cat,sP):
        """Here 'cp' is cost price of item, "desc" is description, "id" is id of item to let users write the item name without caps,spaces and emojis(custom). 'cat' is category it can either be collectible or usable, 'sp' is the selling price of that item"""
        c.execute(f"""INSERT INTO shop VALUES('{itemName}','{cp}','{desc}','{id}','{cat}',{sP})""")
        conn.commit()
        await ctx.send("Values Added")

    #######################################################################################
    ############ ==> Buy command to buy item from shop
    @commands.command()
    async def buy(self,ctx,itemname=None):
        if itemname!=None:
            res=itemname
        else:
            await ctx.reply("Enter Item Id:")
            res = await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=60.0)
            res = res.content
        c.execute(
            f"""SELECT * FROM shop WHERE itemName='{res}' OR itemId='{res}'""")
        data = c.fetchone()
        try:
            data = list(data)
        except TypeError:
            await ctx.reply("This item does not exist in the shop")
            return

        c.execute(
            f"""SELECT * FROM Inventory WHERE userid='{ctx.author.id}' AND itemName='{data[0]}'""")
        items = c.fetchone()
        c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
        user = c.fetchone()
        try:
            user = list(user)
        except TypeError:
            await ctx.reply("Your account does not exist")
            return
        if data[0] == "Lottery Ticket":
            if user[1] < data[1]:
                await ctx.reply("You do not have enough money in your wallet")
                return
            global draws
            draws.append(ctx.author.id)
            c.execute(
                f"""UPDATE userdata SET walletAmt=walletAmt-'{data[1]}' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            emb = discord.Embed(title='Confirmation of Purchase',
                                description=f"You Purchased {data[0]} and paid `{data[1]}`:coin:", color=ctx.author.color)
            await ctx.send(embed=emb)
            return
        if user[1] < data[1]:
            await ctx.reply("You do not have enough money in your wallet")
            return
        try:
            items = list(items)
        except TypeError:
            c.execute(
                f"""INSERT INTO Inventory VALUES('{data[0]}','1','{ctx.author.id}','{data[3]}')""")
            conn.commit()
            c.execute(
                f"""UPDATE userdata SET walletAmt=walletAmt-'{data[1]}' WHERE userid='{ctx.author.id}'""")
            conn.commit()
            emb = discord.Embed(title='Confirmation of Purchase',
                                description=f"You Purchased {data[0]} and paid `{data[1]}`:coin:", color=ctx.author.color)
            await ctx.reply(embed=emb)
            return
        c.execute(
            f"""UPDATE Inventory SET quantity=quantity+'1' WHERE userid='{ctx.author.id}' AND itemName='{data[0]}'""")
        conn.commit()
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt-'{data[1]}' WHERE userid='{ctx.author.id}'""")
        conn.commit()
        emb = discord.Embed(title='Confirmation of Purchase',
                            description=f"You Purchased {data[0]} and paid `{data[1]}`:coin:", color=ctx.author.color)
        await ctx.send(embed=emb)

 #########################################################################################
 ########### ==> Give command to mentioned user, a given number of coins
    @commands.command()
    async def give(self,ctx, user: commands.MemberConverter = None, amount: int = 0):
        if user == None:
            await ctx.reply("Please Mention a user")
            return
        elif user.bot:
            await ctx.reply("You cannot give money to a bot")
            return
        elif user == ctx.author:
            await ctx.reply("You can't give money to yourself")
            return
        c.execute(f"""SELECT * FROM userdata WHERE userid='{ctx.author.id}'""")
        data = c.fetchone()
        try:
            data = list(data)
        except TypeError:
            await ctx.reply("You account does not exist")
            return
        c.execute(f"""SELECT * FROM userdata WHERE userid='{user.id}'""")
        data1 = c.fetchone()
        try:
            data1 = list(data1)
        except TypeError:
            await ctx.reply(f"The account of user {user.name} does not exist")
            return
        if amount <= 0:
            await ctx.reply("Please enter a valid amount")
            return
        if amount > data[1]:
            await ctx.reply("You don't have enough money in your wallet")
            return
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt+'{amount}' WHERE userid='{user.id}'""")
        conn.commit()
        c.execute(
            f"""UPDATE userdata SET walletAmt=walletAmt-'{amount}' WHERE userid='{ctx.author.id}'""")
        await ctx.reply(f"Added ` {amount} ` :coin: into the wallet of {user.name}")

 #####################################################################################
 ########################################## ==> Sell command to sell the item, the user will get coins which is given in shop as selling price
    @commands.command()
    async def sell(self,ctx,itemName=None):
        if itemName==None:
            await ctx.send("Please specify an item to sell.")
            return
        c.execute(f"""SELECT * FROM Inventory WHERE userid='{ctx.author.id}' AND itemName='{itemName}' OR itemId='{itemName}'""")
        
        data=c.fetchone()
        try:
            data=list(data)
        except TypeError:
            await ctx.send("This item does not exist in your inventory!")
            return
        c.execute(f"""SELECT * FROM shop WHERE itemName='{itemName}' OR itemId='{itemName}'""")
        item=c.fetchone()
        item=list(item)
        if item[4].lower()=='collectible':
            await ctx.send("You can't use a collectible")
            return
        c.execute(f"""UPDATE userdata SET walletAmt=walletAmt+'{item[5]}' WHERE userId='{ctx.author.id}'""")
        conn.commit()
        c.execute(f"""SELECT * FROM shop WHERE itemName='{itemName}' OR itemId='{itemName}'""")
        quantity=c.fetchone()
        quantity=list(quantity)
        if quantity[1]>1:
            c.execute(f"""UPDATE Inventory SET quantity=quantity-'1' WHERE itemName='{itemName}' OR  itemId='{itemName}' AND userId='{ctx.author.id}'""")
            
            conn.commit()
            await ctx.reply(f"You sold `{itemName}` and got `{item[5]}`:coin:")
        else:
            c.execute(f"""DELETE FROM Inventory WHERE itemName='{itemName}' OR  itemId='{itemName}' AND userId='{ctx.author.id}'""")
            conn.commit()
            
            



############################################################################################################# ==> search command to search for money in random places
    @commands.command()
    async def search(self,ctx):
        localPlaces=places
        place1=random.choice(localPlaces)
        localPlaces.remove(place1)
        place2=random.choice(localPlaces)
        localPlaces.remove(place2)
        place3=random.choice(localPlaces)
        places.append(place1)
        places.append(place2)
        places.append(place3)
        components = [Button(label=f"{place1.capitalize()}",style=ButtonStyle.grey,id=place1.capitalize()),Button(label=f"{place2.capitalize()}",style=ButtonStyle.green,id=place2.capitalize()),Button(label=f"{place3.capitalize()}",style=ButtonStyle.red,id=place3.capitalize())]
        mssg=await ctx.reply("Where do you want to search",components=[components])
        try:
            while True:
                money = random.randint(500,1500)
                reaction = await self.bot.wait_for('button_click',timeout=30.0)
                if reaction.author!=ctx.author:
                    await reaction.respond(
                        type=4,
                        content="These buttons aren't for you",
                        ephemeral=True
                    )
                    continue
                result = [False,False,False,False,False,False,False,True,False,False,False,False,False,False,False]
                res=random.choice(result)
                if res==False:
                    emb= discord.Embed(title=f"{ctx.author.name} searched in {reaction.component.label.capitalize()}",color=ctx.author.color,description=f"You Found `{money}`:coin: in {reaction.component.label.capitalize()}")
                    c.execute(f"""UPDATE userdata SET walletAmt=walletAmt+'{money}' WHERE userid='{ctx.author.id}'""")
                    conn.commit()
                    for button in components:
                        button.disabled=True
                    await reaction.respond(
                        type=InteractionType.UpdateMessage,
                        embed=emb,
                        components=[components]
                    )
                    break
                    
                else:
                    emb= discord.Embed(title=f"{ctx.author.name} searched in {reaction.component.label.capitalize()}",color=ctx.author.color,description=f"You died while searching in {reaction.component.label.capitalize()} and lose all of your money in wallet :joy:")
                    c.execute(f"""UPDATE userdata SET walletAmt=walletAmt-walletAmt WHERE userid='{ctx.author.id}'""")
                    conn.commit()
                    for button in components:
                        button.disabled=True
                    await reaction.respond(
                        type=InteractionType.UpdateMessage,
                        embed=emb,
                        components=[components]
                    )
                    break
                
        except Exception as e:
            await mssg.edit(content="Guess you didn't want to search anywhere")


###########################################################################
########## Bot's owner command to add more places in that list. but these newly added places will be removed when bot is restarted 
    @commands.command()
    @commands.is_owner()
    async def addp(self,ctx,name):
        if name not in places:
            places.append(name)
            await ctx.send("Added new Place")
        else:
            pass
 ########## ==> This command add new phrases in list by following the same approach as above
    @commands.command()
    async def addph(self,ctx,*,Phrase):
        if Phrase not in phrases:
            phrases.append(Phrase)
            await ctx.send("Phrase added")
        else:
            pass

    async def checks(self,user):
        if user == None:
            return False
        elif user.bot:
            return False
        else:
            return True

def setup(bot):
    bot.add_cog(Economy(bot))