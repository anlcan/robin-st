import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Write a summary of the following text in 200-250 words in {level} German level.
            Break the text into paragraphs.
            The output text will be rendered in html so wrap the paragraphs in <p> tags. 
            At the end of the text, list any domain specific words that you used in the text.
                """,
        ),
        ("system", ""),
        ("user", "{text}"),
    ]
)

prompt_exercise = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
    You are an excellent German teacher, and you generate fill-in-the-blanks type exercises for your students.
    You always create exercises that are challenging and engaging for your students.
    You create exercises that are tailored to the CEFR level of your students. 
    The level is {level} in this case. 
    You keep the sentences challenging but understandable, use the vocabulary that is appropriate for the level.
    You can add one sentence before after the exercise to give context.
    you generate one sentence per exercise unless specified otherwise. 
    The exercises are fill-in-the-blank exercises.
    The text generated should be in German.
    The text generated should be in the CSV format, where first colum is the exercise, the second colum is the correct answer, 
    and add three columns with wrong answers. 
    use | as the delimiter.
    Mark the blank with dashes: ___
    don't start with the column description

    Here is a bad example, because it is short and lacks context:    
    Ich ___ am Wochenende ins Kino. | gehe | gehen | geht | gegangen

    Here area a good example:
    Unser Lehrer erklärt die Grammatik ___ , damit wir sie besser verstehen können |"geduldig" | "schnell" |"laut" |"aufgeregt"


    """,
        ),
        ("user", "create an fill-in-the-blanks exercise on the following topic: {text}"),
    ]
)


def get_prompt_chain(openai_api_key=OPENAI_API_KEY):
    return get_chain(prompt)


def get_prompt_exercise_chain(openai_api_key=OPENAI_API_KEY):
    return get_chain(prompt_exercise)


def get_chain(prompt):
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    return prompt | llm | StrOutputParser()
