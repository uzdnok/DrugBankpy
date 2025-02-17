import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

interactions_data = []

for drug in root.findall('.//ns:drug', namespaces):
    drugbank_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    drug_name = drug.findtext('ns:name', default="N/A", namespaces=namespaces)
    interactions = drug.findall('ns:drug-interactions/ns:drug-interaction', namespaces)
    description = drug.findtext('ns:description', default="N/A", namespaces=namespaces).strip(),
    state = drug.findtext('ns:state', default="N/A", namespaces=namespaces),
    intr_drugs = []
    if state[0] == 'N/A':
        continue
    for interaction in interactions:
        intr_drug_id = interaction.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
        intr_drug_name = interaction.findtext('ns:name', default="N/A", namespaces=namespaces)
        intr_drugs.append([intr_drug_id, intr_drug_name])
    interactions_data.append({
        'drugbank_id': drugbank_id,
        'interracting_drugs': list(intr_drugs),
        '# of interactions': len(intr_drugs)
    })
    int_num = 0
df_interactions = pd.DataFrame(interactions_data)

print(df_interactions)