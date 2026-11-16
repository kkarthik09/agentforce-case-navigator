"""Build a Metadata API directory from root-level Apex files; no deployment."""
from pathlib import Path
import shutil,xml.etree.ElementTree as ET
root=Path(__file__).parent
dest=root/'metadata'; classes=dest/'classes'; classes.mkdir(parents=True,exist_ok=True)
ns='http://soap.sforce.com/2006/04/metadata'; ET.register_namespace('',ns)
package=ET.Element('{'+ns+'}Package'); types=ET.SubElement(package,'{'+ns+'}types')
for source in sorted(root.glob('*.cls')):
    shutil.copy2(source,classes/source.name)
    shutil.copy2(source.with_suffix('.cls-meta.xml'),classes/(source.name+'-meta.xml'))
    ET.SubElement(types,'{'+ns+'}members').text=source.stem
ET.SubElement(types,'{'+ns+'}name').text='ApexClass'
ET.SubElement(package,'{'+ns+'}version').text='65.0'
ET.ElementTree(package).write(dest/'package.xml',encoding='UTF-8',xml_declaration=True)
print(dest)
