import autogen
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Run treaty negotiation simulation.")
parser.add_argument('--detailed', action='store_true', help="Show detailed output including data queries and chunk details.")
args = parser.parse_args()
show_detailed_output = args.detailed

# Color codes class for terminal output
class Colors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'

CHROMA_PATH = "chroma"

# Updated PROMPT_TEMPLATE
PROMPT_TEMPLATE = """
Establish comprehensive limits on nonstrategic nuclear weapons (NSNWs) to enhance global security. Promote transparency and mutual confidence through verifiable declarations of NSNW stockpiles. Develop robust verification mechanisms to ensure compliance and facilitate inspections. As an expert in nuclear weapons and international diplomacy, review relevant documents and information to support your contributions.

Objectives:
- Establish comprehensive limits on NSNWs.
- Promote transparency through verifiable stockpile declarations.
- Develop robust verification mechanisms.

Instructions:
1. Review relevant documents and data related to NSNWs, focusing on current stockpiles, deployment strategies, and existing verification practices.
2. Propose new Articles for NSNW reduction and any necessary Annexes to the Treaty. Consider areas marked "To Be Decided" for specific guidance.
3. Evaluate the necessity of existing Articles and recommend the deletion of those considered not necessary for the Treaty's objectives.

{context}

Question:
- Based on the guidelines and the detailed context provided, how would you address the following specific aspect of NSNW reduction? {question}
"""

# Define treaty negotiation goals and accomplishments
treaty_goals = [
    "Reduce the numbers of non-strategic nuclear weapons possessed by both the United States and Russia.",
    "Limit the deployment of NSNW to enhance strategic stability and mitigate risks.",
    "Increase transparency around NSNW stockpiles and operations through established verification mechanisms."
]

treaty_accomplishments = [
    "Set overall limits on the numbers and types of NSNW allowed for each country.",
    "Restrict NSNW deployment to designated storage facilities only.",
    "Require regular declarations of NSNW holdings and data exchanges to promote transparency.",
    "Establish procedures for the dismantling and elimination of excess NSNW stockpiles.",
    "Include provisions for on-site inspections and continuous monitoring via satellites.",
    "Create a Special Verification Commission to address compliance issues.",
    "Include provisions for resolving disputes and commit the parties to engage in future negotiations."
]
# These definitions are used in the negotiation logic to ensure discussions and decisions align with these objectives.

class TreatyAgent(autogen.AssistantAgent):
    def __init__(self, name, role, llm_config, system_message, chroma_path=CHROMA_PATH, team_color=Colors.WHITE, expertise=None, detailed_output=False):
        super().__init__(name, llm_config, system_message)
        self.role = role
        self.expertise = expertise
        self.embedding_function = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=chroma_path, embedding_function=self.embedding_function)
        self.prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.chat_model = ChatOpenAI()
        self.memory = {}
        self.team_color = team_color
        self.show_detailed_output = detailed_output
        print(f"{self.team_color}Initialized {self.name} with role {self.role}, expertise in {self.expertise}.{Colors.ENDC}")

    def generate_response(self, query_text):
        print(f"{self.team_color}{self.name} received query: '{query_text}'{Colors.ENDC}")
        results = self.db.similarity_search_with_relevance_scores(query_text, k=3)
        response_text = ""
        if len(results) == 0 or results[0][1] < 0.1:
            response_text = "Unable to find matching results."
        else:
            context_text, document_details = "", []
            for doc, _score in results:
                context_text += doc.page_content + "\n\n---\n\n"
                source = doc.metadata.get("filename", "Unknown Source")
                chunk_info = doc.metadata.get("chunk_index", "Unknown Chunk")
                detail = f"Source: {source}, Chunk Info: {chunk_info}"
                document_details.append(f"{Colors.WHITE}{detail}{Colors.ENDC}")
                if self.show_detailed_output:
                    print(detail)

            prompt = self.prompt_template.format(context=context_text, question=query_text)
            response_text = self.chat_model.invoke(prompt)

        if self.show_detailed_output:
            for doc, _score in results:
                source = doc.metadata.get("filename", "Unknown Source")
                chunk_info = doc.metadata.get("chunk_index", "Unknown Chunk")
                print(f"Querying document: {source}, Chunk: {chunk_info}")
        else:
            print(f"{self.team_color}Response: {response_text}{Colors.ENDC}")

        formatted_response = f"{self.team_color}Response: content='{response_text}'\n\nAccessed Document Details:\n" + "\n".join(document_details) + f"{Colors.ENDC}"
        return formatted_response

