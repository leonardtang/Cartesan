"""
Script to interact with (i.e. monitor) OpenAI's ChatGPT web interface.
"""

import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome


class ChatGPTBot:
    def __init__(self):
        self.driver = Chrome()
        self.driver.get("https://chat.openai.com/")
        self.cookies_path = "cookies.pkl"
        time.sleep(2)
        # Eventually have nice first-time cookie setup, like here: https://stackoverflow.com/questions/45417335/python-use-cookie-to-login-with-selenium
        try:
            cookies = pickle.load(open(self.cookies_path, "rb"))
        except:
            # First-time cookie setup. Login to ChatGPT then go to terminal to proceed
            input("Once cookies are saved, press enter...")
            cookies = self.driver.get_cookies()
            pickle.dump(cookies, open(self.cookies_path, "wb"))

        for cookie in cookies:
            try: 
                self.driver.add_cookie(cookie)
            except: 
                print("Warning: failed to set cookie", cookie)
                continue

    def enter_gpt4(self):
        """
        Enter GPT-4 and 
        """
        self.goto_link("https://chat.openai.com/?model=gpt-4")
        self.click_button([
            '//*[@id="radix-:rk:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rm:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rt:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rq:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rl:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rn:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:ro:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rp:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rr:"]/div[2]/div/div[4]/button',
            '//*[@id="radix-:rs:"]/div[2]/div/div[4]/button'
        ])
        # self.click_button('//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/div/span/button')

    def goto_link(self, link):
        """
        Go to a link
        """
        self.driver.get(link)
        time.sleep(2)

    def click_button(self, xpaths):
        """
        Find and click a button
        """
        button = None
        button = None
        while True:
            next = xpaths.pop(0)
            try:
                button = self.driver.find_element(By.XPATH, next)
                break
            except:
                print("Button not found: ", next)
                xpaths.append(next)
                time.sleep(1)
        
        if button is None:
            print("Button not found")
            while True:
                pass
        print("Found button", next)
        
        button.click()
        time.sleep(2)


    def send_response(self, text, image_path):
        # Again, sometimes the XPath changes
        while True:
            try:
                input_text_area = self.driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
            except:
                print("text area not found")
                time.sleep(1)
                continue
            break
        input_text_area.send_keys(text)
        time.sleep(1)

        found = False
        while not found:
            image_xpaths = [
                '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/div/button',
                '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/div/span/button'
            ]
            for image_xpath in image_xpaths:
                try:
                    print("Image trying", image_xpath)
                    image_area = self.driver.find_element(By.XPATH, image_xpath)
                    found = True
                    break
                except:
                    print("image area not found")
                    time.sleep(1)
                    continue
            
        if image_area is None:
            print("Image area not found")
            while True:
                pass
        
        print("Found", image_area)
        image_area.send_keys(image_path)
        # image_area.click()
        print("Keys sent")


        # time.sleep(1)
        send_message = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button')
        send_message.click()

    def get_response(self):
        # Wait for the regenerate button to appear
        regenerate_button = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[1]/div/div[2]/div/button/div'
        rg = WebDriverWait(self.driver, 20, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, regenerate_button)))
        print(f"RG found: {rg}")
        # WebDriverWait(self.driver, 60, poll_frequency=0.1).until(EC.text_to_be_present_in_element((By.XPATH, regenerate_button), "Regenerate"))
        time.sleep(10)
        print("Regenerate button found")

        response_list_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/ol'
        list_size  = self.driver.find_elements_by_xpath(f"{response_list_xpath}/li")
        for i in range(list_size):
            print(f"{response_list_xpath}/li/{i}")
        # response_area = WebDriverWait(self.driver, 5).until(
        #     EC.presence_of_element_located((By.XPATH, response_list_xpath))
        # )
        # print(f"Response area found {response_area}")
        # return response_area.text
    
    def query(self, text, image_path):
        self.send_response(text, image_path)
        return self.get_response()
    

if __name__ == "__main__":
    # Sometimes the popup XPaths change, so just retry until the right XPaths appear
    while True:
        try:
            print("Attempting to initialize...")
            bot = ChatGPTBot()
            bot.enter_gpt4()
        except:
            print("Error during popup clickthrough")
            raise
            time.sleep(2)
            continue
        break
        
    query_text = "Please list all the items in my fridge. If you cannot, give me any list."
    image_path = "/Users/leonmaksin/Documents/Cartesan/images/food.jpeg"
    print(f"Querying with text {query_text} and image {image_path}")
    response = bot.query(query_text, image_path)
    print("ChatGPT Response:")
    print(f"{response}\n")

    while True:
        pass