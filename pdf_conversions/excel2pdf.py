from spire.xls import *
from spire.xls.common import *

workbook = Workbook()

workbook.LoadFromFile("test_files\excel_test.xlsx")

workbook.ConverterSetting.SheetFitToPage = True

workbook.ConverterSetting.SheetFitToPageRetainPaperSize = True

for sheet in workbook.Worksheets: 

    pageSetup = sheet.PageSetup

    pageSetup.PaperSize = PaperSizeType.PaperA4

workbook.SaveToFile("output.pdf", FileFormat.PDF)

workbook.Dispose()