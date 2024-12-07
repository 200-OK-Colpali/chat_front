from spire.presentation import *
from spire.presentation.common import *


presentation = Presentation()
presentation.LoadFromFile("test_files\pres.pptx")

presentation.SaveToFile("PresentationToPDF.pdf", FileFormat.PDF)
presentation.Dispose()
