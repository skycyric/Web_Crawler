from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import re
import pandas
import requests
import time
import os
import traceback


class Downloader(QDialog):
    def __init__(self):
    QDialog.__init__(self)
    # 創建窗口
    self.resize(750, 300)
    layout = QGridLayout()
    self.infoTitle = QLabel('數據獲取設置')
    self.title = QLabel('輸入網頁URL')
    self.url = QPlainTextEdit()
    self.save_location = QLineEdit()
    self.DB_location = QLineEdit()
    self.templete_location = QLineEdit()
    self.progress = QProgressBar()
    download = QPushButton("一鍵統計")
    browse = QPushButton("選擇")
    DB_browse = QPushButton("選擇")
    templete_browse = QPushButton("選擇")
    self.save_location.setPlaceholderText("文件保存路徑")
    self.DB_location.setPlaceholderText("青年之聲用戶名信息存儲文本")
    self.templete_location.setPlaceholderText("Excel模板文件")
    self.progress.setValue(0)
    self.progress.setAlignment(Qt.AlignHCenter)
    num = 1
    layout.addWidget(self.infoTitle, num-1, 0, 1, 4)
    layout.addWidget(self.DB_location, num, 0, 1, 3)
    layout.addWidget(DB_browse, num, 3, 1, 1)
    layout.addWidget(self.templete_location, num+1, 0, 1, 3)
    layout.addWidget(templete_browse, num+1, 3, 1, 1)
    layout.addWidget(self.title, num+2, 0, 1, 4)
    layout.addWidget(self.url, num+3, 0, 1, 4)
    layout.addWidget(self.save_location, num+4, 0, 1, 3)
    layout.addWidget(browse, num+4, 3, 1, 1)
    layout.addWidget(self.progress, num+5, 0, 1, 4)
    layout.addWidget(download, num+6, 0, 1, 4)
    self.setLayout(layout)
    self.setWindowTitle("青年之聲統計神器 - 製作者：16級數字媒體技術2班梁偉添")
    self.DB_location.setText("data.txt")
    self.templete_location.setText("templete.xls")
    self.setFocus()
    download.clicked.connect(self.download)
    browse.clicked.connect(self.browse_file)
    DB_browse.clicked.connect(self.browse_DB)
    templete_browse.clicked.connect(self.browse_templete)
    def browse_file(self):
    save_file = QFileDialog.getSaveFileName(
        self, caption="保存文件到", directory=".", filter="Excel (*.xls)")
    self.save_location.setText(QDir.toNativeSeparators(save_file))
    def browse_DB(self):
    DB_file = QFileDialog.getOpenFileNames(
        self, caption="獲取青年之聲用戶名信息", directory=".", filter="txt (*.txt)")
    # 空數組處理
    if not DB_file:
    return
    self.DB_location.setText(QDir.toNativeSeparators(DB_file[0]))
    def browse_templete(self):
    templete_file = QFileDialog.getOpenFileNames(
        self, caption="獲取模板Excel文件", directory=".", filter="Excel (*.xls)")
    # 空數組處理
    if not templete_file:
    return
    self.templete_location.setText(QDir.toNativeSeparators(templete_file[0]))
    def download(self):
    url = self.url.toPlainText()
    save_location = self.save_location.text()
    DB_location = self.DB_location.text()
    templete_location = self.templete_location.text()
    print("開始寫入")
    if DB_location == "":
    QMessageBox.warning(self, "Warning", "用戶數據不能為空")
    return
    try:
    with open(DB_location, 'r') as f:
    info = f.read()
    except Exception:
    QMessageBox.warning(self, "Warning", "青年之聲用戶名信息獲取失敗\\n檢查文件路徑是否正確")
    return

    reg = r'(.*)'
    studentReg = re.compile(reg)
    self.studentName = re.findall(studentReg, info)
    # 清除空字符串
    self.studentName = [x for x in self.studentName if x != '']
    # 遍歷獲取 url 輸入框中的所有連結
    reg = r'(http.*)'
    urldReg = re.compile(reg)
    urlList = re.findall(urldReg, url)
    # 創建 excel 對象 和 excel 表
    if templete_location != "":
    try:
    rb = xlrd.open_workbook(templete_location, formatting_info=True)
    book = xlutils.copy.copy(rb)
    sheet = book.get_sheet(0)
    except Exception:
    QMessageBox.warning(self, "Warning", "Excel模板獲取失敗\\n檢查文件路徑是否正確")
    return

    else:
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('青年之聲統計', cell_overwrite_ok=True)

    # 設置字體樣式
    font0 = xlwt.Font()
    font0.name = '微軟雅黑'

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment = alignment
    try:
    az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    column = 4
    r = 0
    for name in self.studentName:
    userClass = name.split('\\t')[0]
    userNum = name.split('\\t')[1]
    userName = name.split('\\t')[2]
    sheet.write(r+2, 0, r+1, style0)
    sheet.write(r+2, 1, userClass, style0)
    sheet.write(r+2, 2, userNum, style0)
    sheet.write(r+2, 3, userName, style0)
    r += 1
    # 分離處理 url 連結
    for originUrl in urlList:

        # 獲取url
    reg = r'quId=(.*?)&'
    quIdReg = re.compile(reg)
    quId = re.findall(quIdReg, originUrl)[0]
    url = "https://api.12355.net/pc/service/getReplysByQuestionId?quId=%s&page=1&rows=500" % quId
    askUrl = "https://api.12355.net/pc/service/getQuesDetail?quId=%s" % quId

    try:
        # 獲取html頁面
    response = requests.get(url)
    html = response.text
    response = requests.get(askUrl)
    askHtml = response.text
    except Exception:
    traceback.print_exc()
    QMessageBox.warning(self, "Warning", "網絡連接失敗")
    return
    if html == "":
    break
    # 獲取提問時間
    reg = r'"askTime":"(.*?)"'
    askReg = re.compile(reg)
    askList = re.findall(askReg, askHtml)
    # 獲取用戶名
    reg = r'"creatorName":"(.*?)"'
    nameReg = re.compile(reg)
    nameList = re.findall(nameReg, html)
    # 獲取回覆信息
    reg = r'"replyContent":"(.*?)"'
    contentReg = re.compile(reg)
    contentList = re.findall(contentReg, html)
    # 獲取回復時間
    reg = r'"replyTime":"(.*?)"'
    timeReg = re.compile(reg)
    timeList = re.findall(timeReg, html)
    row = 0
    # 批量生成超連結
    sheet.write(1, column, xlwt.Formula('HYPERLINK("%s";"問題%s")' %
                (originUrl, column-3)), style0)
    for name in self.studentName:
    index = 0
    # 檢測回復是否符合條件
    for creatorName in nameList:
        # 檢測回復是否匹配 用戶名
    if name.split('\\t')[2] == creatorName:
        # 檢測是否是問題當天的時間進行回復
    if askList[0].split(' ')[0] == timeList[index].split(' ')[0]:
        # 去除標點 檢測回復是否超過5個字
    reg = r"(?u)\\w"
    textReg = re.compile(reg)
    textList = re.findall(textReg, contentList[index])
    if len(textList) >= 5:
    sheet.write(row+2, column, "合格", style0)
    break
    index += 1

    row += 1
    # 進度條加載
    percent = (column-3) * 100 / len(urlList)
    self.progress.setValue(int(percent))
    print(str(int(percent))+"%")
    # 縱向求和 判斷數組是否越界的情況
    if column < 26:
    sheet.write(row+2, column, xlwt.Formula("COUNTIF(%s3:%s%s,\"合格\")" %
                (az[column], az[column], row+2)), style0)
    else:
    letter = "%s%s" % (az[int(column/26-1)], az[column % 26])
    sheet.write(row+2, column, xlwt.Formula("COUNTIF(%s3:%s%s,\"合格\")" %
                (letter, letter, row+2)), style0)

    column += 1

    # 橫向求和
    r = 0
    column -= 1
    sheet.write(r+1, column+1, "合計", style0)
    # 判斷數組是否越界的情況
    if column < 26:
    for name in self.studentName:
    sheet.write(r+2, column+1, xlwt.Formula("COUNTIF(%s%s:%s%s,\"合格\")" %
                (az[4], r+3, az[column], r+3)), style0)
    r += 1
    sheet.write(r+2, column+1, xlwt.Formula("SUM(%s%s:%s%s)" %
                (az[4], r+3, az[column], r+3)), style0)
    else:
    letter = "%s%s" % (az[int(column/26-1)], az[column % 26])
    for name in self.studentName:
    sheet.write(r+2, column+1, xlwt.Formula("COUNTIF(%s%s:%s%s,\"合格\")" %
                (az[4], r+3, letter, r+3)), style0)
    r += 1
    sheet.write(r+2, column+1, xlwt.Formula("SUM(%s%s:%s%s)" %
                (az[4], r+3, letter, r+3)), style0)

    book.save(save_location)

    except Exception:
    traceback.print_exc()
    QMessageBox.warning(self, "Warning", "數據寫入失敗")
    return
    print("完成寫入")
    QMessageBox.information(self, "Information", "數據寫入完成")
    self.progress.setValue(0)

    # # 清空輸入
    # self.url.setText("")
    # self.save_location.setText("")
app = QApplication(sys.argv)
dl = Downloader()
dl.show()
app.exec_()
來源：https: // twgreatdaily.com/Rf_GLGwBmyVoG_1Z41fk.html
