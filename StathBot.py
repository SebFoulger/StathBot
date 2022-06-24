import discord
import random
import requests
import json
import os
import time

#Symbol to put before commands:
global com
com = "!!"

TOKEN = 'ODU3OTQ3ODA5NTc5NDAxMjI2.YNXAKQ.I5-dWLmln3VxDioPUK6qizbB7bY'

#Which channel can it function in:
global channelName
channelName = 'stath-bot'

client = discord.Client()


class Random_data:                          #Class to used to store things when we want to generate a random piece of data, e.g. images/gifs/questions/quotes etc.
    def __init__(self,input_list,size):
        self.data_list=input_list           #The data
        self.data_size=len(input_list)      #The size of the data
        self.recent_list=[]                 #The data that's recently been used (to ensure we aren't sending the same data over and over again)
        self.recent_max_size=size           #The maximum size that the recently used data can be. Note making this bigger will slow down the code

class Question_class:                       #Class to keep track of data related to questions/answers/games
    def __init__(self):
        self.current_answer=""              #Current answer to the asked question
        self.question_asked=False           #Has a question been asked (and not answered yet?)
        self.start_time=0                   #Used to output how long the user took to answer
        self.number_questions=0             #Keeps track of how many questions are left in a game
        self.total_questions=0              #Keeps track of how many questions in total in a game
        self.players = []                   #A 2D array keeping track of players and their score in the current game
        self.start_player=""                #Keeps track of which player started the game (so we know who can end it)

class Flute:                                #Class to keep track of fluuute :)
    def __init__(self,max_val):             
        self.number=1                       #Number is the current number of u's in the fluuute
        self.max_val=max_val+1              #This holds the max length of the fluuuute so that it knows when to reset
        self.counter=0                      #This keeps track of how many times we have reached max flutage

#Initialising the random quotes object:

file = open("quotes.txt","r")
quotes_list=file.readlines()
file.close()

global quotes
quotes = Random_data(quotes_list,3)

#Initialising the random gifs object:

file = open("gifs.txt","r")
gifs_list=file.readlines()
file.close()

global gifs
gifs = Random_data(gifs_list,3)                 #gifs.data_list is an array containing the tenor links for gifs

#Intialising the random images object:

APP_FOLDER = "D:/Python/Discord Bots/StathBot/images/"

totalFiles = 0

for base,dirs,files in os.walk(APP_FOLDER):     #Finding out the number of images we have
    for Files in files:
        totalFiles+=1

temp_list = []
for i in range(1,totalFiles+1):                 #images.data_list is an array like ['1.jpg',...,'66.jpg']
    temp_list.append(f'{i}.jpg')
images = Random_data(temp_list,3)

#Initializing the random questions object

file = open("questions.txt","r")
questions_list = file.readlines()
file.close()

global question_size    #This keeps track of recent questions so that we have to wait at least question_size questions before we see a repeat question
question_size=2

global questions
questions = Random_data(questions_list,question_size)

#Initializing the answers object

file = open("answers.txt","r")
answers_list = file.readlines()
file.close()
for i in range(0,len(answers_list)):
    answers_list[i]=answers_list[i].strip("\n")
    

global answers
answers = Random_data(answers_list,2)

#Initialising the flute object

global flu
flu = Flute(60)     #Max fluteage of 60!

#Initialising the admins list

file = open("admins.txt","r")
global admins_list
admins_list = file.readlines()
file.close()
for i in range(0,len(admins_list)):
    admins_list[i]=admins_list[i].strip("\n")


#Initialising the help message:

file = open("help.txt","r")
global help_msg
help_msg = file.read()
file.close()

global q
q = Question_class()

def get_random(obj):
    n = obj.data_size
    if (len(obj.data_list)==len(obj.recent_list)):
        obj.recent_list=[]
    temp = obj.data_list[random.randint(0,n-1)]
    while temp in obj.recent_list:
        temp = obj.data_list[random.randint(0,n-1)]

    if len(obj.recent_list)<obj.recent_max_size:
        obj.recent_list.append(temp)
    else:
        obj.recent_list.pop(0)
        obj.recent_list.append(temp)
    return temp

