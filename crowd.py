
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'RUNNER' # change to what you need
#BOT_OWNER_ROLE_ID = "787948023165747230" 
  
 

 
oot_channel_id_list = [
"790504442818068490",
"789766952285241344",
"790448995892985877",
"787374423664885791",
"787292252451504128",
"782496161642184705",
"777779980260081676",
"787142092718735401",
"781900462667595849",
"770467560553578536",
"779323929420234772",
"763663837525573642",
"786908858047922186",
"760555743556141077",
"568617830258442255",
"745465606219890700",
"787374556967862273",
"787374556967862273",
"776456074382802995",
"782496162350891019",
"785386670810988574",
"760557826359296020",
"777779518286462987",
"782280378681393213",
"783307048459829299",
"786291209080537099",
"786940661835235368",
"774945138488508427",
"774945140204634140",
"783351014924615721",
"786396180007092266",
"745465606219890700",
"779323930464092171",
"783020931634167808",
"783307049995993099",
"782679376478208096",
"786291212285247558",
"570794448808837131",
"700241674529669120",
"774945138488508427",
"776456074382802995",
"789837704871149598",
"790545565628891146",
]

answer_pattern = re.compile(r'(not|n|e)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 1000
nomarkscore = 500
markscore = 100

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
        print("Nelson Trivia Self Bot")
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
        self.embed=discord.Embed(title="**__CROWD RESULTS!__**",description="",colour=discord.Colour.green())
        self.embed.add_field(name="**__Option ❶__**", value="[0.0](https://discord.gg/VCAGARv)", inline=False)
        self.embed.add_field(name="**__Option ❷__**", value="[0.0](https://discord.gg/VCAGARv)", inline=False)
        self.embed.add_field(name="**__Option ❸__**", value="[0.0](https://discord.gg/VCAGARv)", inline=False)
        #self.embed.add_field(name="**__Best Ans__**", value="🔎", inline=False)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/787740573720248350/788072389405048862/cool.jpg") 
        
   
        

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = " <a:emoji_89:786191472290037772> "
                best_ans = "<:1_:775563482833748059>"
       

            if answer == 2:
                two_check = " <a:emoji_89:786191472290037772> "
                best_ans = "<:2_:775563557559468073>"
       

            if answer == 3:
                three_check = " <a:emoji_89:786191472290037772> "
                best_ans = "<:3_:775563599435399178>"

            

        if lowest < 0:
            if answer == 1:
                one_cross = ":x:"
            if answer == 2:
                two_cross = ":x:"
            if answer == 3:
                three_cross = ":x:"            
 
        self.embed.set_field_at(0, name="**__Option ❶__**",  value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**__Option ❷__**",  value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**__Option ❸__**",  value="**{0}**{1}".format(lst_scores[2], three_check))
        #self.embed.set_field_at(3, name="**__Best Ans__**", value=f"{best_ans}") 

        
        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='With I Am Best Bot Ever Made By ┻━┻◥ʙ ᴏ ꜱ ꜱ ➈™࿐ ...'))
        await self.change_presence(activity=discord.Activity(type=1,name=' I Am Captain Cool'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "-":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("<a:emoji_19:790558948230823976>")
                #await self.embed_msg.add_reaction("<a:POISIONTRIVIA:775330905253347368>")
                #await self.embed_msg.add_reaction("")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("** You Do Not Have permission To Use This** **cmd!** If You Want To Run Bot Then apply in #「✒┃apply-for-runner」")
            return




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
    loop.create_task(bot.start('Nzg4MDYxMDQ1ODA0NzYxMTE4.X9eBCg.ePcU1plkajIyy8_RbY0SHmgVT40'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NzAzODQ3Nzc5MjE0MDMyODk3.X-CJDA.h5GK4fZeROPFKaFZmjObLCTK-X8',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
