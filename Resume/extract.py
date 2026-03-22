import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.XML(xml_content)
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        TEXT = WORD_NAMESPACE + 't'
        return '\n'.join([node.text for node in tree.iter(TEXT) if node.text])
    except Exception as e:
        return f"Error reading {path}: {str(e)}"

print("=== RESUME CONTENT ===")
print(get_docx_text('Cyber Security Resume.docx'))
print("\n=== COVER LETTER CONTENT ===")
print(get_docx_text('Cover Letter.docx'))
