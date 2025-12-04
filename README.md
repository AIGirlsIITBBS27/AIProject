### *Medical Knowledge Graph Question Answering System* ###

A complete end-to-end medical question answering system integrating:

  -LLM-based symptom extraction
  -UMLS-powered Neo4j knowledge graph
  -Question decomposition
  -Triage question generation
  -Medical reasoning engine
  -React frontend
  -FastAPI backend

----
## Features #
-Free-text medical query interpretation
-LLM-based symptom extraction (NER)
-Knowledge graph lookup (SNOMED CT + RxNorm)
-Multi-step question decomposition
-Triage question generation
-Reasoning grounded in medical KG
-Login and signup (MYSQL)

----
## Project Structure ##
```
backend/
 └── app/
      ├── _init_.py
      ├── auth.py
      ├── database.py
      ├── kg_connector.py
      ├── llm_client.py
      ├── main.py
      ├── medical_chatbot.py
      ├── models.py
      ├── nlp_utils.py
      ├── cgi.py
      └── requirements.txt
      └── users.db
```
```
frontend/
 ├── public/
 │    ├── video/
 │    ├── im.png
 │    ├── chatbot2.jpeg
 │    ├── vite.svg
 ├── src/
 │    ├── App.jsx
 │    ├── chatbot.jsx
 │    ├── login.jsx
 │    ├── Signup.jsx
 │    ├── ForgotPassword.jsx
 │    ├── api.js
 │    ├── *.css
 │    └── main.jsx
 ├── package.json
 ├── vite.config.js
 ├── index.html
 └── .gitignore
```
```
Other Files:
 ├── primgkg graph.png
 ├── umls graph.jpeg
 |── dataset.rar
```

## **Installation and Setup** ##
 **Backend**

cd backend/app
pip install -r requirements.txt
uvicorn main:app --reload

**Backend runs at** :http://127.0.0.1:8000
## Start olama and Mistral ##
```
ollama pull mistral
ollama run mistral
```

## Neo4j Setup ##
```
Install Neo4j Desktop
Create a new database(here it is KGMAP)
Import UMLS, SNOMED CT, RxNorm data
Create constraints

Example:
CREATE CONSTRAINT concept_cui IF NOT EXISTS
FOR (c:Concept) REQUIRE c.cui IS UNIQUE;

Update kg_connector.py:
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"
```
Note: Sometimes neo4j uses neo4j instead of bolt

## API Example ##
```
Request
{
  "question": "I have fever and throat pain for two days"
}

Response
{
  "symptoms": ["fever", "throat pain"],
  "possible_conditions": ["Viral pharyngitis"],
  "analysis": "Based on symptoms and KG lookup"
}
```
**Security Notes**
Removed node_modules in frontend <br>
Removed .env file and .gitignore in backend. <br>
Login system uses MySQL
No sensitive patient data stored


## **LLM reply using Knowledge graph**
```
Install anaconda(optional)
Install ollama
```
**Run the following commands to install dependencies:** <br>
```
pip install neo4j
pip install ollama 
```
Start olama and Mistral in cmd
```
ollama pull mistral
ollama run mistral
```
**Then Connect to the instances in Neo4j Desktop**

**Then to execute the code we write as**<br>
```
python medical_chatbot.py
```
**Input and Output**
```
You: I have headache
```
```
DOCTOR: To understand your symptoms better, I need a few more details:
- When did you first start experiencing headaches?
- Can you describe the nature of your headache (e.g., throbbing, sharp, constant, intermittent)?
- Have you noticed any pattern or triggers associated with your nausea?
- What type of visual disturbances are you experiencing? Are they flashes, blurriness, floating spots, or something else?
- Have you vomited only once or multiple times? Does it occur before, during, or after the headache?
- Do you have any history of migraines or other known conditions that could be related to your symptoms?
```
```
You: 2 days, sharp, no, yes, yes
```
```
DOCTOR: Next clarification question:
- Do you have any history of migraines or other known conditions that could be related to your symptoms?
```
```
You: high blood pressure
```
```
DOCTOR: I'm really sorry that you are experiencing a headache. Headaches can have multiple causes and it's important to understand the possible reasons for your symptoms, especially when they last for more than a day or two.
Firstly, one of the potential reasons could be high blood pressure. Prolonged high blood pressure can lead to tension-type headaches, which can feel sharp o r persistent.
Another possibility is stress or fatigue, as these conditions can also trigger headaches. However, if your headache comes with other symptoms like nausea, omiting, vision changes, or an unusual sensitivity to light, it might be a sign of migraines.
```
