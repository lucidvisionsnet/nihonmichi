"""
Consolidate multiple GPX files into a single file. `trk` and `rte` elements
from separate files are kept separate. GPX files are sorted based on filename,
ascending. GPX files are identified by a ".gpx" file extension. Output is
pretty-printed. Metadata from the first GPX file processed is used in the output
file. Assumes OsmAnd metadata is present and preserves it.
"""

import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pathlib import Path
from typing import List

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("gpx_dir", help="directory of GPX files to merge")
    p.add_argument("out_name", help="name of output GPX file")
    args = p.parse_args()

    gpx_dir = Path(args.gpx_dir).expanduser().resolve()
    output_path = Path(args.out_name).expanduser()

    assert gpx_dir.is_dir(), "a directory of GPX files is required"

    gpx_files = sorted(gpx_dir.glob("*.gpx"))
    assert gpx_files, "no .gpx files found in provided GPX directory"

    print(f"Base file: {gpx_files[0].name}")
    base_tree = ET.parse(gpx_files[0])
    base_root = base_tree.getroot()

    NS = "{http://www.topografix.com/GPX/1/1}"
    TRK_TAG = f"{NS}trk"
    RTE_TAG = f"{NS}rte"

    for gpx_file in gpx_files[1:]:
        print(f"Appending: '{gpx_file.name}'")
        tree = ET.parse(gpx_file)
        root = tree.getroot()

        trks = root.findall(f".//{TRK_TAG}")
        for trk in trks:
            base_root.append(trk)

        rtes = root.findall(f".//{RTE_TAG}")
        for rte in rtes:
            base_root.append(rte)

    raw_xml_bytes = ET.tostring(base_root, encoding="utf-8", xml_declaration=True)
    dom = xml.dom.minidom.parseString(raw_xml_bytes)
    pretty_xml = dom.toprettyxml(indent="  ")
    # Clean up extra blank lines that minidom adds.
    clean_xml = "\n".join(line for line in pretty_xml.splitlines() if line.strip())

    output_path = Path(output_path)
    output_path.write_text(clean_xml, encoding="utf-8")

if __name__ == "__main__":
    main()
