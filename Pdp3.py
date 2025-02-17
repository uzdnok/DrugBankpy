import xml.etree.ElementTree as ET
import pandas as pd

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

data = []
product_data = []
for drug in root.findall('.//ns:drug', namespaces):
    drugbank_id = drug.findtext('ns:drugbank-id', default="N/A", namespaces=namespaces)
    product_entries = drug.findall('ns:products/ns:product', namespaces = namespaces)
    manufacturer = drug.findtext('ns:manufacturer', namespaces = namespaces)
    for product in product_entries:
        product_name = product.findtext('ns:name', default="N/A", namespaces=namespaces)
        product_data.append({
            'drugbank-id': drugbank_id,
            'product-name': product_name,
            'labeller':product.findtext('ns:labeller', default="N/A", namespaces=namespaces),
            'NDC-code':product.findtext('ns:ndc-product-code', default="N/A", namespaces=namespaces),
            'dosage-form':product.findtext('ns:dosage-form', default="N/A", namespaces=namespaces),
            'Application_route':product.findtext('ns:route', default="N/A", namespaces=namespaces),
            'strength':product.findtext('ns:strength', default="N/A", namespaces=namespaces),
            'registering_country':product.findtext('ns:country', default="N/A", namespaces=namespaces),
            'registering_agency':product.findtext('ns:source', default="N/A", namespaces=namespaces),

        })
df_products = pd.DataFrame(product_data)
print(df_products)

