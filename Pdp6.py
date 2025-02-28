import xml.etree.ElementTree as ET
from collections import defaultdict

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

def create_dictPDP6(path):
    tree = ET.parse(path)
    root = tree.getroot()

    namespaces = {'ns': 'http://www.drugbank.ca'}

    pathways_count = defaultdict(int)
    interaction_counts = defaultdict(int)
    for drug in root.findall('.//ns:drug', namespaces):
        pathways = drug.findall('ns:pathways/ns:pathway', namespaces = namespaces)
        drug_name = drug.findtext('ns:name', default="N/A", namespaces=namespaces)
        for pathway in pathways:
            pathway_drugs = pathway.findall('ns:drugs/ns:drug', namespaces=namespaces)
            for pathway_drug in pathway_drugs:
                drug_name = pathway_drug.findtext('ns:name', default="N/A", namespaces=namespaces)
                pathways_count[drug_name] += 1
        print(pathways_count[drug_name], drug_name)
        interaction_counts[pathways_count[drug_name]] += 1
        if pathways_count[drug_name] != 0:
            interaction_counts[pathways_count[drug_name] - 1] -= 1
    return dict(interaction_counts)

interaction_counts = create_dictPDP6("drugbank_partial.xml")
print(interaction_counts)
drugs = list(interaction_counts.keys())
counts = list(interaction_counts.values())

plt.bar(drugs, counts)
plt.title('Histogram liczby interakcji dla leków')
plt.xlabel('Liczba Interakcji')
plt.ylabel('Liczba leków o danyej liczbie interakcji')
plt.xticks(rotation=90)
#plt.show()
