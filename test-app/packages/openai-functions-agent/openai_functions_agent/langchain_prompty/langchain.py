from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, Runnable
from typing import Dict
from .utils import load, prepare

def create_chat_prompt(path: str, input_name_agent_scratchpad = "agent_scratchpad") -> Runnable[Dict[str, ChatPromptTemplate], str]:
    def runnable_chat_lambda(inputs: Dict[str, any]) -> ChatPromptTemplate:
        p = load(path)
        parsed = prepare(p, inputs)
        lc_messages = []
        for message in parsed:
            lc_messages.append((message["role"], message["content"]))
        
        lc_messages.append(MessagesPlaceholder(variable_name=input_name_agent_scratchpad, optional=True))
        lc_p = ChatPromptTemplate.from_messages(lc_messages)
        lc_p = lc_p.partial(**p.inputs)

        return lc_p
    return RunnableLambda(runnable_chat_lambda)