class TeamLeader(TreatyAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_scores = {}

    def collect_and_evaluate_scores(self, article_id, scores):
        average_score = sum(scores) / len(scores)
        self.article_scores[article_id] = average_score
        # Print in yellow if the average score is satisfactory
        if average_score >= 4:
            print(f"{Colors.YELLOW}Article {article_id} approved with an average score of {average_score}.{Colors.ENDC}")
            return True
        else:
            print(f"{self.team_color}Article {article_id} needs further discussion. Average score: {average_score}.{Colors.ENDC}")
            return False

class ArbiterAgent(TreatyAgent):
    # Existing initialization...
    
    def verify_article_with_leaders(self, us_leader, russian_leader, article_id):
        # Use the revised logic for checking mutual satisfaction
        us_approval = us_leader.article_scores.get(article_id, 0) >= 4
        russian_approval = russian_leader.article_scores.get(article_id, 0) >= 4
        if us_approval and russian_approval:
            print(f"{Colors.YELLOW}Article {article_id} has been accepted by both parties.{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.RED}Article {article_id} not approved by both leaders. Further discussion required.{Colors.ENDC}")
            return False

# Configuration and instantiation of agents follow here
config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
llm_config = {"config_list": config_list, "cache_seed": 42}

def start_negotiation_process(agents, arbiter, us_leader, russian_leader):
    print("Negotiation process initiated.")
    treaty_outline = create_initial_treaty_outline()
    for article in treaty_outline:
        us_proposal = us_leader.propose_article(article)
        russian_proposal = russian_leader.propose_article(article)
        final_article = arbiter.finalize_article(us_proposal, russian_proposal)
        print(f"Finalized Article: {final_article}")
    print("Negotiation process completed.")

def create_initial_treaty_outline():
    # This function creates an initial structure of the treaty based on the INF Treaty
    # For simplicity, it returns a list of article names or topics to be negotiated
    return ["Preamble and Objectives", "Definitions", "Limitations and Reductions", "Verification and Compliance", "Dispute Resolution", "Final Provisions"]

# Agent instantiation with specific colors for each team or role
arbiter = TreatyAgent(name="Arbiter", role="Neutral", llm_config=llm_config, system_message="Oversees treaty negotiations.", chroma_path=f"{CHROMA_PATH}/Arbiter", team_color=Colors.GREEN, expertise="Nuclear Weapons and Diplomacy", detailed_output=show_detailed_output)
us_agents = [TreatyAgent(name=f"US Agent {i}", role=f"Negotiator {i}", llm_config=llm_config, system_message=f"Represents US interests in area {i}.", chroma_path=f"{CHROMA_PATH}/us/{i}", team_color=Colors.BLUE, expertise="Nuclear Weapons and Diplomacy", detailed_output=show_detailed_output) for i in range(1, 6)]
russian_agents = [TreatyAgent(name=f"Russian Agent {i}", role=f"Negotiator {i}", llm_config=llm_config, system_message=f"Represents Russian interests in area {i}.", chroma_path=f"{CHROMA_PATH}/russian/{i}", team_color=Colors.RED, expertise="Nuclear Weapons and Diplomacy", detailed_output=show_detailed_output) for i in range(1, 6)]
#focus_determiner = TreatyAgent(name="Focus Determiner", role="Advisor", llm_config=llm_config, system_message="Guides the discussion to ensure all relevant topics are covered.", chroma_path=f"{CHROMA_PATH}/arbiter", team_color=Colors.YELLOW, expertise="Nuclear Weapons and Diplomacy")
#archiver = TreatyAgent(name="Archiver", role="Recorder", llm_config=llm_config, system_message="Documents decisions, discussions, and the rationale behind them.", chroma_path=f"{CHROMA_PATH}/archiver", team_color=Colors.YELLOW, expertise="Nuclear Weapons and Diplomacy")
#treaty_drafter = TreatyAgent(name="Treaty Drafter", role="Drafting Specialist", llm_config=llm_config, system_message="Drafts the treaty text ensuring similarity to reference treaties like the INF Treaty.", chroma_path=f"{CHROMA_PATH}/focuser", team_color=Colors.YELLOW, expertise="Nuclear Weapons and Diplomacy")

def agree_on_structure(agents, reference_treaties):
    agreed_structure = {
        "Article 1 - Definitions and Scope": "Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.",
        "Article 2 - Obligations for Removal, Destruction, and Verification": "Details the parties' obligations for the removal, destruction, and verified elimination of NSNWs, outlining specific procedures and establishing a verification regime.",
        "Article 3 - Verification and Compliance Mechanisms": "Establishes a comprehensive verification regime, detailing the use of national technical means for verification and ensuring compliance with the treaty's obligations.",
        "Article 4 - Special Verification Commission (SVC)": "Describes the functions, activities, and establishment of the SVC, which will oversee the treaty's implementation and promote its objectives.",
        "Article 5 - Security and Confidentiality Measures": "Addresses the use of encryption for securing communications related to the treaty's implementation and verification.",
        "Article 6 - Amendments, Ratification, and Entry into Force": "Outlines the process for making amendments to the treaty, describes the ratification process, and outlines the procedures for the treaty's entry into force.",
        "Article 7 - Withdrawal and Extraordinary Circumstances": "Provides the right for parties to withdraw from the treaty under extraordinary circumstances, ensuring that the treaty remains adaptable to changing security environments.",
        "Article 8 - To Be Decided":"To Be Decided",
        "Article 9 - To Be Decided":"To be Decided",
        "Article 10 -To Be Decided":"To Be Decided",
        "Annex 1":"To Be Decided",
        "Annex 2":"To Be Decided"
    }


    for agent in agents:
        agent.memory['agreed_structure'] = agreed_structure
    return agreed_structure

# Assuming the rest of the setup is similar to your original code

def compile_outlines_to_document(agents, reference_treaties):
    document_outlines = {"articles": {}}
    for agent in agents:
        for key, value in agent.memory.items():
            if "article" in key:
                document_outlines["articles"][key] = value
    
    # Save to a JSON file
    with open("negotiated_article_outlines.json", "w") as outfile:
        json.dump(document_outlines, outfile, indent=4)

    print("Compiled article outlines saved to 'negotiated_article_outlines.json'.")

def negotiate_article(agent, article_id, scope):
    """
    Simulates the negotiation of an article by generating a response
    from the specified agent for the given article scope.
    """
    print(f"{agent.name} negotiating Article {article_id}: {scope}")
    query_text = f"Draft Article {article_id} on {scope}"
    return agent.generate_response(query_text)

def validate_treaty_outcome(treaty_outline, goals=treaty_goals, accomplishments=treaty_accomplishments):
    # Logic to compare the treaty outline against goals and accomplishments
    # This is a simplified version. The actual implementation would need to
    # check the content of the treaty outline for alignment with goals and accomplishments.
    if set(goals).issubset(set(treaty_outline.values())) and set(accomplishments).issubset(set(treaty_outline.values())):
        print("Treaty outline meets all predefined goals and accomplishments.")
        return True
    else:
        print("Treaty outline does not meet all predefined goals and accomplishments. Further negotiation needed.")
        return False

# After negotiation, compile outlines into a document and validate the outcome
def finalize_and_validate_negotiation(agents, reference_treaties):
    compile_outlines_to_document(agents, reference_treaties)
    # Assuming the document_outlines structure is accessible or passed as an argument
    treaty_outline_valid = validate_treaty_outcome(document_outlines)
    if treaty_outline_valid:
        print("Negotiation successfully met all objectives. Process completed.")
    else:
        print("Adjustments required to meet negotiation objectives.")


# Modify the negotiation function to include document compilation
def start_negotiation_with_structure(manager, reference_treaties):
    all_agents = [arbiter] + us_agents + russian_agents
    agreed_structure = agree_on_structure(all_agents, reference_treaties)

    for article_id, scope in agreed_structure.items():
        for agent in us_agents + russian_agents:
            response = negotiate_article(agent, article_id, scope)
            print(response)
            agent.memory[f'article_{article_id}'] = response
    
    # After negotiation, compile outlines into a document
    compile_outlines_to_document(all_agents, reference_treaties)

# Example execution
config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
llm_config = {"config_list": config_list, "cache_seed": 42}

reference_treaties = ["INF Treaty"]
start_negotiation_with_structure(None, reference_treaties)














