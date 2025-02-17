import xml.etree.ElementTree as ET
import pandas as pd

def solvePDP4(pathname):

    pd.set_option('display.max_columns', None)

    tree = ET.parse(pathname)
    root = tree.getroot()

    namespaces = {'ns': 'http://www.drugbank.ca'}

    pathway_data = []
    for drug in root.findall('.//ns:drug', namespaces):
        pathways = drug.findall('ns:pathways/ns:pathway', namespaces = namespaces)
        for pathway in pathways:
            pathway_name = pathway.findtext('ns:name', default="N/A", namespaces=namespaces)
            pathway_data.append({
                'name': pathway_name,
                'category': pathway.findtext('ns:category', default="N/A", namespaces=namespaces),
                'smpdb-id' : pathway.findtext('ns:smpdb-id', default="N/A", namespaces=namespaces),
            })
    df_products = pd.DataFrame(pathway_data)
    print(df_products)
    print("Num of pathways: ", len(pathway_data))
    return df_products, len(pathway_data)

solvePDP4("drugbank_partial.xml")