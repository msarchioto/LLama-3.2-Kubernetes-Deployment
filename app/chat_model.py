from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

from config import MODEL_PATH, MAX_NEW_TOKENS, TEMPERATURE, TOP_P, SYSTEM_PROMPT

class ChatModel:
    def __init__(self):
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        # Create HuggingFace pipeline
        pipeline = HuggingFacePipeline(
            pipeline={
                "task": "text-generation",
                "model": self.model,
                "tokenizer": self.tokenizer,
                "max_new_tokens": MAX_NEW_TOKENS,
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "return_full_text": False
            }
        )

        # Create conversation template
        template = f"""{{history}}
Human: {{input}}
Assistant: """

        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )

        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            return_messages=True,
            human_prefix="Human",
            ai_prefix="Assistant"
        )

        # Create conversation chain
        self.conversation = ConversationChain(
            llm=pipeline,
            memory=self.memory,
            prompt=prompt,
            verbose=False
        )

        # Initialize system prompt
        self.memory.chat_memory.add_ai_message(SYSTEM_PROMPT)

    async def generate_response(self, message: str) -> Dict:
        """
        Generate a response for the given message using the conversation chain.
        """
        try:
            response = self.conversation.predict(input=message)
            return {
                "response": response,
                "error": None
            }
        except Exception as e:
            return {
                "response": None,
                "error": str(e)
            }

    def get_conversation_history(self) -> List[Dict]:
        """
        Return the conversation history.
        """
        return [
            {
                "role": msg.type,
                "content": msg.content
            }
            for msg in self.memory.chat_memory.messages
        ] 