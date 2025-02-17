import xml.etree.ElementTree as ET

import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

gene_data = []

for drug in root.findall('.//ns:drug', namespaces):
    targets = drug.findall('ns:targets/ns:target', namespaces)
    drug_name = drug.find('ns:name', namespaces).text
    for target in targets:
        target_name = target.findtext('ns:name', default="N/A", namespaces=namespaces)
        polypeptide = target.find('ns:polypeptide', namespaces=namespaces)
        if polypeptide is None:
            continue
        polypeptide_id = polypeptide.attrib.get('id', 'N/A')
        gene_name = polypeptide.findtext('ns:gene-name', default="N/A", namespaces=namespaces)
        product_entries = drug.findall('ns:products/ns:product', namespaces=namespaces)
        manufacturer = drug.findtext('ns:manufacturer', namespaces=namespaces)
        for product in product_entries:
            product_name = product.findtext('ns:name', default="N/A", namespaces=namespaces)
            gene_data.append({
                'gene_name': gene_name,
                'drug_name': drug_name,
                'product name': product_name,
                'labeller': product.findtext('ns:labeller', default="N/A", namespaces=namespaces),
                'NDC-code': product.findtext('ns:ndc-product-code', default="N/A", namespaces=namespaces),
                'dosage-form': product.findtext('ns:dosage-form', default="N/A", namespaces=namespaces),
                'Application_route': product.findtext('ns:route', default="N/A", namespaces=namespaces),
                'registering_country': product.findtext('ns:country', default="N/A", namespaces=namespaces),
                'registering_agency': product.findtext('ns:source', default="N/A", namespaces=namespaces),
            })

studied_gene = "F2"
df_gene = pd.DataFrame(gene_data)
selected_gene = df_gene[df_gene['gene_name'] == studied_gene]

plt.figure(figsize=(8, 8))
selected_gene['dosage-form'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title(f'Rozkład form podania produktów leczniczych dla genu {studied_gene}')
plt.ylabel('')
plt.show()

plt.figure(figsize=(8, 8))
selected_gene['registering_agency'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title(f'Rozkład agencji zatwierdzających leki związane z genem {studied_gene}')
plt.ylabel('')
plt.show()

