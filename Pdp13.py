import random
import xml.etree.ElementTree as ET

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
namespaces = {'ns': 'http://www.drugbank.ca'}

new_drugs = []

real_drugs = []


def remove_namespace(element):
    tag = element.tag.split('}', 1)[-1]
    new_elem = ET.Element(tag)
    new_elem.attrib = {(k.split('}', 1)[-1] if '}' in k else k): v for k, v in element.attrib.items()}
    if element.text and element.text.strip():
        new_elem.text = element.text.strip()
    for child in element:
        new_child = remove_namespace(child)
        new_elem.append(new_child)
    return new_elem


for drug in root.findall('.//ns:drug', namespaces):
    drug_copy = remove_namespace(drug)
    real_drugs.append(drug_copy)
    new_drugs.append(drug_copy)


def copy_element(element, parent):
    tag_name = element.tag.split('}')[1] if '}' in element.tag else element.tag
    new_element = ET.SubElement(parent, tag_name)

    if element.text:
        new_element.text = element.text.strip()

    for sub_element in element:
        copy_element(sub_element, new_element)


for i in range(199):

    new_drug = ET.Element('drug',
                          {'type': 'biotech', 'created': '2025-02-15', 'updated': '2025-02-15'})

    drugbank_id = ET.SubElement(new_drug, 'drugbank-id', {'primary': 'true'})
    drugbank_id.text = f"DB{10001 + i}"

    existing_drug = random.choice(real_drugs)
    new_name = ET.SubElement(new_drug, 'name')
    drug_name = existing_drug.findtext('ns:name', default="New_drug", namespaces=namespaces)
    new_name.text = drug_name + str(i)

    for element in existing_drug:
        copy_element(element, new_drug)
    new_drugs.append(new_drug)

new_root = ET.Element("drugbank", {
    "xsi:schemaLocation": "http://www.drugbank.ca http://www.drugbank.ca/docs/drugbank.xsd",
    "version": "5.1",
    "exported-on": "2024-03-14",
    "xmlns": "http://www.drugbank.ca",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
})
new_root.extend(new_drugs)

new_tree = ET.ElementTree(new_root)
new_tree.write("drugbank_partial_and_generated.xml", encoding='utf-8', xml_declaration=True)
