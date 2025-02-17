import xml.etree.ElementTree as ET
from collections import defaultdict

import pandas as pd

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

proteins_data = []
ctr = defaultdict(int)

tot_num = 0

for drug in root.findall('.//ns:drug', namespaces):
    drugbank_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    drug_name = drug.findtext('ns:name', default="N/A", namespaces=namespaces)
    targets = drug.findall('ns:targets/ns:target', namespaces)
    for target in targets:
        target_name = target.findtext('ns:name', default="N/A", namespaces=namespaces)
        polypeptide = target.find('ns:polypeptide', namespaces=namespaces)
        genatlas_id = "N/A"
        if polypeptide is not None:
            source = polypeptide.attrib.get('source', 'N/A')
            polypeptide_id = polypeptide.attrib.get('id', 'N/A')
            gene_name = polypeptide.findtext('ns:gene-name', default="N/A", namespaces=namespaces)
            Chromosome_number = polypeptide.findtext('ns:chromosome-location', default="N/A", namespaces=namespaces)
            placement_in_cell = polypeptide.findtext('ns:cellular-location', default="N/A", namespaces=namespaces)
        else:
            continue

        for ext_id in target.findall('.//ns:external-identifier', namespaces):
            resource = ext_id.find('ns:resource', namespaces).text
            if resource == "GenAtlas":
                genatlas_id = ext_id.find('ns:identifier', namespaces).text
                break
        target_id = target.findtext('ns:id', default="N/A", namespaces=namespaces)
        proteins_data.append({
            'target_id': target_id,
            'source': source,
            'source_name': polypeptide_id,
            'gene_name': gene_name,
            'GenAtlasID': genatlas_id,
            'Polipeptide_name': target_name,
            'Chromosome_number': Chromosome_number,
            'placement in cell': placement_in_cell,
            'drug_name': drug_name
        })
        ctr[target_id] += 1
        tot_num += 1
df_products = pd.DataFrame(proteins_data)
print(df_products)
print("# of targets: ",tot_num)