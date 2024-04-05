from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a summary of the following in 200-250 words in B2 German level break it into"),
    ("system", "the output text will be rendered in html so wrap the paragraps in <p> tags"),
    ("user", "{text}")
])

prompt_exercise = ChatPromptTemplate.from_messages([
    ("system", """
    You are an excellent German teacher, and you generate exercises for your students.
    You always create exercises that are challenging and engaging for your students.
    You create exercises that are tailored to the level of your students, which is {level} in this case. 
    You keep the sentences challenging but understandable, use the vocabulary that is appropriate for the level.
    you generate one sentence per exercise unless specified otherwise. 
    The exercises are fill-in-the-blank exercises.
    The text generated should be in German.
    The text generated should be in the CSV format, where first colum is the exercise, the second colum is the correct answer, 
    and add three columns with wrong answers. use | as the delimiter.
    Mark the blank with dashes: ___
    don't start with the column description

    Here is a bad example, becuase it is short and lacks context:
    Ich ___ am Wochenende ins Kino. | gehe | gehen | geht | gegangen

    Here area a good example:
    Unser Lehrer erklärt die Grammatik ___ , damit wir sie besser verstehen können |"geduldig" | "schnell" |"laut" |"aufgeregt"


    """),
    ("user", "create an exercise on the following topic: {text}")
])

def get_prompt_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt | llm | StrOutputParser()

def get_prompt_exercise_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt_exercise | llm | StrOutputParser()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a summary of the following in 200-250 words in B2 German level break it into"),
    ("system", "the output text will be rendered in html so wrap the paragraps in <p> tags"),
    ("user", "{text}")
])

prompt_exercise = ChatPromptTemplate.from_messages([
    ("system", """
    You are an excellent German teacher, and you generate exercises for your students.
    You always create exercises that are challenging and engaging for your students.
    You create exercises that are tailored to the level of your students, which is {level} in this case. 
    You keep the sentences challenging but understandable, use the vocabulary that is appropriate for the level.
    you generate one sentence per exercise unless specified otherwise. 
    The exercises are fill-in-the-blank exercises.
    The text generated should be in German.
    The text generated should be in the CSV format, where first colum is the exercise, the second colum is the correct answer, 
    and add three columns with wrong answers. use | as the delimiter.
    Mark the blank with dashes: ___
    don't start with the column description

    Here is a bad example, becuase it is short and lacks context:
    Ich ___ am Wochenende ins Kino. | gehe | gehen | geht | gegangen

    Here area a good example:
    Unser Lehrer erklärt die Grammatik ___ , damit wir sie besser verstehen können |"geduldig" | "schnell" |"laut" |"aufgeregt"


    """),
    ("user", "create an exercise on the following topic: {text}")
])

def get_prompt_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt | llm | StrOutputParser()

def get_prompt_exercise_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt_exercise | llm | StrOutputParser()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a summary of the following in 200-250 words in B2 German level break it into"),
    ("system", "the output text will be rendered in html so wrap the paragraps in <p> tags"),
    ("user", "{text}")
])

prompt_exercise = ChatPromptTemplate.from_messages([
    ("system", """
    You are an excellent German teacher, and you generate exercises for your students.
    You always create exercises that are challenging and engaging for your students.
    You create exercises that are tailored to the level of your students, which is {level} in this case. 
    You keep the sentences challenging but understandable, use the vocabulary that is appropriate for the level.
    you generate one sentence per exercise unless specified otherwise. 
    The exercises are fill-in-the-blank exercises.
    The text generated should be in German.
    The text generated should be in the CSV format, where first colum is the exercise, the second colum is the correct answer, 
    and add three columns with wrong answers. use | as the delimiter.
    Mark the blank with dashes: ___
    don't start with the column description

    Here is a bad example, becuase it is short and lacks context:
    Ich ___ am Wochenende ins Kino. | gehe | gehen | geht | gegangen

    Here area a good example:
    Unser Lehrer erklärt die Grammatik ___ , damit wir sie besser verstehen können |"geduldig" | "schnell" |"laut" |"aufgeregt"


    """),
    ("user", "create an exercise on the following topic: {text}")
])

def get_prompt_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt | llm | StrOutputParser()

def get_prompt_exercise_chain(openai_api_key):
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    return prompt_exercise | llm | StrOutputParser()
