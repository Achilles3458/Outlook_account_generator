from bose.account_generator import AccountGenerator
from bose.ip_utils import find_ip_details
from bose import *
from contextlib import suppress
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .config import config

class OutlookSignUpTask(BaseTask):
    def get_task_config(self):
        accounts_created_len = len(Profile.get_profiles())
        is_min_3_accounts_created = accounts_created_len >= 100

        return TaskConfig(
            target_website='microsoft.com',
            prompt_to_close_browser= is_min_3_accounts_created,
            change_ip=is_min_3_accounts_created,
        )

    def get_browser_config(self, data):
        return BrowserConfig(
            profile=data['username'],
            is_tiny_profile=True,
            window_size=WindowSize.RANDOM,
            user_agent=UserAgent.REAL,
        )

    def get_data(self):
        country_code = find_ip_details()['country']
        accounts = AccountGenerator.generate_accounts(config['number_of_accounts_to_generate'], country=country_code)
        return accounts

    def run(self, driver: BoseDriver, account):
        first_name = account['first_name']
        last_name = account['last_name']
        # username = account['username']
        username = 'davidupwork' + str(284+len(Profile.get_profiles()))
        password = 'upworkguy123$'
        # password = account['password']
        dob_year = str(account['dob']['year'])
        dob_day = str(account['dob']['day'])
        dob_month = str(account['dob']['month'])
        account['email'] = username + '@outlook.com'
        email = account['email']
        ip_details = find_ip_details()
        country_name = ip_details['country_name']

        def press_next_btn():
                driver.get_element_by_id('iSignupAction', Wait.LONG).click()

        def sign_up():

            # Fill in the email and check if it's already taken
            while True: 
                try:
                    emailInput = driver.get_element_by_id('MemberName', Wait.SHORT)
                    emailInput.send_keys(email)
                    break
                except:
                    pass
            driver.long_random_sleep()
            press_next_btn()
            
            
            
            # with suppress(Exception):
            if driver.get_element_by_id('MemberNameError', Wait.SHORT) is not None:
                print(driver.get_element_by_id('MemberNameError', Wait.SHORT).text)
                print("Username is already taken. So this account was not craeated.")
                raise Exception()


            driver.short_random_sleep()
            # Fill in the password and proceed
            while True: 
                try:
                    passwordinput = driver.get_element_by_id('PasswordInput', Wait.SHORT)
                    passwordinput.send_keys(password)
                    break
                except:
                    pass

            driver.long_random_sleep()
            press_next_btn()


            driver.short_random_sleep()

            # Fill in the personal information
            while True: 
                try:
                    first = driver.get_element_by_id('FirstName', Wait.LONG)
                    first.send_keys(first_name)
                    break
                except:
                    pass
            driver.short_random_sleep()
            
            while True: 
                try:
                    last = driver.get_element_by_id('LastName', Wait.LONG)
                    last.send_keys(last_name)
                    break
                except:
                    pass

            driver.short_random_sleep()
            press_next_btn()

            driver.short_random_sleep()
            
            while True: 
                try:
                    birthMonth = driver.get_element_by_id('BirthMonth', Wait.LONG)
                    objectMonth = Select(birthMonth)
                    objectMonth.select_by_value(str(dob_month))
                    break
                except:
                    pass
            driver.short_random_sleep()


            # Fill in the date of birth
            while True: 
                try:
                    birthYear = driver.get_element_by_id('BirthYear', Wait.LONG)
                    birthYear.send_keys(str(dob_year))
                    break
                except:
                    pass

            driver.short_random_sleep()

            # Select the country from the dropdown
            while True: 
                try:
                    dropdown = driver.get_element_by_id('Country', Wait.LONG)
                    dropdown.find_element(By.XPATH, f"//option[. = '{country_name}']").click()
                    break
                except:
                    pass

            driver.short_random_sleep()


            while True: 
                try:
                    birthDay = driver.get_element_by_id('BirthDay', Wait.LONG)
                    objectDay = Select(birthDay)
                    objectDay.select_by_value(str(dob_day))
                    break
                except:
                    pass

            driver.short_random_sleep()
            press_next_btn()
            

            # Prompt to solve the CAPTCHA
            driver.prompt_to_solve_captcha(more_rules = [' - If you are using Residential IP AND Microsoft Captcha is too Tough. Solve via Audio Captcha.'])

            yes_button = driver.get_element_or_none_by_selector('[id="acceptButton"]', Wait.LONG)
            if yes_button is None:
                # Agree to Privacy Policy if it appears
                if driver.is_in_page('privacynotice.account.microsoft.com/notice', Wait.LONG):
                    continue_button = driver.get_element_or_none_by_selector('[id="id__0"]', Wait.LONG)
                    continue_button.click()
                yes_button = driver.get_element_or_none_by_selector('[id="acceptButton"]', Wait.LONG)

                if yes_button is None: 
                    if driver.is_in_page('privacynotice.account.microsoft.com/notice', Wait.LONG):
                        continue_button = driver.get_element_or_none_by_selector('[id="id__0"]', Wait.LONG)
                        continue_button.click()
                    yes_button = driver.get_element_or_none_by_selector('[id="acceptButton"]', Wait.LONG)


            # Click "Yes" button if it appears
            yes_button.click()

            # driver.get_by_current_page_referrer("https://outlook.live.com/mail/0/options/mail/rules", Wait.LONG)

            # op = 0

            # while True: 
            #     try:
            #         if (driver.current_url == "https://outlook.live.com/mail/0/options/mail/rules"):
            #             break
            #         driver.get_by_current_page_referrer("https://outlook.live.com/mail/0/options/mail/rules", Wait.LONG)
            #     except:
            #         op = 1
            #         driver.short_random_sleep()
            #         pass

            # while True: 
            #     try:
            #         add_button = driver.get_element_or_none_by_text_contains('Add new rule', Wait.LONG)
            #         add_button.click()
            #         name = driver.get_element_or_none('//input[@placeholder="Name your rule"]', Wait.LONG)
            #         name.send_keys('1111')
            #         con = driver.get_element_or_none('//div[@aria-label="Select a conditional"]', Wait.LONG)
            #         con.click()
            #         method = driver.get_element_or_none('//button[@data-index="32"]', Wait.LONG)
            #         method.click()
            #         action = driver.get_element_or_none('//div[@aria-label="Select a action"]', Wait.LONG)
            #         action.click()
            #         action_option = driver.get_element_or_none('//button[@data-index="11"]', Wait.LONG)
            #         action_option.click()
            #         mail = driver.get_element_or_none('//div[@aria-label="Select people for this condition"]', Wait.LONG)
            #         driver.short_random_sleep()
            #         mail.send_keys('maksym.uzwina2003@gmail.com')
            #         name.click()
            #         mail.click()
            #         driver.short_random_sleep()
            #         while True: 
            #             try:
            #                 mail_option = driver.get_element_or_none_by_text_contains('Use this address: maksym.uzwina2003@gmail.com', Wait.LONG)
            #                 driver.short_random_sleep()
            #                 mail_option.click()
            #                 break
            #             except:
            #                 pass
            #         driver.get_element_or_none_by_text_contains('Save', Wait.LONG).click()
            #         break
            #     except:
            #         pass


            # driver.short_random_sleep()


        def is_bot_detected():
            blocked_el = driver.get_element_or_none_by_text('The request is blocked.')
            return blocked_el is not None


        # Open the sign-up page via Google
        driver.organic_get("https://signup.live.com/")

                        
        if is_bot_detected():
            print('Bot is Blocked by Microsoft. Possibly because Microsoft has flagged the IP. You can try runnning the Bot after few minutes or you change your IP address to bypass the IP Ban.')
            driver.long_random_sleep()
            return
        
        sign_up()

        Profile.set_profile(account)
        driver.get_by_current_page_referrer('https://account.microsoft.com/')

        # Open the sign-up page via Google
        
        
        
        # Uncomment following line if you want to browse things after account is created. 
        # driver.prompt()
