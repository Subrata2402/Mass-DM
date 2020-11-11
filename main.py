  
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

 
oot_channel_id_list = ["775945251340156930"]

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
        self.embed=discord.Embed(title="**__HQ Trivia Crowd Results !__**", colour=0x00ff00)
        self.embed.add_field(name="**__Option ❶__**", value=f"**[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❷__**", value=f"**[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❸__**", value=f"**[0]({g})**", inline=False)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775384878942257173/775933617943347230/unnamed.gif")
        self.embed.set_footer(text='Made by Subrata#3297',icon_url='https://cdn.discordapp.com/avatars/660337342032248832/828f7b13ce161e8a9d4c129e0ac776c4.webp?size=1024')
        self.embed.add_field(name="**__Correct Answer !__**", value="0", inline=False)
        self.embed.add_field(name="**__Erased Answer !__**", value="0", inline=False) 


        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        mark_check_one=""
        mark_check_two=""
        mark_check_three=""
        one_cross =""
        two_cross =""
        three_cross =""
        best_answer = "**Option ➜** <a:redload:772439692411011073>"
        not_answer = "**Option ➜** <a:redload:772439692411011073>"
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        gif_ans = 'https://cdn.discordapp.com/attachments/769445612231720960/774230429023993896/unnamed.gif'
        best_answer = '**Option ➜** <a:redload:772439692411011073>'
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = " <:emoji_13:772843132093202443>  "
                mark_check_one = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/769445612231720960/773618942874615828/772873539174268990.png"
                best_answer = "**Option ➜** <:emoji_39:773917426835521536>"
                   
            else:
                one_check = " "

            if answer == 2:
                two_check = " <:emoji_13:772843132093202443>  "
                mark_check_two = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/769445612231720960/773619358031151159/772873573999443978.png"
                best_answer = "**Option ➜** <:emoji_50:773917478723125269>"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = " <:emoji_13:772843132093202443> "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/769445612231720960/773619564206489600/772873605754388480.png"
                best_answer = "**Option ➜** <:emoji_44:773918363402371074>"
                   
            else:
                three_check = ""

            

        if lowest < 0:
            if wrong == 1:
                one_cross = " ❌"
                not_answer = "**Option ➜** <:emoji_39:773917426835521536>" 
               
            if wrong == 2:
                two_cross = " ❌"
                not_answer = "**Option ➜** <:emoji_50:773917478723125269>" 
               
            if wrong == 3:
                three_cross = " ❌"
                not_answer = "**Option ➜** <:emoji_44:773918363402371074>"
         
    
        self.embed.set_field_at(0, name="**__Option ❶__**", value=f"**[{lst_scores[0]}]({g}){one_check}{one_cross}**")
        self.embed.set_field_at(1, name="**__Option ❷__**", value=f"**[{lst_scores[1]}]({g}){two_check}{two_cross}**")
        self.embed.set_field_at(2, name="**__Option ❸__**", value=f"**[{lst_scores[2]}]({g}){three_check}{three_cross}**")
        self.embed.set_thumbnail(url="{}".format(gif_ans))
        self.embed.set_field_at(3, name="**__Correct Answer !__**", value=best_answer, inline=True)
        self.embed.set_field_at(4, name="**__Erased Answer !__**", value=not_answer, inline=True) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        log=self.get_channel(775948612014178315)
        await log.send("> ** Vedantu 2.0 Database Is Updated ** ✅")
        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="with Vedantu Trivia !"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+v":
            await message.delete()

            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            await self.embed_msg.add_reaction("🎉")
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




 
 
