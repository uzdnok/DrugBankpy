import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()

namespaces = {'ns': 'http://www.drugbank.ca'}

still_approved = 0
num_was_approved = 0
num_was_withdrawn = 0
num_vet_approved = 0
num_is_experimental = 0
approval_data = []

status_data = {
    'approved': 0,
    'withdrawn': 0,
    'experimental': 0,
    'veterinary': 0
}

for drug in root.findall('.//ns:drug', namespaces):
    groups = drug.findall('ns:groups/ns:group', namespaces)
    was_approved = False
    was_withdrawn = False
    for group in groups:
        group_name = group.text
        if group_name == 'approved':
            was_approved = True
            num_was_approved += 1
        if group_name == 'withdrawn':
            was_withdrawn = True
            num_was_withdrawn += 1
        if group_name == 'vet_approved':
            num_vet_approved += 1
        if group_name == 'experimental' or group_name == 'investigational':
            num_is_experimental += 1
    if was_approved and not was_withdrawn:
        still_approved += 1

status_data['approved'] = num_was_approved
status_data['withdrawn'] = num_was_withdrawn
status_data['experimental'] = num_is_experimental
status_data['veterinary'] = num_vet_approved

df = pd.DataFrame(list(status_data.items()), columns=['Status', 'Count'])

plt.figure(figsize=(8, 8))
plt.pie(df['Count'], labels=df['Status'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99','#ffcc99','#ff6666'])
plt.title('Rozkład leków w różnych kategoriach')
plt.axis('equal')
plt.show()

print(df)
print("# of approved and not withdrawn drugs: ", still_approved)