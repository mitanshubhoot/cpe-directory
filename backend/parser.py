import xml.etree.ElementTree as ET
import sqlite3
import json

NAMESPACE = "http://cpe.mitre.org/dictionary/2.0"
NS = {"cpe-dict": NAMESPACE}

def parse_xml_and_store(xml_file):
    conn = sqlite3.connect("cpe.db")
    cursor = conn.cursor()

    tree = ET.parse(xml_file)
    root = tree.getroot()

    count = 0
    for item in root.findall(".//cpe-dict:cpe-item", NS):
        cpe_22_uri = item.attrib.get('name')
        cpe_22_deprecation_date = item.attrib.get('deprecation_date')  # ✅ fixed

        title_elem = item.find("cpe-dict:title", NS)
        title = title_elem.text if title_elem is not None else "N/A"

        # 2.3 Info (optional)
        cpe_23_tag = item.find("{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item")
        cpe_23_uri = cpe_23_tag.attrib.get("name") if cpe_23_tag is not None else None
        cpe_23_deprecation_date = None
        if cpe_23_tag is not None:
            dep = cpe_23_tag.find("{http://scap.nist.gov/schema/cpe-extension/2.3}deprecation")
            if dep is not None:
                cpe_23_deprecation_date = dep.attrib.get("date")

        # References
        refs = item.findall("cpe-dict:references/cpe-dict:reference", NS)
        ref_links = [ref.attrib.get("href") for ref in refs]
        ref_links_json = json.dumps(ref_links)

        print("Inserting:", title)
        cursor.execute(
            "INSERT INTO cpe (cpe_title, cpe_22_uri, cpe_23_uri, reference_links, cpe_22_deprecation_date, cpe_23_deprecation_date) VALUES (?, ?, ?, ?, ?, ?)",
            (title, cpe_22_uri, cpe_23_uri, ref_links_json, cpe_22_deprecation_date, cpe_23_deprecation_date)
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ Inserted {count} CPE entries into cpe.db")

if __name__ == "__main__":
    parse_xml_and_store("official-cpe-dictionary_v2.3.xml")
