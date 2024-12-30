import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

# Zdefiniowanie przestrzeni nazw
namespaces = {'ns': 'http://www.drugbank.ca'}

# Przechowywanie danych
data = []

i = 1
# Iteracja przez elementy `drug` z uwzględnieniem przestrzeni nazw
for drug in root.findall('.//ns:drug', namespaces):
    # Pobieranie danych z elementów XML
    drug_data = {
        'drugbank-id': drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces),
        'name': drug.findtext('ns:name', default="N/A", namespaces=namespaces),
        'type': drug.attrib.get('type', 'N/A'),
        'description': drug.findtext('ns:description', default="N/A", namespaces=namespaces).strip(),
        'state': drug.findtext('ns:state', default="N/A", namespaces=namespaces),
        'indication': drug.findtext('ns:indication', default="N/A", namespaces=namespaces),
        'mechanism-of-action': drug.findtext('ns:mechanism-of-action', default="N/A", namespaces=namespaces),
        'food_interactions': ' , '.join([group.text for group in drug.findall('.//ns:food-interaction', namespaces)]),
    }

    if drug_data['description'] != "N/A" or drug_data['state'] != "N/A":
        data.append(drug_data)
        #print(drug_data)
        i += 1
        if i > 15:
            break

# Tworzenie DataFrame
df = pd.DataFrame(data)
print(df)

