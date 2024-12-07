from spire.doc import *
from spire.doc.common import *


document = Document()
document.LoadFromFile("test_files/test2.docx")
document.SaveToFile("WordToPdf.pdf", FileFormat.PDF)
document.Close()