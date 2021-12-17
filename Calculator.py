import wx, math, threading as thread
from time import sleep

from wx.core import Centre

app = wx.App()
frm = wx.Frame(None, title="Ivy Calculator", size=(215,60))

label = wx.StaticText(frm, label="Form Over Function")
label_font: wx.Font = label.GetFont()
label_font.PointSize += 10
label.SetFont(label_font)

ID_ANS = 1337

def create_operator_menu():
  menu = wx.Menu()
  menu.AppendRadioItem(wx.ID_ANY, "Add")
  menu.AppendRadioItem(wx.ID_ANY, "Subtract")
  menu.AppendRadioItem(wx.ID_ANY, "Multiply")
  menu.AppendRadioItem(wx.ID_ANY, "Divide")
  return menu

def create_number_menu(menu: wx.Menu):
  menu.AppendSeparator()
  for i in range(11):
    menu.AppendRadioItem(wx.ID_ANY, str(i))
  return menu
  
class WxMenuBarCalculator():
  def __init__(self, frm):
    self.frm = frm
    self.number_menu_1 = create_number_menu(wx.Menu())
    self.number_menu_1_ans_btn: wx.MenuItem = self.number_menu_1.AppendRadioItem(ID_ANS, "ans")
    self.number__menu_1_no_after_0: wx.Menu = create_number_menu(wx.Menu())
    self.number_menu_1.AppendSubMenu(self.number__menu_1_no_after_0, "Number after 0")

    self.number_menu_2 = create_number_menu(wx.Menu())
    self.number_menu_2_ans_btn: wx.MenuItem = self.number_menu_2.AppendRadioItem(ID_ANS, "ans")
    self.number__menu_2_no_after_0: wx.Menu = create_number_menu(wx.Menu())
    self.number_menu_2.AppendSubMenu(self.number__menu_2_no_after_0, "Number after 0")

    self.operator_menu = create_operator_menu()
    self.result_menu = wx.Menu()
    self.calc_result: wx.MenuItem = self.result_menu.Append(wx.ID_ANY, "Calculate result")
    self.result_label: wx.MenuItem = self.result_menu.Append(wx.ID_ANY, "Answer: ", kind=wx.ITEM_NORMAL)
    self.result_label.Enable(False)

    self.menubar = wx.MenuBar()
    self.menubar.Append(self.number_menu_1, "Number 1")
    self.menubar.Append(self.operator_menu, "Operator")
    self.menubar.Append(self.number_menu_2, "Number 2")
    self.menubar.Append(self.result_menu, "Result")
    
    self.operator_menu.Bind(wx.EVT_MENU, self.on_operator_select)
    self.number_menu_1.Bind(wx.EVT_MENU, self.on_number_1_select)
    self.number_menu_2.Bind(wx.EVT_MENU, self.on_number_2_select)
    self.result_menu.Bind(wx.EVT_MENU, self.on_calculate_result)
    self.frm.SetMenuBar(self.menubar)
    self.selected_operator = "+"
    self.number_1 = "0"
    self.number_2 = "0"
    self.ans = "0"
    def update_ans_thread():
      while True:
        self.number_menu_1_ans_btn.SetItemLabel(f"ans ({self.ans})")
        self.number_menu_2_ans_btn.SetItemLabel(f"ans ({self.ans})")
        sleep(0.1)
    thread.Thread(target=update_ans_thread).start()
  @property
  def answer(self):
    try:
      ans = eval(f"{self.number_1} {self.selected_operator} {self.number_2}") 
    except:
      ans = math.nan
    finally:
      self.ans = str(ans)
      return ans
  def on_operator_select(self, event: wx.MenuEvent):
    self.selected_operator = ""
    for menu_item  in self.operator_menu.GetMenuItems():
      if menu_item.IsChecked():
        self.selected_operator = menu_item.GetItemLabel()
        break
    if self.selected_operator == "Add":
      self.selected_operator = "+"
    elif self.selected_operator == "Subtract":
      self.selected_operator = "-"
    elif self.selected_operator == "Multiply":
      self.selected_operator = "*"
    elif self.selected_operator == "Divide":
      self.selected_operator = "/"
  def on_number_1_select(self, event: wx.MenuEvent):
    sel_menu = ""
    for menu_item in self.number_menu_1.GetMenuItems():
      if menu_item.IsChecked():
        if menu_item.GetId() == ID_ANS:
          sel_menu = self.ans
        else:
          sel_menu = str(menu_item.GetItemLabel())
        break
    no_after_0 = 0
    for menu_item in self.number__menu_1_no_after_0.GetMenuItems():
      if menu_item.IsChecked():
        no_after_0 = int(menu_item.GetItemLabel())
        break

    self.number_1 = sel_menu + (no_after_0 * "0")
  def on_number_2_select(self, event: wx.MenuEvent):
    selected_number = ""

    for menu_item in self.number_menu_2.GetMenuItems():
      if menu_item.IsChecked():
        if menu_item.GetId() == ID_ANS:
          selected_number = self.ans
        else:
          selected_number = str(menu_item.GetItemLabel())
        break
    no_after_0 = 0
    for menu_item in self.number__menu_2_no_after_0.GetMenuItems():
      if menu_item.IsChecked():
        no_after_0 = int(menu_item.GetItemLabel())
        break

    self.number_2 = selected_number + (no_after_0 * "0")
    print(self.number_2, self.number_1, self.selected_operator)
  def on_calculate_result(self, event: wx.MenuEvent):
    answer_text = f"Answer: {self.answer}"
    self.result_label.SetItemLabel(answer_text)
    
johnnyIve_calculator = WxMenuBarCalculator(frm)
frm.Show()
app.MainLoop()