def ask_question():
    q.question_asked=True
    question = get_random(questions)
    q.current_answer = answers.data_list[questions.data_list.index(question)]
    q.start_time = time.time()
    return question

def end_game():
    q.question_asked=False
    string = ""

    questions.recent_list=[]
    questions.recent_max_size=question_size
    
    q.number_questions=0
    
    string+='Game over\n'
    end_game = sorted(list(q.players), key=lambda x: x[1])
    
    temp = []
    length=len(end_game)-1
    for i in range(0,length+1):
        temp.append(end_game[length-i])

    if len(temp)==0:
            string+="No players"
    else:
        if temp[0][1]==1:
            string+=f'Winner: {temp[0][0].split("#")[0]} with 1 point'
        else:
            string+=f'Winner: {temp[0][0].split("#")[0]} with {temp[0][1]} points\n'
        if len(temp)>1:
            if temp[1][1]==1:
                string+=f'Second place: {temp[1][0].split("#")[0]} with 1 point'
            else:
                string+=f'Second place: {temp[1][0].split("#")[0]} with {temp[1][1]} points\n'
        if len(temp)>2:
            if temp[2][1] == 1:
                string+=f'Third place: {temp[2][0].split("#")[0]} with 1 point'
            else:
                string+=f'Third place: {temp[2][0].split("#")[0]} with {temp[2][1]} points'

    q.players = []
    q.start_player=""
    return string

