from fastapi import FastAPI, Request, Body
import xml.etree.ElementTree as ET
from collections import defaultdict

app = FastAPI()


tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

interaction_data = []
pathway_data = []
pathways_count = defaultdict(int)
for drug in root.findall('.//ns:drug', namespaces):
    drugbank_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    pathways = drug.findall('ns:pathways/ns:pathway', namespaces = namespaces)
    for pathway in pathways:
        pathway_drugs = pathway.findall('ns:drugs/ns:drug', namespaces=namespaces)
        for pathway_drug in pathway_drugs:
            pathways_count[drugbank_id] += 1
    if pathways_count[drugbank_id] == 0:
        pathways_count[drugbank_id] = 0


@app.post("/drug-pathways")
def get_drug_pathways(drugbank_id: str = Body("DB00001", embed=True)):
    if drugbank_id not in pathways_count:
        return {"error": f"Lek o ID {drugbank_id} nie został znaleziony."}
    return {"drugbank_id": drugbank_id, "Ilość ścieżek": pathways_count[drugbank_id]}

