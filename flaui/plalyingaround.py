import PIL.ImageGrab
from loguru import logger
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()

from flaui.robot.keywords.combobox import ComboBoxKeywords
from flaui.robot.keywords.application import ApplicationKeywords
from flaui.robot.automation.uia3 import UIA3
from flaui.robot.keywords.element import ElementKeywords

uia = UIA3()
app_keywords = ApplicationKeywords(uia)
element_keywords = ElementKeywords(uia)
combo_keywords = ComboBoxKeywords(uia)

if __name__ == '__main__':
    app_keywords.attach_application_by_name('WpfApplication.exe')
    logger.debug(element_keywords.get_name_from_element('/Window/Tab/TabItem[1]/ComboBox[1]'))
    s = combo_keywords.select_combobox_item_by_index('/Window/Tab/TabItem[1]/ComboBox[1]',2)
    print('s')