from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Bot:
    """
    Метод __init__ инициирует драйвер браузера
    Метод login описывает авторизацию на сайте и переход до требуемой страницы
    Метод get_data описывает вход на страницу поиска, перебор списка вин номеров с очисткой поля input.
    Информация со страницы (ячеек таблицы) пишется во временные словари (структура -  вин номер : {Номер ТО : {'Сервис':PID-PID,'Заказ наряд':001, 'дата': 01-01-2019,'пробег':12345,'диллер':56000}})
    При каждой итерации, данные дописываются в файл info.txt
    """

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.login = 'pvenukidze'
        self.password = 'petr130485'


    def login_func(self):
        self.driver.get('http://ddms.kia.com/nxui/ddms/index.html')
        sleep(5)
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_userid_input").send_keys(self.login)     # Находим input по id и вставляем в него логин
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd").click()                            # Находим блок с паролем и кликаем по нему, т.к. input предварительно недоступен                                                                                            # Задержка
        sleep(2)
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd_input").send_keys(self.password)      # Находим input пароля, вводим в него пароль
        button = self.driver.find_element_by_id('mainframe_LOOGIN_form_Div00_btn_login')                         # Находим кнопку Login
        button.click()
        sleep(8)
        url_gwms =  self.driver.find_element_by_id('mainframe_VFrameSet_MiddleHFrameSet_WorkVFrameSet_MainHFrameSet_WorkFrameSet_HOME_form_div_siteLink_btn_gwmsImageElement')
        url_gwms.click()
        sleep(6)
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
        press_confirm = self.driver.find_element_by_id('btnMsgYes_000001')
        press_confirm.click()

    def get_data(self, vin_list):
        self.driver.get('http://gwms.kiacdn.com/jsp_html5/w400_basic_data/w400_0103/W400_0103.jsp')
        sleep(2)
        vin_dict = {}
        z=0
        print("Время начала: {}".format(str(datetime.datetime.now())))
        for vin in vin_list:
            persent = round(z/len(vin_list)*100,2)
            print("Выполнено: {}%".format(str(persent)), end='\r')
            i=0
            while i<18:
                self.driver.find_element_by_id('txtVIN').send_keys(Keys.BACK_SPACE)
                i+=1
            start = True
            while start:
                try:
                    self.driver.find_element_by_id('txtVIN').send_keys(vin)
                    search_btn = self.driver.find_element_by_id("btnInq")
                    search_btn.click()
                    service1 = self.driver.find_element_by_id('plsDataGrid_userCtrl_0_2_0')
                    hov = ActionChains(self.driver).move_to_element(service1)
                    hov.perform()
                    hov.click()
                    z_dic = {}
                    start = False
                except:
                    sleep(2)

            for i in range(10):
                start = True
                while start:
                    try:
                        inner_dic={}
                        if self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_2_0').get_attribute('value') == '' \
                        and self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_4_0').get_attribute('value') == '0':
                            continue
                        inner_dic['service'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_1_0').get_attribute('value')
                        inner_dic['order'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_2_0').get_attribute('value')
                        inner_dic['date'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_3_0').get_attribute('value')
                        inner_dic['odometr'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_4_0').get_attribute('value')
                        inner_dic['dealer'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_5_0').get_attribute('value')
                        if inner_dic['service']!='' and inner_dic['date']!='':
                            z_dic[i] = inner_dic
                        start=False
                    except:
                        sleep(3)
            vin_dict[vin] = z_dic
            with open('info.txt', 'a') as file:
                file.write(vin+': '+str(vin_dict[vin])+'\n')
            z+=1
        print("Время окончания: {}". format(str(datetime.datetime.now())))
        # for key, val in vin_dict.items():
        #     print(key, '  ', val)
        self.driver.quit()


def file_open():
    vin_list = []
    with open('vin.txt', 'r') as file:
        for line in file.readlines():
            if len(line)>2:
                vin_list.append(line.replace('\n',''))
    return vin_list


def main():
    res = file_open()
    b = Bot()                                                                                               # Инициализируем экземпляр класса
    b.login_func()
    b.get_data(res)


if __name__ == '__main__':                                                                                  # Точка входа
    main()
