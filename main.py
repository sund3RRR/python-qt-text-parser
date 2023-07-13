import sys, re
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from form.form import Ui_MainWindow
from form.add_dialog import Add_UI_Dialog
from form.del_dialog import Del_UI_Dialog


class Add_Dialog(QDialog):
    def __init__(self) -> None:
        super(Add_Dialog, self).__init__()
        self.ui = Add_UI_Dialog()
        self.ui.setupUi(self)

        self.ui.cancel_button.clicked.connect(self.close_dialog)

        
    def close_dialog(self):
        self.close()

# test commentary        
class Del_Dialog(QDialog):
    def __init__(self) -> None:
        super(Del_Dialog, self).__init__()
        self.ui = Del_UI_Dialog()
        self.ui.setupUi(self)

        self.ui.cancel_button.clicked.connect(self.close_dialog)

        
    def close_dialog(self):
        self.close()

# test 1 commentary        
class App(QMainWindow):
    def __init__(self) -> None:
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        self.open_action = QAction("Open", self)
        self.file_menu.addAction(self.open_action)
        self.open_action.triggered.connect(self.load_text)

        self.save_action = QAction("Save", self)
        self.file_menu.addAction(self.save_action)
        self.save_action.triggered.connect(self.save)

        self.ui.start_button.clicked.connect(self.parse_content)

        self.ui.sort_button_1.clicked.connect(lambda: self.sort_list(self.ui.text_1, self.ui.sort_combobox_1))
        self.ui.clear_button_1.clicked.connect(lambda: self.ui.text_1.clear())
        self.ui.sortbutton_2.clicked.connect(lambda: self.sort_list(self.ui.text_2, self.ui.sort_combobox_2))
        self.ui.clear_button_2.clicked.connect(lambda: self.ui.text_2.clear())

        self.ui.move_content_right_button.clicked.connect(lambda: self.move_item(self.ui.text_1, self.ui.text_2))
        self.ui.move_content_left_button.clicked.connect(lambda: self.move_item(self.ui.text_2, self.ui.text_1))
        self.ui.move_all_content_rught_button.clicked.connect(lambda: self.move_all_items(self.ui.text_1, self.ui.text_2))
        self.ui.move_all_content_left_button.clicked.connect(lambda: self.move_all_items(self.ui.text_2, self.ui.text_1))

        self.add_dialog = Add_Dialog()  
        self.ui.add_button.clicked.connect(self.add_dialog.exec)
        self.add_dialog.ui.add_button.clicked.connect(self.add_item_list)

        self.del_dialog = Del_Dialog()
        self.ui.remove_button.clicked.connect(self.del_dialog.exec)
        self.del_dialog.ui.del_button.clicked.connect(self.del_item_list)

        self.ui.search_button.clicked.connect(self.search)

        self.ui.reset_button.clicked.connect(self.reset)
        self.ui.exit_button.clicked.connect(self.close)

        
    def reset(self):
        self.ui.text_content.clear()
        self.ui.text_1.clear()
        self.ui.text_2.clear()
        self.ui.search_output.clear()
        self.ui.search_word_input.clear()
        self.ui.checkbox_1.setChecked(False)
        self.ui.checkbox_2.setChecked(False)
        self.ui.switcher_all.setChecked(False)
        self.ui.switcher_email.setChecked(False)
        self.ui.switcher_numbers.setChecked(False)


    def search(self):
        search_word = self.ui.search_word_input.text() 
        
        search_list = []
        if self.ui.checkbox_1.isChecked() and self.ui.checkbox_2.isChecked():
            for i in range (0, self.ui.text_1.count()):
                if search_word in self.ui.text_1.item(i).text():
                    search_list.append(self.ui.text_1.item(i).text())
            for i in range (0, self.ui.text_2.count()):
                if search_word in self.ui.text_2.item(i).text():
                    search_list.append(self.ui.text_2.item(i).text())
        elif self.ui.checkbox_1.isChecked():
            for i in range (0, self.ui.text_1.count()):
                if search_word in self.ui.text_1.item(i).text():
                    search_list.append(self.ui.text_1.item(i).text())
        elif self.ui.checkbox_2.isChecked():
            for i in range (0, self.ui.text_2.count()):
                if search_word in self.ui.text_2.item(i).text():
                    search_list.append(self.ui.text_2.item(i).text())

        self.ui.search_output.clear()
        for item in search_list:
            self.ui.search_output.addItem(item)
                

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "TXT(*.txt)")

        if filePath == "":
            return
        
        text = ""
        for i in range (0, self.ui.text_2.count()):
            text += ' ' + self.ui.text_2.item(i).text()

        with open(filePath, "w") as file:
            file.write(text)
                

    def add_item_list(self):
        text = self.add_dialog.ui.text_input.text()
        if text == "":
            return
        elif self.add_dialog.ui.chapter_switcher_1.isChecked():
            self.ui.text_1.addItem(text)
        elif self.add_dialog.ui.chapter_swither_2.isChecked():
            self.ui.text_2.addItem(text)
        
         
    def del_item_list(self):
        if self.del_dialog.ui.chapter_switcher_1.isChecked():
            index = self.ui.text_1.currentRow()
            if index != -1:
                self.ui.text_1.takeItem(index)
        elif self.add_dialog.ui.chapter_swither_2.isChecked():
            index = self.ui.text_2.currentRow()
            if index != -1:
                self.ui.text_2.takeItem(index)
        

    def parse_content(self):  
        new_splitted_text = ""  

        if self.ui.text_content.toPlainText() == "":
            return
        elif self.ui.switcher_all.isChecked():
            new_splitted_text = self.splitted_text
            pass
        elif self.ui.switcher_numbers.isChecked():
            new_splitted_text = [string for string in self.splitted_text if re.search(r"\d", string)]
            pass
        elif self.ui.switcher_email.isChecked():
            new_splitted_text = [string for string in self.splitted_text if re.search(r"\w+@\w+\.\w+", string)]
            pass
        
        self.ui.text_1.clear()
        self.ui.text_1.addItems(new_splitted_text)


    def load_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        with open(file_path, "r") as file:
            text = "".join(file.readlines()) 
            self.ui.text_content.setText(text)
            self.text = self.ui.text_content.toPlainText()
            self.splitted_text = re.split(r" |\t|\n", self.text)
            pass
        

    def sort_list(self, list_widget, sort_combobox):
        sort_type = sort_combobox.currentIndex()
        match sort_type:
            case 0:
                self.sunder_sort(list_widget, lambda item1, item2: len(item1) > len(item2))
            case 1:
                self.sunder_sort(list_widget, lambda item1, item2: len(item1) < len(item2))
            case 2:
                self.sunder_sort(list_widget, lambda item1, item2: item1 > item2)
            case 3:
                self.sunder_sort(list_widget, lambda item1, item2: item1 < item2)
    
            
    def sunder_sort(self, list_widget :QListWidget, func):
        for i in range(0, list_widget.count()):
            for j in range(0, list_widget.count() - 1):
                if func(list_widget.item(j).text(), list_widget.item(j + 1).text()):
                    backup = list_widget.item(j + 1).text()
                    list_widget.item(j + 1).setText(list_widget.item(j).text())
                    list_widget.item(j).setText(backup)

    
    def move_item(self, from_list, to_list):
        new_item = from_list.currentItem()

        if new_item:
            index = from_list.currentRow()
            to_list.addItem(new_item.text())
            from_list.takeItem(index)
        else: return

        
    def move_all_items(self, from_list :QListWidget, to_list :QListWidget):
        for i in range(0, from_list.count()):
            new_item = from_list.item(0)
            to_list.addItem(new_item.text())
            from_list.takeItem(0)


if __name__ == "__main__":    
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())
