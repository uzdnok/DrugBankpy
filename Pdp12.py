import xml.etree.ElementTree as ET
from collections import defaultdict

import pandas as pd
import requests

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial_and_generated.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

data = []
diseases = defaultdict(int)
responses = {}
all_uniprot_ids = []
drug_uniprot_id = {}
def get_uniprot_data_xml(uniprot_ids):
    for uniprot_id in uniprot_ids:
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
        response = requests.get(url)
        if response.status_code == 200:
            responses[uniprot_id] = response.text

for drug in root.findall('.//ns:drug', namespaces):  # Zawczasu pobieranie wszystkich informcji z Uniprot - tak jest szybciej
    drug_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    drug_groups = drug.findall('ns:groups/ns:group', namespaces)
    targets = drug.findall('ns:targets/ns:target', namespaces)
    for target in targets:
        target_name = target.findtext('ns:name', default="N/A", namespaces=namespaces)
        polypeptide = target.find('ns:polypeptide', namespaces=namespaces)
        Uniprot_id = "N/A"
        if polypeptide is not None:
            for ext_id in target.findall('.//ns:external-identifier', namespaces):
                resource = ext_id.find('ns:resource', namespaces).text
                if resource == "UniProtKB":
                    Uniprot_id = ext_id.find('ns:identifier', namespaces).text
        drug_uniprot_id[drug_id] = Uniprot_id
        if Uniprot_id != "N/A" and Uniprot_id not in all_uniprot_ids:
            all_uniprot_ids.append(Uniprot_id)

get_uniprot_data_xml(all_uniprot_ids)

for drug in root.findall('.//ns:drug', namespaces):
    drug_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    if drug.findtext('ns:description', default="N/A", namespaces=namespaces).strip() is None and drug.findtext('ns:state', default="N/A", namespaces=namespaces) is None:
        continue
    print(drug_id)
    drug_groups = drug.findall('ns:groups/ns:group', namespaces)
    targets = drug.findall('ns:targets/ns:target', namespaces)
    for target in targets:
        target_name = target.findtext('ns:name', default="N/A", namespaces=namespaces)
        polypeptide = target.find('ns:polypeptide', namespaces=namespaces)
        Uniprot_id = "N/A"
        if polypeptide is not None:
            for ext_id in target.findall('.//ns:external-identifier', namespaces):
                resource = ext_id.find('ns:resource', namespaces).text
                if resource == "UniProtKB":
                    Uniprot_id = ext_id.find('ns:identifier', namespaces).text

        if Uniprot_id != "N/A":
            uniprot_data = responses[Uniprot_id]
            if uniprot_data:
                uniprot_root = ET.fromstring(uniprot_data)
                namespaces_uniprot = {'up': 'http://uniprot.org/uniprot'}
                disease_comments = uniprot_root.findall('.//up:comment[@type="disease"]', namespaces=namespaces_uniprot)
                for comment in disease_comments:
                    diseases[drug_id] += 1

import matplotlib.pyplot as plt

sorted_items = sorted(diseases.items(), key=lambda x: x[1], reverse=True)
drug_ids, disease_counts = zip(*sorted_items)

plt.figure(figsize=(12, 8))

plt.bar(drug_ids, disease_counts, color='skyblue')

plt.xlabel("ID leku")
plt.ylabel("Liczba chorób")
plt.title("Liczba chorób związanych z targetami dla poszczególnych leków")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


