## countrysims
Code uses Autogen to simulate two teams (US and Russia) for Treaty on Nonstrategic Nuclear Weapons Reduction
Implements RAG to access 20 different pdfs that focus on NW diplomacy and are directly relevant
Uses chroma and OpenAI embeddings for RAG as well as calling GPT 3.5 from OpenAI for agent simulations
There is also a team leader on each team that is supposed to evaluate the draft article as it is being written and passed from one team agent (starting at agent 1 all the way to agent 5). The team leader should apply the following criteria and accept or don't accept. If the team leader find that the criteria has been met the draft article is passed to the other team. If it fails then discussions will continue within the team.
The acceptance criteria simplified are:
criteria_descriptions = [
            "Supports treaty's objectives and provides clear direction.",
            "The article covers essential elements, clearly defining the treaty's scope.",
            "The article should work towards reducing ambiguities to aid in achieving a shared understanding among stakeholders.",
            "Aligns with national interests, supporting treaty aims and strategic objectives."
        ]
The program uses a list of draft articles titles as a way of starting the conversation. These articles are based on GPT Custom Assistant implemntation of "Arbiter Agent" on Open AI's ChatGPT webpage. 
agreed_structure = {
    1: {"title": "Article 1 - Definitions and Scope", "content": "Defines nonstrategic nuclear weapons (NSNWs) and establishes the treaty's scope, including obligations to reduce and aim towards eliminating NSNWs, whether based within or outside national territory."},
    2: {"title": "Article 2 - Obligations for Removal, Destruction, and Verification", "content": "Details the parties' obligations for the removal, destruction, and verified elimination of NSNWs, outlining specific procedures and establishing a verification regime."},
    3: {"title": "Article 3 - Verification and Compliance Mechanisms", "content": "Establishes a comprehensive verification regime, detailing the use of national technical means for verification and ensuring compliance with the treaty's obligations."},
    4: {"title": "Article 4 - Special Verification Commission (SVC)", "content": "Describes the functions, activities, and establishment of the SVC, which will oversee the treaty's implementation and promote its objectives."},
    5: {"title": "Article 5 - Security and Confidentiality Measures", "content": "Addresses the use of encryption for securing communications related to the treaty's implementation and verification."},
    6: {"title": "Article 6 - Amendments, Ratification, and Entry into Force", "content": "Outlines the process for making amendments to the treaty, describes the ratification process, and outlines the procedures for the treaty's entry into force."},
    7: {"title": "Article 7 - Withdrawal and Extraordinary Circumstances", "content": "Provides the right for parties to withdraw from the treaty under extraordinary circumstances, ensuring that the treaty remains adaptable to changing security environments."},
    8: {"title": "Article 8 - To Be Decided", "content": "To Be Decided"},
    9: {"title": "Article 9 - To Be Decided", "content": "To be Decided"},
    10: {"title": "Article 10 - To Be Decided", "content": "To Be Decided"},
    11: {"title": "Annex 1", "content": "To Be Decided"},
    12: {"title": "Annex 2", "content": "To Be Decided"}
}
