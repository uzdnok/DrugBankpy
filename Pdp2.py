import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial_and_generated.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

data = []
synonyms_dict = {}
og_name = {}

for drug in root.findall('.//ns:drug', namespaces):
    drugbank_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    name = drug.findtext('ns:name', default="N/A", namespaces=namespaces)
    synonyms = [synonym.text for synonym in drug.findall('ns:synonyms/ns:synonym', namespaces=namespaces)]

    if drugbank_id != "N/A" and synonyms:
        data.append({
            'drugbank-id': drugbank_id,
            'name': name,
            'synonyms': synonyms
        })

        synonyms_dict[drugbank_id] = synonyms
        og_name[drugbank_id] = name

df = pd.DataFrame(data)
print(df)

def draw_synonym_graph(drugbank_id):
    if drugbank_id not in synonyms_dict:
        print(f"Nie znaleziono synonimów dla {drugbank_id}.")
        return

    original_name = og_name[drugbank_id]
    synonyms = synonyms_dict[drugbank_id]

    G = nx.Graph()

    G.add_node(drugbank_id, label=original_name, type='original')

    for synonym in synonyms:
        G.add_node(synonym, label=synonym, type='synonym')
        G.add_edge(drugbank_id, synonym)

    pos = nx.spring_layout(G, k=0.5, iterations=50)
    labels = nx.get_node_attributes(G, 'label')
    node_types = nx.get_node_attributes(G, 'type')

    node_colors = ['skyblue' if node_types[node] == 'synonym' else 'lightgreen' for node in G.nodes()]

    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color=node_colors, font_size=10, font_weight='bold', edge_color='gray')

    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', font_color='black', verticalalignment="center")

    plt.title(f'Graf synonimów dla {drugbank_id}')
    plt.show()

draw_synonym_graph('DB00002')