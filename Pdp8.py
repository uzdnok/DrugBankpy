import xml.etree.ElementTree as ET
from collections import defaultdict

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

placement_data = defaultdict(int)
i = 0
for drug in root.findall('.//ns:drug', namespaces=namespaces):
    targets = drug.findall('ns:targets/ns:target', namespaces=namespaces)
    for target in targets:
        target_name = target.findtext('ns:name', default="N/A", namespaces=namespaces)
        polypeptide = target.find('ns:polypeptide', namespaces=namespaces)
        if polypeptide is None:
            continue
        polypeptide_id = polypeptide.attrib.get('id', 'N/A')
        placement_in_cell = polypeptide.findtext('ns:cellular-location', default="N/A", namespaces=namespaces)
        placement_data[placement_in_cell] += 1

labels = placement_data.keys()
sizes = placement_data.values()

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=None, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)


plt.legend(labels, loc="upper left", bbox_to_anchor=(0.75, 1), fontsize=10)
plt.title('Występowanie targetów w częściach komórki')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.axis('equal')
plt.show()

print(i)