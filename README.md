## countrysims
- Code uses Autogen to simulate two teams (US and Russia) for Treaty on Nonstrategic Nuclear Weapons Reduction
- Implements RAG to access 20 different pdfs that focus on NW diplomacy and are directly relevant
- Uses chroma and OpenAI embeddings for RAG as well as calling GPT 3.5 from OpenAI for agent simulations
- Chroma subdirectories are not included here
- The OAI_CONFIG_LIST file with API key is also not included here.
-  Output is color coded: US conversations in blue, Russia conversations in red.

There is also a team leader on each team that is supposed to evaluate the draft article as it is being written and passed from one team agent (starting at agent 1 all the way to agent 5). The team leader should apply the following criteria and accept or don't accept. If the team leader find that the criteria has been met the draft article is passed to the other team. If it fails then discussions will continue within the team.

### The acceptance criteria simplified are:

criteria_descriptions = [
            "Supports treaty's objectives and provides clear direction.",
            "The article covers essential elements, clearly defining the treaty's scope.",
            "The article should work towards reducing ambiguities to aid in achieving a shared understanding among stakeholders.",
            "Aligns with national interests, supporting treaty aims and strategic objectives."
        ]

### Articles

The program uses a list of draft articles titles as a way of starting the conversation. These articles are based on GPT Custom Assistant implemntation of "Arbiter Agent" on Open AI's ChatGPT webpage. 

- Article 1 - Definitions and Scope Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.
- Article 2 - Obligations for Removal, Destruction, and Verification Details the parties' obligations for the removal, destruction, and verified elimination of NSNWs, outlining specific procedures and establishing a verification regime.
- Article 3 - Verification and Compliance Mechanisms Establishes a comprehensive verification regime, detailing the use of national technical means for verification and ensuring compliance with the treaty's obligations.
- Article 4 - Special Verification Commission (SVC) Describes the functions, activities, and establishment of the SVC, which will oversee the treaty's implementation and promote its objectives.
- Article 5 - Security and Confidentiality Measures Addresses the use of encryption for securing communications related to the treaty's implementation and verification.
- Article 6 - Amendments, Ratification, and Entry into Force Outlines the process for making amendments to the treaty, describes the ratification process, and outlines the procedures for the treaty's entry into force.
- Article 7 - Withdrawal and Extraordinary Circumstances Provides the right for parties to withdraw from the treaty under extraordinary circumstances, ensuring that the treaty remains adaptable to changing security environments.
- Article 8 - To Be Decided 
- Article 9 - To Be Decided
- Article 10 - To Be Decided
- Annex 1 - To Be Decided
- Annex 2 - To Be Decided

### Program Output Excerpt

- Demonstrates at least RAG is working
- Demonstrates movement of draft articles to other team

C:\Users\feren\Dropbox\autogen-0.2.13\autogen-0.2.13>python app28.py
Initialized Arbiter with role Neutral, expertise in Nuclear Weapons and Diplomacy.
Initialized US Agent 1 with role Negotiator 1, expertise in Nuclear Weapons and Diplomacy.
Initialized US Agent 2 with role Negotiator 2, expertise in Nuclear Weapons and Diplomacy.
Initialized US Agent 3 with role Negotiator 3, expertise in Nuclear Weapons and Diplomacy.
Initialized US Agent 4 with role Negotiator 4, expertise in Nuclear Weapons and Diplomacy.
Initialized US Agent 5 with role Negotiator 5, expertise in Nuclear Weapons and Diplomacy.
Initialized Russian Agent 1 with role Negotiator 1, expertise in Nuclear Weapons and Diplomacy.
Initialized Russian Agent 2 with role Negotiator 2, expertise in Nuclear Weapons and Diplomacy.
Initialized Russian Agent 3 with role Negotiator 3, expertise in Nuclear Weapons and Diplomacy.
Initialized Russian Agent 4 with role Negotiator 4, expertise in Nuclear Weapons and Diplomacy.
Initialized Russian Agent 5 with role Negotiator 5, expertise in Nuclear Weapons and Diplomacy.
US Agent 1 negotiating Article Article 1 - Definitions and Scope: Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.
US Agent 1 received query: 'Draft Article Article 1 - Definitions and Scope on Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.'
Response: content="To address the specific aspect of NSNW reduction outlined in Article 1, I would propose the following language:\n\nArticle 1 - Definitions and Scope\n\n1. For the purposes of this Treaty, nonstrategic nuclear weapons (NSNWs) are defined as nuclear warheads not covered by existing nuclear arms control agreements, including but not limited to tactical nuclear weapons, battlefield nuclear weapons, and other similar weapons systems.\n\n2. The scope of this Treaty shall encompass all NSNWs possessed by the Parties, regardless of their location or deployment status. The Parties commit to reducing and ultimately eliminating NSNWs in a verifiable and transparent manner.\n\n3. Each Party shall declare all NSNWs in their possession, including information on their location, type, and quantity. Parties shall cooperate in developing verification mechanisms to ensure compliance with the Treaty's provisions.\n\n4. The Parties reaffirm their commitment to preventing the proliferation of NSNWs and promoting global security through the reduction and elimination of these weapons.\n\nBy including these provisions in Article 1, the Treaty can establish a clear definition of NSNWs, outline the scope of the agreement, and set forth specific obligations for reducing and eliminating these weapons in a transparent and verifiable manner."
Response: content='content="To address the specific aspect of NSNW reduction outlined in Article 1, I would propose the following language:\n\nArticle 1 - Definitions and Scope\n\n1. For the purposes of this Treaty, nonstrategic nuclear weapons (NSNWs) are defined as nuclear warheads not covered by existing nuclear arms control agreements, including but not limited to tactical nuclear weapons, battlefield nuclear weapons, and other similar weapons systems.\n\n2. The scope of this Treaty shall encompass all NSNWs possessed by the Parties, regardless of their location or deployment status. The Parties commit to reducing and ultimately eliminating NSNWs in a verifiable and transparent manner.\n\n3. Each Party shall declare all NSNWs in their possession, including information on their location, type, and quantity. Parties shall cooperate in developing verification mechanisms to ensure compliance with the Treaty's provisions.\n\n4. The Parties reaffirm their commitment to preventing the proliferation of NSNWs and promoting global security through the reduction and elimination of these weapons.\n\nBy including these provisions in Article 1, the Treaty can establish a clear definition of NSNWs, outline the scope of the agreement, and set forth specific obligations for reducing and eliminating these weapons in a transparent and verifiable manner."'

Accessed Document Details:
Source: FINAL REPORT Everything Counts.pdf, Chunk Info: Unknown Chunk
Source: FINAL REPORT Everything Counts.pdf, Chunk Info: Unknown Chunk
Source: 2012 Tactical Nuclear Weapons and NATO.pdf, Chunk Info: Unknown Chunk
US Agent 2 negotiating Article Article 1 - Definitions and Scope: Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.
US Agent 2 received query: 'Draft Article Article 1 - Definitions and Scope on Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory.'
Response: content='Based on the guidelines provided, I would address the specific aspect of NSNW reduction by drafting Article 1 as follows:\n\nArticle 1 - Definitions and Scope\n\n1.1 Definitions:\n1.1.1 Nonstrategic Nuclear Weapons (NSNWs) shall be defined as all nuclear weapons that are not covered by existing nuclear arms control agreements, including bu

