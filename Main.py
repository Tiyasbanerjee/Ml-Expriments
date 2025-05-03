import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI



BASE_DIR = os.path.dirname(__file__)


def initialize_files_read(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def initialize_files_write(file_path, content):
    with open(file_path, 'a') as file:
        file.write("\n\n\n\n\n\n\n" + content)


def memory_overwrite(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def recent_context_overwrite(file_path, content, number):
    # Read and split into lines
    current_text = initialize_files_read(file_path)
    # remove useless newlines 
    current_text = current_text.rstrip('\n')    
    
    lines = current_text.split('\n')

    if len(lines) >= number:
        lines = lines[-number+1:] 
    
    # write the new content in next line

    lines.append(content)
    # Join and write back
    
    new_text = '\n'.join(lines)

    memory_overwrite(file_path, new_text)


def call_model(prompt: str, temperature: float):
    api_key ="abc"


    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=temperature,
        google_api_key=api_key
                                   )

    response = llm.invoke(prompt)
    return response.content


def prompt_maker(commands, data, memory, context,user_feetback,explained_quearies, name, notname):
    feedback_file = os.path.join(BASE_DIR, "mem_for_sum.txt")
    feedback = initialize_files_read(feedback_file)

    prompt = f"""
    Your name is {name} and you are debating against {notname}.
DEBATE ROLE: Expert debater engaging in evidence-based argumentation.

CONTEXT DATA:
→ Your cheracteristics and instrustions (importance:- your characyer is determined from it): {commands}
→ Opponent arguement (importance:- what your opponent is argueing): {data}
→ History or your memory that stores what happend before and which toppics and suntoppics are alrady covered (importance:-what stuffs happened in before convertations): {memory}
→ The Toppic of the debate (importance:- this is the main toppic or theam you and your opponent is arguement about, cautions:- if it seems your opponent is going out of the main and sub toppics and argueing about other things useless for understanding this toppic so ask them return questions that what is the realation between them with this toppic): {explained_quearies}
→ Recent arguements and toppics (importance:- holds the recod of the past arguements. helpful when: when you are trying to prove somthing and your opponent is trying to diffend , so you can ask them return questions that 'before you said that this is true now when my arguement is also becomes true for your past arguements so now how can you prove me wrong again?' . Good this type of queries ): {context}
→ Feedback(importance:- this is the most important part when moveing ahed , if this is blank that means the judge of the debaute is satisfyed but if he says for any improvements , you must follow them becouse it is human feeetback): {user_feetback}
→ computer feetback(importance:- this is computer feetback which is helpful for you to imporve your self and your arguements): {feedback}

OUTPUT REQUIREMENTS:
1. REPLY SECTION
   Under "**{name}'S_REPLY**":
   - Present your main arguments 
   - Support with evidence
   - deffend your position
   - Use clear examples (examples like which are trying to proof opponent wrong)
   - Always End with a question to your opponent (the question should not be sumthing addresing the opponent but rather a type of arguement which is trying to prove the opponent wrong , example- some question, if this happen true how wuold you can say that? if you are true so why this happen? , dont repeat the same question again and again, try to make it different each time)
   - Avoid unnecessary jargon

2. MEMORY SECTION
   Under "**MEMORY_**":
   - Document the realtime debate process as a human brain would do.
   - Record key debate points.
   - Make history of the toppics covered to avoid repetition.
   - Track argument evolution.
   

3. SUMMARY SECTION
   Under "**ARGUMENT_SUMMARY**":
   - Capture core arguments
   - where the opponent is wrong
   - breaf summery of the convertation
   - Add "{name}_SAID_IS:" prefix
   - Keep it concise

CRITICAL FORMAT RULES:
→ USE EXACTLY THE SAME FORMAT AS GIVEN!
→ NEVER MODIFY THE TEXT BETWEEN '**'!
→ KEEP STANDERD SPACEING!
→ FOLLOW ORDERS STRICTLY!
→ DONT SAY WHAT JUDGE SAID OR WHAT THE JUDGE THINKS , JUDGE IS NOT YOUR OPPONENT HE IS THE ONE WHO IS JUDGING YOU AND YOUR OPPONENT , SO DONT SAY ANYTHING ABOUT HIM OR HER , HE WILL SHARE HIS THOUGHTS BUT DONT MENTION HIM OR HER IN YOUR REPLY, THOUGH YOU CAN MENTION THE JUDGE'S FEEDBACK IN THE MEMORY SECTION!

RESPONSE TEMPLATE(MUST BE FOLLOWED!!!):

**{name}'S_REPLY**:
[Your response]

**MEMORY_**:
[Memory update]

**ARGUMENT_SUMMARY**:
  **{name}_SAID_IS:** [Brief recap]
""".strip()
    return prompt


def prompt_maker_summery(data1, data2,JUDGE_FEEDBACK):
    MEM_FILE= os.path.join(BASE_DIR, "mem_for_sum.txt")
    CON_FILE= os.path.join(BASE_DIR, "recent_context.txt")
    text_of_mem = initialize_files_read(MEM_FILE)
    text_for_con = initialize_files_read(CON_FILE)


    prompt = f"""
DEBATE PROGRESS ANALYSIS

CURRENT EXCHANGE:
MIKE's Position: {data1}
RIYA's Position: {data2}
some of privious context(importance:- help to understand them and judge them): {text_for_con}
your memory(importance:- in your memory it is stored what are the two opponents faults and strengths and it also stores some of important memoey): {text_of_mem}
human feetback(importance:- this is the most important part when moveing ahed , if this is blank that means the judge of the debaute is satisfyed but if he says for any improvements , you must follow them before giveing your judgement becouse it is human feeetback): {JUDGE_FEEDBACK}

FORMAT YOUR RESPONSE IN EXACTLY THREE SECTIONS:

**SUMMARY OF THE DEBATE**
Key Points:
• Main arguments from both sides
• Areas of agreement/disagreement
• Progress made so far
• Current debate status

Keep language simple and clear.
Highlight key developments in plain terms.
Focus on the most important points.

**RATINGS AND FEEDBACK**
Score both debaters on:

Quality of Argument (_/5):
• Evidence strength
• Logic clarity
• Examples used
• Expert citations

Practical Aspects (_/5):
• Real-world application
• Resource consideration
• Risk awareness
• Timeline realism

Overall Impact (_/5):
• Persuasiveness
• Clarity of vision
• Solution viability
• Long-term effects

**UPDATED MEMORY**
Human feetback:
• what improvements are needed in respect to the human feetback explain it in detail
• explain their faults in details and guide them how to improve

Track Development:
• Key arguments where they bouth disagreed
• Questions raised
• New topics explored
• Areas needing work or clarification
• Important claims made
• where the debate is heading if it is going out of the toppic or any senseless direction which should be avoided
• Continious feedback on the debate for improvement and classification of the toppic.

Remember: Keep feedback constructive and clear.
""".strip()
    return prompt

def devider(prompt):
    text = prompt
    try:
        # Updated patterns to be more flexible and match the exact format from prompt_maker
        patern1 = r"\*\*[A-Z]+'S_REPLY\*\*:?"  # More flexible reply pattern
        patern2 = r"\*\*MEMORY_\*\*:?"          # More flexible memory pattern
        patern3 = r"\*\*ARGUMENT_SUMMARY\*\*:?"  # More flexible summary pattern
        patern4 = r"[A-Z]+_SAID_IS:"            # SAID_IS pattern

        # Find all matches
        match1 = re.search(patern1, text)
        match2 = re.search(patern2, text)
        match3 = re.search(patern3, text)
        match4 = re.search(patern4, text)

        # Error handling for missing sections
        if not all([match1, match2, match3, match4]):
            print("\nDEBUG - Response format error. Text received:")
            print(text[:200] + "..." if len(text) > 200 else text)
            # Return default formatted response
            return (
                "**ERROR_REPLY**: Format error - sections missing",
                "**MEMORY_**: Response format error",
                "ERROR_SAID_IS: Invalid response format"
            )

        # Get indices
        m1 = match1.start()
        m2 = match2.start()
        m3 = match3.start()
        m4 = match4.start()

        # Extract sections
        f1 = text[m1:m2].strip()
        f2 = text[m2:m3].strip()
        f3 = text[m4:].strip()

        return f1, f2, f3

    except Exception as e:
        print(f"\nDEBUG - Error processing response: {str(e)}")
        # Return error response
        return (
            "**ERROR_REPLY**: Processing error",
            "**MEMORY_**: Failed to process response",
            "ERROR_SAID_IS: Processing failed"
        )

def inp():
    # 1) topic
    while True:
        topic = input("Enter your topic(if not write 'PASS'):: ").strip()
        if topic == "PASS":
            break
        if topic:
            break
        print("Please enter at least one character.")

    # 2) temperature
    while True:
        try:
            temperature = float(input("Enter the temperature (0.0 to 1.0): "))
            if 0.0 <= temperature <= 1.0:
                break
            print("Temperature must be between 0.0 and 1.0.")
        except ValueError:
            print("That's not a valid number.")

    # 3) recent context size
    while True:
        try:
            recent_con_size = int(input("Enter the recent context STORAGE SIZE (1-30): "))
            if 1 <= recent_con_size <= 30:
                # <-- this return exits the entire function immediately
                return topic, temperature, recent_con_size
            print("Size must be between 1 and 30.")
        except ValueError:
            print("Please enter an integer.")

def sum_mem_devider(text):
    patern1 = r"\*\*UPDATED MEMORY\*\*"
    
    match1 = re.search(patern1, text)
    m1 = match1.start()
    
    f2 = text[m1:]  # Updated memory section
    f1 = text[:m1]  # Everything before updated memory

    
        
    return f1, f2  # Return both values to match the unpacking



def sp_call(user_input):
    prompt = f"""
You are a debate moderator. Frame the following topic for structured debate:
INPUT: {user_input}.
-from this user input extract the meaning and main questions and quaries it makes.
-explain this in detailed.
-also explain the main and sub toppics and questions and quaries it makes.
""".strip()
    return call_model(prompt, temperature=0.7)


MEMORY_FILE_1    = os.path.join(BASE_DIR, "data_1.txt")
mf1= initialize_files_read(MEMORY_FILE_1)
MEMORY_FILE_2    = os.path.join(BASE_DIR, "data_2.txt")
mf2= initialize_files_read(MEMORY_FILE_2)
COMMANDS_FILE_1  = os.path.join(BASE_DIR, "commands_1.txt")
cf1= initialize_files_read(COMMANDS_FILE_1)
COMMANDS_FILE_2  = os.path.join(BASE_DIR, "commands_2.txt")
cf2= initialize_files_read(COMMANDS_FILE_2)
CONTEXT   = os.path.join(BASE_DIR, "recent_context.txt")
cnf= initialize_files_read(CONTEXT)
CONTEXT_HISTORY = os.path.join(BASE_DIR, "history_of_contexts.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "output.txt")
MEM_OF_SUM=os.path.join(BASE_DIR,"mem_for_sum.txt")

INP=os.path.join(BASE_DIR,"inp.txt")

DATA=os.path.join(BASE_DIR,"reply.txt")
USER_FEEDBACK= os.path.join(BASE_DIR,"feetback.txt")


    
    
def main():
        prompt, temperature, recent_con_size = inp()

        prompt_sp_c = sp_call(prompt)

        commands1 = cf1   
        commands2 = cf2

        data = initialize_files_read(DATA)
        user_feetback= initialize_files_read(USER_FEEDBACK)
    
        i=0

        while True:
            i += 1 

            if len(data) < 3:
                data = f"""
                   THE OPPONENTS QUESTION IS: {prompt}
                """

            call_model_1 = call_model(prompt_maker(commands1, data, mf2, cnf,user_feetback,prompt_sp_c,"MIKE","RIYA"), temperature)
            
            reply, memory, summary = devider(call_model_1)
            memory_overwrite(MEMORY_FILE_1, memory)
            recent_context_overwrite(CONTEXT, summary, recent_con_size)
            initialize_files_write(CONTEXT_HISTORY, summary)
            reply = f"{i}." + reply
            initialize_files_write(OUTPUT_FILE, reply)
            print(f"MIKE'S REPLY to num {i} is: ok ")
              
            data1 = reply

            call_model_2 = call_model(prompt_maker(commands2, data, mf1, cnf,user_feetback, prompt_sp_c,"RIYA", "MIKE"), temperature)

            reply, memory, summary = devider(call_model_2)
            memory_overwrite(MEMORY_FILE_2, memory)
            recent_context_overwrite(CONTEXT, summary, recent_con_size)
            initialize_files_write(CONTEXT_HISTORY, summary)
            reply = f"{i}." + reply
            initialize_files_write(OUTPUT_FILE, reply)
            print(f"RIYA'S REPLY to num {i} is: ok ")

            data = reply 
            memory_overwrite(DATA,data)
            
            sum_cal_md = call_model(prompt_maker_summery(data1, data,user_feetback), temperature)
            
            sumery,mem_of_sum = sum_mem_devider(sum_cal_md)
            memory_overwrite(MEM_OF_SUM, mem_of_sum)
            initialize_files_write(OUTPUT_FILE, sumery)
             
            print(f"SUMMERY of num {i} is: ok ")
            
            user_feetback = input("USER FEETBACK: ").strip().upper()
            memory_overwrite(USER_FEEDBACK, user_feetback)
            user_feetback = "JUDGE'S FEETBACK IS:-" + user_feetback 



if __name__ == "__main__":
    main()

