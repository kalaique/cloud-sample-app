import requests
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

class Test_pyService(unittest.TestCase):
    PY_SERVICE_URL = "http://localhost:8000/health"
    FRONTEND_URL = "http://localhost:3001"
    COLOR_GREEN = "rgba(82, 196, 26, 1)"
    COLOR_RED = "rgba(255, 77, 79, 1)"

    def test_UI_color(self):
        # Check service status
        status = False
        try:
            response = requests.get(self.PY_SERVICE_URL)
        except requests.exceptions.RequestException as e:
            status = False
        else:
            print(response.status_code)
            if response.status_code == 200:
                message = response.json()
                print(message)
                for key, value in message.items():
                    if key == 'alive' and value == 'ok':
                        print(value)
                        status = True
                    else:
                        status= False
            else:
                status = False

        # Get color in UI
        #s = Service(r"C:\Users\User\Downloads\chromedriver.exe")
        #driver = webdriver.Chrome(service=s)
        driver = webdriver.Chrome('/home/runner/work/_actions/nanasess/setup-chromedriver/v1/lib/setup-chromedriver.sh')
        driver.implicitly_wait(20)
        driver.get(self.FRONTEND_URL)
        driver.maximize_window()
        time.sleep(20)
        element_pyservice = driver.find_element(By.XPATH, "//span[contains(text(), 'python service')]")
        color_pyservice = element_pyservice.value_of_css_property("color")
        if status:
            # Verify UI is GREEN
            self.assertEqual(self.COLOR_GREEN, color_pyservice, "Py service is not in GREEN color while service is UP")
        else:
            # Verify UI is RED
            self.assertEqual(self.COLOR_RED, color_pyservice, "Py service is not in RED color while service is DOWN")

        driver.close()

if __name__ == "__main__":
    unittest.main()
