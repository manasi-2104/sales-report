const SPREADSHEET_ID = "1R5G-5SJOTfWyy4YVI41GT788MIYM0CWhvZLAqXmFiS4";

function getTargetSheet_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  return ss.getSheets()[0];
}

function doGet() {
  return ContentService.createTextOutput("Sales Report API is running.");
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = getTargetSheet_();

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Timestamp","Date","Supervisor Name","Promoter Name/Mobile Number","D Mart Stores","Attendance","Shift"]);
    }

    sheet.appendRow([new Date(), data.date || "", data.supervisor || "", data.promoter || "", data.store || "", data.attendance || "", data.shift || ""]);

    return ContentService.createTextOutput(JSON.stringify({success:true})).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({success:false,error:String(err)})).setMimeType(ContentService.MimeType.JSON);
  }
}
