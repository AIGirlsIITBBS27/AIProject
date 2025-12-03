# app/kg_connector.py
from neo4j import GraphDatabase, basic_auth
import os

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "Surbhi@123")
KG_DB = "kgmap"


class KGConnector:
    def __init__(self, neo4j_uri=None, neo4j_user=None, neo4j_password=None):
        try:
            self.driver = GraphDatabase.driver(
                neo4j_uri,
                auth=basic_auth(neo4j_user, neo4j_password)
            )
            print("Neo4j connected.")
        except Exception as e:
            print("Neo4j connection failed:", e)
            self.driver = None

    def query(self, symptom_text: str):
        """Search symptom → diseases → remedies."""
        if not self.driver:
            return []

        symptom_text = symptom_text.lower()

        query = """
        MATCH (s:SymptomNode)
        WHERE toLower(s.name) CONTAINS $q

        OPTIONAL MATCH (s)-[:CAUSES]->(d:DiseaseNode)
        OPTIONAL MATCH (s)-[:HOME_REMEDY]->(r:RemedyNode)

        RETURN {
            symptom: s.name,
            diseases: collect(DISTINCT d.name),
            remedies: collect(DISTINCT r.name)
        } AS result
        LIMIT 1
        """

        try:
            with self.driver.session(database=KG_DB) as session:
                data = session.run(query, q=symptom_text)
                results = [rec["result"] for rec in data]
                return results if results else []
        except Exception as e:
            print("Neo4j query error:", e)
            return []
