from selenium import webdriver
from time import sleep

class Bot:

    def __init__(self, vin):
        self.driver = webdriver.Firefox()
        self.login(vin)

    def login(self, vin):
        self.driver.get('http://ddms.kia.com/nxui/ddms/index.html')                                         # Открываем страницу
        sleep(5)                                                                                            # Дожидаемся загрузки страницы
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_userid_input").send_keys("Admin")   # Находим input по id и вставляем в него логин
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd").click()                       # Находим блок с паролем и кликаем по нему, т.к. input предварительно недоступен
        sleep(2)                                                                                            # Задержка
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd_input").send_keys("Admin")      # Находим input пароля, вводим в него пароль
        button = self.driver.find_element_by_id('mainframe_LOOGIN_form_Div00_btn_login')                    # Находим кнопку Login
        button.click()                                                                                      # Кликаем по кнопке Login
        #result = self.search_vin(vin)

        sleep(4)
        self.driver.close()

    def search_vin(self):
        self.driver.find_element_by_id("txtVIN").send_keys(vin)
        search_button = self.driver.find_element_by_id("lblInq")
        search_button.click()


        return result

def main(vin):
    b = Bot(vin)                                                                                               # Инициализируем экземпляр класса


if __name__ == '__main__':                                                                                  # Точка входа
    main('LK9OR49ML2IJ339')
