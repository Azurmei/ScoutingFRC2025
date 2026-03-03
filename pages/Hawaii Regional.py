from gs_client.gsClient import sheet, append_data, check_duplicate
import gspread

# Name of the worksheet you want
worksheet_name = "HAWAII_MATCHES"

# List all existing worksheets
existing_titles = [ws.title for ws in sheet.worksheets()]
print("Available worksheets:", existing_titles)

# Try to open worksheet, create if it doesn't exist
try:
    worksheet = sheet.worksheet(worksheet_name)
except gspread.exceptions.WorksheetNotFound:
    worksheet = sheet.add_worksheet(title=worksheet_name, rows=100, cols=20)
    print(f"Created new worksheet: {worksheet_name}")