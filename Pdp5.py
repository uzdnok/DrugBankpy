import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

interaction_data = []
pathway_data = []
for drug in root.findall('.//ns:drug', namespaces):
    pathways = drug.findall('ns:pathways/ns:pathway', namespaces=namespaces)
    for pathway in pathways:
        pathway_name = pathway.findtext('ns:name', default="N/A", namespaces=namespaces)
        pathway_drugs = pathway.findall('ns:drugs/ns:drug', namespaces=namespaces)
        pathway_drug_names = [pathway_drug.findtext('ns:name', default="N/A", namespaces=namespaces) for pathway_drug in
                              pathway_drugs]

        pathway_data.append({
            'name': pathway_name,
            'category': pathway.findtext('ns:category', default="N/A", namespaces=namespaces),
            'drugs_involved': pathway_drug_names
        })
        for pathway_drug in pathway_drugs:
            drug_name = pathway_drug.findtext('ns:name', default="N/A", namespaces=namespaces)
            interaction_data.append({
                'drug_name': drug_name,
                'pathway': pathway_name,
            })

df_pathways = pd.DataFrame(pathway_data)
df_interactions = pd.DataFrame(interaction_data)

print(df_pathways)
#print(df_interactions)

def draw_interaction_graph():
    G = nx.Graph()

    for _, row in df_interactions.iterrows():
        drug = row['drug_name']
        pathway = row['pathway']

        G.add_node(drug, bipartite=0)
        G.add_node(pathway, bipartite=1)

        G.add_edge(drug, pathway)

    pos = nx.bipartite_layout(G, nodes=[node for node, data in G.nodes(data=True) if data['bipartite'] == 0])

    node_colors = ['skyblue' if G.nodes[node].get('bipartite') == 0 else 'lightgreen' for node in G.nodes()]

    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight='bold',
            edge_color='gray')

    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    plt.title('Interakcje leków z szlakami sygnałowymi')
    plt.show()

draw_interaction_graph()