def bin_search(a,b,n):

    i = 0
    j = n

    while i<j:
        m=(i+j)//2
        if a[m].split(",")[0] < b:
            i=m+1
        else:
            j=m
                    
    return i
    


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    username = str(message.author).split("#")[0]
    userMessage = str(message.content)
    channel = str(message.channel.name)

    if message.author == client.user:
        return

    if message.channel.name == channelName:

        #Random quote generator
        
        if userMessage.lower() == f'{com}quote':
            quote = get_random(quotes)
            await message.channel.send(quote)
            return

        #Random gif generator

        elif userMessage.lower() == f'{com}gif':
            gif = get_random(gifs)
            await message.channel.send(gif)
            return


        #Random image generator

        elif userMessage.lower() == f'{com}image':
            img = get_random(images)
            await message.channel.send(file=discord.File("images/"+img))
            return

        #Random episode generator. Randomly outputs an episode of the form 'Season X Episode X'

        elif userMessage.lower() == f'{com}randomep':
            await message.channel.send(f'Season {random.randint(1,2)} Episode {random.randint(1,6)}')
            return

        #Flute command (leons request). Sends a fluuute with one more u each time, resetting eventually and keeping track of how many resets.

        elif userMessage.lower() == f'{com}flute':
            temp = ""
            for i in range(0,flu.number):               #To output the correct number of u's
                temp+="u"
                
            await message.channel.send(f'fl{temp}te')   #Sends the flute message
            flu.number+=1
            if flu.number==flu.max_val:                 #Resetting the flute:
                flu.counter+=1
                await message.channel.send('Congratulations, you have reached maximum flute-age!')
                await message.channel.send(f'There has now been {flu.counter} max flutes.')
                await message.channel.send('Resetting...')
                flu.number=1
            return

        #Command to get the number of questions a user has asked
        
        elif userMessage.lower() == f'{com}score':
            file = open('userquestions.txt','r')
            lines = file.readlines()
            file.close()

            i = bin_search(lines,str(message.author),len(lines))    #Find the location of the author in the file, or where it should be if the author isn't already there
            temp = lines[i].strip("\n").split(",")
            if  temp[0]==str(message.author):                       #If the user has been found:
                await message.channel.send(f'{username} has answered {temp[1]} questions correctly!')
            else:                                                   #If the user hasn't been found:
                await message.channel.send(f'{username} has not answered any questions yet.')
            return

        #Leaderboard command. Outputs the top 3 users with the most number of questions answered correctly.

        elif userMessage.lower() == f'{com}leaderboard':            
            file = open('userquestions.txt','r')
            lines = file.readlines()
            file.close()
            for i in range(0,len(lines)):
                lines[i]=lines[i].strip('\n').split(',')    #Splitting the scores from the usernames
                lines[i][0]=lines[i][0].split('#')[0]       #Removing the #XXXX from the usernames
                lines[i][1] = int(lines[i][1])              #Turning the scores into integers

            end_lines = sorted(list(lines), key=lambda x: x[1])
            length = len(end_lines)

            string = 'Leaderboard for number of questions answered correctly:\n1st place:   '+end_lines[length-1][0].split('#')[0]+' with ' + str(end_lines[length-1][1])+' points\n'
            string+='2nd place: '+end_lines[length-2][0]+' with ' + str(end_lines[length-2][1])+' points\n'
            string+='3rd place: '+end_lines[length-3][0]+' with ' + str(end_lines[length-3][1])+' points'

            await message.channel.send(string)
            return

        #Help command

        elif userMessage.lower() == f'{com}help':
            await message.author.send(help_msg)
            return

        #Question command

        elif userMessage.lower() == f'{com}question':
            if q.number_questions==0:           #If we are not already in a game:
                if q.question_asked:            #If a question has already been asked:
                    await message.channel.send("Overriding previous question")
                await message.channel.send(ask_question())
            else:                               #If we are in a game:
                await message.channel.send("Please wait for the game to finish")
            return

        #Game command

        elif userMessage.lower().startswith(f'{com}game '):
            try:                                                #If the input is of the form !!game X where X is an integer:
                qnum = int(userMessage[6:])+1
                q.start_player=message.author
                q.total_questions=qnum
                questions.recent_max_size=qnum
                if qnum>=1:
                    await message.channel.send(f'Question 1')
                    q.number_questions=qnum
                    await message.channel.send(ask_question())
                else:
                    message.channel.send("Please choose more than 0 questions")
            except:                                             #If the input is invalid:
                await message.channel.send("Error")
            return

        #End game command

        elif userMessage.lower()==f'{com}endgame' and (message.author==q.start_player or str(message.author) in admins_list):
            await message.channel.send(f'{username} has ended the game')
            await message.channel.send(end_game())
            return

        #Answer command (this needs needs to be the second last command in this if):

        elif q.question_asked and userMessage.lower() == q.current_answer.lower():
            end_time = time.time()

            #Writing the number of questions that the user has answered to a text document
            
            file = open('userquestions.txt','r')
            lines = file.readlines()
            file.close()

            n=len(lines)

            i = bin_search(lines,str(message.author),n)

            if i!=n:
                at_end=False
                if lines[i].split(",")[0]==str(message.author):
                    temp = lines[i].strip("\n").split(",")
                    lines[i]=temp[0]+","+str(int(temp[1])+1)+"\n"
                else:
                    lines.insert(i,str(message.author)+",1\n")
            else:
                at_end=True         

            if not at_end:

                file = open('userquestions.txt','w')
                for line in lines:
                    file.write(line)
                file.close()
            else:
                file = open('userquestions.txt','a')
                file.write(f'{str(message.author)},1\n')
                file.close()

            #End of writing the number of questions
            
            q.question_asked = False
            await message.channel.send(f'{username} wins in {round(end_time-q.start_time,2)} seconds! \nThe answer was {q.current_answer}')
            

            if q.number_questions>=2:
                found = False
                for i in range(0,len(q.players)):
                    if q.players[i][0]==str(message.author):
                        found=True
                        q.players[i][1]+=1
                        break;

                if  not found:
                    q.players.append([str(message.author),1])


                if q.number_questions==2:
                    await message.channel.send(end_game())
                else:
                    q.number_questions-=1
                    await message.channel.send(f'Question {q.total_questions-q.number_questions+1}')
                    await message.channel.send(ask_question())
            return


        #If they use an invalid command (this needs to be the last command in this if):

        elif userMessage.lower().startswith(com):
            await message.channel.send(f'Use {com}help for help')
            return

client.run(TOKEN)
