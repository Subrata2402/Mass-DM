  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import random
import datetime
import multiprocessing
import threading
import concurrent

#BOT_OWNER_ROLE = 'Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "503197827556704268" 
  
g="https://discord.gg/2degbQMAxU" 

 
oot_channel_id_list = ["764790868745650226", "774480528631136287",  "774605289076686849", "728413225078751251", "773602512812769331", "763607773849583639", "768676688304930866", "771545387701764106", "764790868745650226", "770486337912045578"]

answer_pattern = re.compile(r'(n|not)?([1-3]{1})(\?)?(cnf|c|cf|conf|apg)?(\w|\ww)?$', re.IGNORECASE)

apgscore = 1000
nomarkscore = 320
markscore = 320

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        #value=random.randint(0,0xffffff)
        self.embed=discord.Embed(title="<:eraser:776122385908629544> **| HQ ERASER**",url="https://discord.gg/2degbQMAxU", description="", colour=0x00ff00)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
        self.embed.set_footer(text="DANGER TRIVIA")
        self.embed.add_field(name="**__Erased Answer__**", value="0", inline=False) 


        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        not_answer = "**Option ➜ <a:redload:772439692411011073> = <:emoji_43:776062431100928001>**"
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = " <:emoji_13:772843132093202443>  "

            if answer == 2:
                two_check = " <:emoji_13:772843132093202443>  "
                
            if answer == 3:
                three_check = " <:emoji_13:772843132093202443> "
                

        if lowest < 0:
            if wrong == 1:
                one_cross = ""
                not_answer = "**Option ➜ <:emoji_44:776063628561874955> = <:emoji_43:776062431100928001>**" 
                gif_ans="https://cdn.discordapp.com/emojis/777831205407424513.png"    
          
            if wrong == 2:
                two_cross = ""
                not_answer = "**Option ➜ <:emoji_45:776063661722173452> = <:emoji_43:776062431100928001>**" 
                gif_ans="https://cdn.discordapp.com/emojis/777831258314637342.png"

            if wrong == 3:
                three_cross = ""
                not_answer = "**Option ➜ <:emoji_46:776063695104639006> = <:emoji_43:776062431100928001>**"
                gif_ans="https://cdn.discordapp.com/emojis/777831284990672907.png"

    
        self.embed.set_field_at(0, name="**__Erased Answer__**", value=not_answer, inline=True)
        self.embed.set_thumbnail(url="{}".format(gif_ans)) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        log=self.get_channel(775948612014178315)
        await log.send("> ** HQ Eraser Database Is Updated ** ✅")
        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="with HQ Eraser !"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "hr":
            await message.delete()

            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            await self.embed_msg.add_reaction("<:eraser:776122385908629544>")
            self.embed_channel_id = message.channel.id    
            

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('Nzc1OTM0NjIyMjgyMjg1MDg3.X6tjbg.-AkIf1_vvcs2-LgrnSEeS3GRS1k'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjYwMzM3MzQyMDMyMjQ4ODMy.X6uAMA.Z5E4mok4Fn7iAzMRRN_1dLZSGqY',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=5)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
