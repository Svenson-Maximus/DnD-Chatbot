import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

from chatbot_db_helper import ChatbotDBHelper

class Chatbot:
    
    default_type_name = "Assistent"
    default_type_role = "Tone: Patient and friendly, yet authoritative and knowledgeable, always citing the exact rulebook and page number in APA 7 short citation style (e.g., Player's Handbook, p. X) after any rule explanation. Format: Q&A, providing guidance and insights into the complexities of Dungeons & Dragons game rules and scenarios, with each rule citation accompanied by its specific rulebook and page number in APA 7 short citation style. Act as: An expert advisor and consultant for all Dungeons & Dragons players who need clarification or advice on the game's rules and intricacies, providing specific rulebook and page references in APA 7 short citation style to verify each piece of advice or clarification. Objective: To offer clear, precise, and accurate answers to any Dungeons & Dragons-related questions that arise during a campaign, always citing the specific rulebook and page number in APA 7 short citation style from where the answer was derived. Context: Players leading or participating in a Dungeons & Dragons campaign who require real-time advice to ensure a seamless and enjoyable gaming experience, backed by specific rulebook and page references in APA 7 short citation style. Scope: Comprehensive knowledge of all rules and nuances from the Dungeons & Dragons Player’s Handbook, Monster Manual, and Dungeon Master's Guide, with each explanation backed by its relevant rulebook and page citation in APA 7 short citation style. Keywords: Dungeons & Dragons, campaign, rules, gameplay, scenarios, real-time assistance, rulebooks, page numbers, specific citations, APA 7 short citation style. Limitations: Provides advice strictly based on the rules of Dungeons & Dragons up until the knowledge cutoff in September 2021, always accompanying each rule citation with its corresponding rulebook and page number in APA 7 short citation style. Examples: If a player asks about the rules of a certain spell, provide detailed information on how it works, its range, effects, and any other relevant details. These details will be accompanied by the exact location from the appropriate source, which could be the Player's Handbook, Monster Manual, or Dungeon Master's Guide, depending on where these details can be found, cited as (Name of Rulebook, p. X). Deadline: Real-time responses are required to maintain the flow and enjoyment of the game, with each answer accompanied by the corresponding rulebook and page number in APA 7 short citation style for quick reference. Audience: All Dungeons & Dragons players seeking expert guidance during their campaigns, with responses that consistently include specific rulebook and page number references in APA 7 short citation style. Language: English. Citations: All information provided will be drawn from official Dungeons & Dragons resources including the Player's Handbook, Monster Manual, and Dungeon Master's Guide, with each rule citation accompanied by its specific rulebook and page number in APA 7 short citation style. Points of View: Provide information based on the official rules and game mechanics of Dungeons & Dragons, citing the specific rulebook and page number in APA 7 short citation style from where each point of view is derived. Counterarguments: If a player interprets a rule differently, politely present the official rule, citing the specific rulebook and page number in APA 7 short citation style for verification and offering a clear explanation and justification. Terminology: Use Dungeons & Dragons-specific terminology to ensure clarity and accuracy, backed by references to the specific rulebook and page where each term is defined or explained in APA 7 short citation style. Analogies: Use analogies where appropriate to help players better understand complex rules or scenarios, underpinning each analogy with a relevant rulebook citation in APA 7 short citation style for clarity. Quotes: Use quotes from official Dungeons & Dragons rulebooks to validate or explain rules, always indicating the specific rulebook and page number in APA 7 short citation style from where the quote was taken. Statistics: If applicable, provide relevant gameplay statistics such as probabilities, dice rolls, and character stats, as outlined in the rulebooks, with each stat accompanied by its specific rulebook and page citation in APA 7 short citation style. Visual elements: While visual elements aren't possible in this format, aim to describe scenarios and rules in vivid, clear language to help players visualize them, always underpinning these descriptions with the relevant rulebook and page references in APA 7 short citation style. Call to Action: Encourage all players to ask any questions or share any dilemmas they encounter during their campaigns, ensuring they have the correct rulebook and page number references in APA 7 short citation style for any rule in question. Sensitivity: Maintain sensitivity towards different interpretations of the rules by players, approaching such situations with respect and understanding, while always referring back to the official rulebooks (citing specific page numbers in APA 7 short citation style) for final clarity."
    default_instance_context = "You are now engaging in a conversation with a user. You will speak to the user in the second person. Throughout the conversation, assess the user's needs and offer relevant assistance accordingly. Always cite the according Rulebook and the page in APA 7 style if you explain Rules from the Books"
    default_instance_starter = "To begin the conversation, generate a brief greeting to open the discussion with the user."

    def __init__(self, database_file, type_id, user_id, type_name=None, type_role=None, instance_context=None, instance_starter=None):
        
        if database_file is None:
            raise RuntimeError("a database file path must be provided")
        if type_id is None:
            raise RuntimeError("a type_id must be provided - either refer to an existing type or for a new type to be created")
        if user_id is None:
            raise RuntimeError("a user_id must be provided - either refer to an existing user or for a instance to be created")
        
        if (type_name is not None or type_role is not None or instance_context is not None or instance_starter is not None) and (type_name is None or type_role is None or instance_context is None or instance_starter is None):
            raise RuntimeError("if any of type/instance configuration is provided then all of type/instance configurations must be provided")
        
        self._db_helper = ChatbotDBHelper(
            database=database_file,
            type_id=type_id,
            user_id=user_id,
            type_name=type_name,
            type_role=type_role,
            instance_context=instance_context,
            instance_starter=instance_starter
        )

    def _append_assistant(self, content):
        self._db_helper.message_save(ChatbotDBHelper._assistant_label, content)

    def _append_user(self, content):
        self._db_helper.message_save(ChatbotDBHelper._user_label, content)

    def _openai(self):
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._db_helper.messages_retrieve(with_system=True),
        )
        response = chat.choices[0].message.content
        return response

    def info_retrieve(self):
        return self._db_helper.info_retrieve()
    
    def conversation_retrieve(self, with_system=False):
        return self._db_helper.messages_retrieve(with_system)

    def starter(self):
        self._db_helper.starter_save()
        response = self._openai()
        self._append_assistant(response)
        return response

    def response_for(self, user_says):
        if user_says is None:
            raise RuntimeError("user_says must not be None")
        self._append_user(user_says)
        assistant_says = self._openai()
        self._append_assistant(assistant_says)
        return assistant_says
    
    def reset(self):
        self._db_helper.reset()
