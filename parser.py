from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class Bot:

    def __init__(self, vin_list):
        self.driver = webdriver.Firefox()
        self.login(vin_list)
        #self.get_data()

    def login(self, vin_list):

        self.driver.get('http://ddms.kia.com/nxui/ddms/index.html')
        sleep(5)
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_userid_input").send_keys("pvenukidze")   # Находим input по id и вставляем в него логин
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd").click()                       # Находим блок с паролем и кликаем по нему, т.к. input предварительно недоступен
        # sleep(2)                                                                                            # Задержка
        self.driver.find_element_by_id("mainframe_LOOGIN_form_Div00_edt_pwd_input").send_keys("petr130485")      # Находим input пароля, вводим в него пароль
        button = self.driver.find_element_by_id('mainframe_LOOGIN_form_Div00_btn_login')                    # Находим кнопку Login
        button.click()                                                                                      # Кликаем по кнопке Login
        sleep(8)
        url_gwms =  self.driver.find_element_by_id('mainframe_VFrameSet_MiddleHFrameSet_WorkVFrameSet_MainHFrameSet_WorkFrameSet_HOME_form_div_siteLink_btn_gwmsImageElement')
        url_gwms.click()
        sleep(8)
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
        press_confirm = self.driver.find_element_by_id('btnMsgYes_000001')
        press_confirm.click()
        self.driver.get('http://gwms.kiacdn.com/jsp_html5/w400_basic_data/w400_0103/W400_0103.jsp')
        sleep(5)
        #vin_list = ['XWEPC813DB0000246','XWEPH81ADH0011955','Z94CB41BAHR446738','Z94CB41BAHR439798','XWEFX411BHC004238','XWEPH81AAH0000459']
        vin_dict = {}
        for vin in vin_list:
            i=0
            while i<18:
                self.driver.find_element_by_id('txtVIN').send_keys(Keys.BACK_SPACE)
                i+=1
            self.driver.find_element_by_id('txtVIN').send_keys(vin)
            search_btn = self.driver.find_element_by_id("btnInq")
            search_btn.click()
            sleep(4)
            service1 = self.driver.find_element_by_id('plsDataGrid_userCtrl_0_2_0')
            hov = ActionChains(self.driver).move_to_element(service1)
            hov.perform()
            hov.click()
            z_dic = {}
            for i in range(10):
                inner_dic={}
                if self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_2_0').get_attribute('value') == '' and self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_4_0').get_attribute('value') == '0':
                    continue
                inner_dic['service'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_2_0').get_attribute('value')
                inner_dic['date'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_3_0').get_attribute('value')
                inner_dic['odometr'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_4_0').get_attribute('value')
                inner_dic['dealer'] = self.driver.find_element_by_id('plsDataGrid_userCtrl_'+str(i)+'_5_0').get_attribute('value')
                if inner_dic['service']!='' and inner_dic['date']!='':
                    z_dic[i] = inner_dic
            vin_dict[vin] = z_dic
            with open('info.txt', 'a') as file:
                file.write(vin+': '+str(vin_dict[vin])+'\n')
            sleep(1)
        for key, val in vin_dict.items():
            print(key, '  ', val)
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
    b = Bot(res)                                                                                               # Инициализируем экземпляр класса

if __name__ == '__main__':                                                                                  # Точка входа
    main()
