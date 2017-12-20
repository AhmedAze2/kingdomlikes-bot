from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from time import sleep
import itertools
import re, pickle

with open('config.json') as data_file:
    data = json.load(data_file)

browser = webdriver.Chrome(data['webdriver_filepath'])
#browser.set_window_position(1100,5)


class KingdomLikesBot:
    def __init__(self):
        self.FINNISHED = False
        self.main_window = browser.window_handles[0]
        self.popup = None

        self.wait = WebDriverWait(browser, 10)

    def collect_youtube_cookies(self):
        """This function collects cookies for later use in kingdomlikes"""
        pickle.dump(browser.get_cookies(), open('ytCookies.pkl', 'wb'))

    def collect_facebook_cookies(self):
        """This function collects cookies for later use in kingdomlikes"""
        pickle.dump(browser.get_cookies(), open('fbCookies.pkl', 'wb'))

    def collect_instagram_cookies(self):
        """This function collects cookies for later use in kingdomlikes"""
        pickle.dump(browser.get_cookies(), open('igCookies.pkl', 'wb'))

    def load_FB_cookies(self):
        """Loads cookies from .pkl file, this is needed so that we dont'
        have to retype the username and pwd in every popup. """

        cookies = pickle.load(open("fbLikesCookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        print('laoded cookies, refreshing page.')
        browser.refresh()

    def load_IG_cookies(self):
        """Loads cookies from .pkl file, this is needed so that we dont'
        have to retype the username and pwd in every popup. """

        cookies = pickle.load(open("igCookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        print('laoded cookies, refreshing page.')
        browser.refresh()

    def load_YT_cookies(self):
        """Loads cookies from .pkl file, this is needed so that we dont'
        have to retype the username and pwd in every popup. """

        cookies = pickle.load(open("ytCookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        print('loaded cookies, refreshing page.')
        browser.refresh()

    def login_KingdomLikes(self, email, pwd):
        """Searches the webpage for the 'email' and 'password' field, enters the email and pwd.
        and clicks 'login'      """
        # Locate username and password field
        username = self.wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password = browser.find_element_by_name('password')
        username.send_keys(email)
        password.send_keys(pwd)
        # Press the login button
        browser.find_element_by_css_selector('#formlogin > div:nth-child(1) > input.button.blue').click()

    def like_YT_video(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1

        try:
            # Like the video
            likeBut = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-video-primary-info-renderer > div > div > div > div > '
                                                                                       'ytd-menu-renderer > div > ytd-toggle-button-renderer > a')))
            likeBut.click()
            print('Liked the video')
            sleep(1.5) 

            # Close the popup
            browser.close()

            # Succesfully liked the page - setting failure to False
            failure = False

        except TimeoutException as e:
            print('--> The FB page in the popup was "broken" or the internet connection was not fast enough', e)

        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)              
            print('finally')                                        
            return failure

    def dislike_YT_video(self, n : int):
        """Finds and presses the dislike button and closes the popup window when done."""
        failure = n + 1

        try:
            # dislike the video
            likeBut = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-video-primary-info-renderer > div > div > div > div > ytd-menu-renderer > div > ytd-toggle-button-renderer:nth-child(2) > a')))
            likeBut.click()
            print('----> Disliked video')

            # Close the popup
            browser.close()

            # Succesfully liked the page - setting failure to False
            failure = False

        except TimeoutException as e:
            print('----> The FB page in the popup was "broken" or the internet connection was not fast enough', e)


        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)
            print('finally')
            return failure

    def like_IG_photo(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1

        try:
            # like the photo
            sleep(2)
            likeBut = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_eszkz _l9yih')))
            likeBut.click()
            print('----> liked the IG photo')

            # Close the popup
            browser.close()

            # Succesfully liked the photo - setting failure to False
            failure = False

        except TimeoutException as e:
            print('----> The IG photoo in the popup was "broken" or the internet connection was not fast enough', e)

        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)
            print('finally')

            return failure

    def like_IG_follow(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1

        try:
            # follow the person
            sleep(2)
            likeBut = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button._qv64e')))           #(By.CSS_SELECTOR, 'span > button._qv64e._gexxb._r9b8f._njrw0'))) _qv64e _t78yp _r9b8f _njrw0
            likeBut.click()
            print('----> followed the person')

            # Close the popup
            browser.close()

            # Succesfully liked the page - setting failure to False
            failure = False

        except TimeoutException as e:
            print('----> The IG page in the popup was "broken" or the internet connection was not fast enough', e)

        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)
            print('finally')
            return failure

    def like_FB_photo(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1

        try:
            # Close the popup first
            closeBut = self.wait.until(EC.element_To_be_clickable((By.CSS_SELECTOR, 'body > div > div > div > a')))
            closeBut.click()
            sleep(1)

            # Like the photo
            likeBut = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form > div > div > div > div > div > div > div > span > div > a')))
            likeBut.click()
            print('----> Liked the fb photo')

            # Close the popup
            browser.close()

            # Succesfully liked the page - setting failure to False
            failure = False

        except TimeoutException:
            print('--> The FB page in the popup was "broken" or the internet connection was not fast enough')

        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)
            print('finally')
            return failure

    def like_FB_page(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1
        print('Clicking on like button in FB popup.')
        try:
            sleep(1)
            likeBut = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.likeButton._4jy0._4jy4._517h._51sy._42ft')))
            likeBut.click()
            print('----> Liked the fb page')
            sleep(0.5)

            # Close the popup
            browser.close()

            # Succesfully liked the page - setting failure to False
            failure = False

        except TimeoutException:
            print('--> The FB page in the popup was "broken" or the internet connection was not fast enough.')
            print('Checking if it is possible to unlike the FB page')
            try:
                unLike = browser.find_element_by_css_selector('button.likeButton._4jy0._4jy4._517h._51sy._42ft')
                unLike.click()
            except:
                print('There was no \'unLike button\'')
        finally:
            # Switch control to the main_window
            browser.switch_to_window(self.main_window)
            print('finally')
            return failure

    def like_FB_picture(self):
        """Finds and presses the like button and closes the popup window when done."""
        print('Clicking on like button in FB popup.')
        likeBut = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div > div > div > div > div > div > span:nth-child(1) > div > a')))
        likeBut.click()
        print('----> SYNES GODT OM')

    def _get_allLikeButtons(self) -> list:
        """Locate all the (links to facebook pages) buttons that are ready."""
        PagesToLike = browser.find_elements_by_css_selector(
                      'div.pagecontent.normalheight.left.hide > div > div.containerbtn.remove > button')
        return PagesToLike

    def _get_allSkipButtons(self) -> list:
        """Locate all the skip buttons."""
        skipButtons = browser.find_elements_by_css_selector('div.pagecontent.normalheight.left.hide > div > div.containerbtn.remove > a')
        return skipButtons

    def switch_to_popup(self):
        """Waits for the popup to be presence, before switching focus to the popup."""
        print(browser.window_handles)
        while len(browser.window_handles) == 1:
            sleep(1)
            print(len(browser.window_handles), browser.window_handles)

        self.popup = browser.window_handles[1]
        browser.switch_to_window(self.popup)
        print('Succesfully switched to popup.')

    def get_list_of_like_buttons(self) -> list:
        """Return 'list_of_like_buttons' """
        # Wait for any button to appear
        try:
            list_of_like_buttons = WebDriverWait(browser, 60).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".button.blue")))
            return list_of_like_buttons
        except WebDriverException:
            print('There is not more points to be earned on this network. Error:', e)
            print('STOPPING HERE NOW')
            exit()

    def click_on_button(self, but_nr):
        """Keeps trying to click on the given 'but_nr' button, until it is succesful"""
        print('Starting to spam the button..')
        while True:
            # Keep trying to click on the button, until it's loaded and clickable
            try:
                self.list_of_like_buttons[but_nr].click()
                print('--> Succesfully clicked the button')
                return
            except WebDriverException as e:
                # The button is loading (blue loading screen over it) - not clickable
                print('- ERROR: element is loading - not clickable. Could be a result of the window being resized.')
                sleep(0.2)
                continue
            except TypeError:
                print("'NoneType' object is not subscriptable'\n - Unclear why this error is gotten\n")

    def change_network(self, n):
        """Change network to earn points on; Eg. change from FB page like to YT Dislikes. AND
        set everything up: click on the first button; switch to popup; load cookies; like it; close popup."""

        if n == 1:
            # Click on the network: Youtube likes
            but = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'YouTube Likes')))
            but.click()

            # Wait for any button to appear
            self.list_of_like_buttons = self.get_list_of_like_buttons()

            # Keep clicking on the button, until it is clickable (it reacts)
            self.click_on_button(but_nr=0)

            # Switch to the popup; load cookies; dislike it; close popup.
            self.switch_to_popup()
            self.load_YT_cookies()
            self.like_YT_video(n=0)

        elif n == 2:
            # Click on the network: Youtube dislikes
            but = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'YouTube disLikes')))
            but.click()

            # Wait for any button to appear
            self.list_of_like_buttons = self.get_list_of_like_buttons()

            # Keep clicking on the button, until it is clickable (it reacts)
            self.click_on_button(but_nr=0)

            # Switch to the popup; load cookies; dislike it; close popup.
            self.switch_to_popup()
            self.load_YT_cookies()
            self.dislike_YT_video(n=0)

        elif n == 3:
            # Click on the network: FB Page Like
            but = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Facebook Likes')))
            but.click()

            # Wait for any button to appear
            self.list_of_like_buttons = self.get_list_of_like_buttons()

            # Keep clicking on the button, until it is clickable (it reacts)
            self.click_on_button(but_nr=0)

            # Switch to the popup; load cookies; like it; close popup.
            self.switch_to_popup()
            self.load_FB_cookies()
            self.like_FB_page(n=0)

        elif n == 4:
            # Click on the network: Instagram Like
            but = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Instagram Likes')))
            but.click()

            # Wait for any button to appear
            self.list_of_like_buttons = self.get_list_of_like_buttons()

            # Keep clicking on the button, until it is clickable (it reacts)
            self.click_on_button(but_nr=0)

            # Switch to the popup; load cookies; like it; close popup.
            self.switch_to_popup()
            self.load_IG_cookies()
            self.like_IG_photo(n=0)

        elif n == 5:
            # Click on the network: Instagram follow
            but = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Instagram Followers')))
            but.click()

            # Wait for any button to appear
            self.list_of_like_buttons = self.get_list_of_like_buttons()

            # Keep clicking on the button, until it is clickable (it reacts)DK
            self.click_on_button(but_nr=0)

            # Switch to the popup; load cookies; follow the person; close popup.
            self.switch_to_popup()
            self.load_IG_cookies()
            self.like_IG_follow(n=0)




browser.get('http://kingdomlikes.com/free_points/facebook-likes')
bot_1 = KingdomLikesBot()
bot_1.login_KingdomLikes(email=data['email'], pwd=data['pwd'])

for network_nr in range(3, 6):
    assume_finnished = False # If two buttons in succession are taking too long to load -> change network
    bot_1.FINNISHED = False
    bot_1.change_network(n=network_nr)
    but_nr = 1

    while not bot_1.FINNISHED:
        try:
            print('BUTTON_NR ->', but_nr)
            list_of_like_buttons = WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".button.blue")))
            list_of_skip_buttons = WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, "[Skip]")))
            print('Found: like buttons: {}\tskip buttons: {}'.format(len(list_of_like_buttons), len(list_of_skip_buttons)))
        except TimeoutException as e:
            print('There is not more points to be earned on this network. Error:', e)
            bot_1.FINNISHED = True
            continue

        try:
            list_of_like_buttons[but_nr].click()
        except IndexError:
            # There isn't eg. a 5. button, set but_nr to click to -> 0
            print('- ERROR: IndexError!')
            but_nr = 0
            continue
        except WebDriverException as e:
            # The button is loading (blue loading screen over it) - not clickable
            print('- ERROR: element is loading - not clickable. Could be a result of the window being resized.\n', e)
            failed_clicks += 1
            if failed_clicks <= 30:
                # If failed to click on 'but_nr' button 30 times; give it time to load -> click on next button.
                but_nr += 1
                failed_clicks = 0
                # If the former button wasn't clickable either (assume_finnished==True)
                if assume_finnished:
                    # Change network
                    bot_1.FINNISHED = True
                    continue
                else:
                    # This will be set to False again, if the next button is succesfully pressed (we reach the button of this while loop)
                    assume_finnished = True

            continue

        failed_clicks = 0 # Counts the number of time a button has been clicked on while unclickable (blue loading screen)

        # Wait for the popup to appear and then switch to it
        bot_1.switch_to_popup()

        # Like/dislike/share depending on n (the network eg. 'FB page Likes' or 'YT disLikes') handle the situation accordingly. if not succesful -> failure = True
        if network_nr == 1:
            failure = bot_1.like_YT_video(n=but_nr)
        elif network_nr == 2:
            failure = bot_1.dislike_YT_video(n=but_nr)
        elif network_nr == 3:
            failure = bot_1.like_FB_page(n=but_nr)
        elif network_nr == 4:
            failure = bot_1.like_IG_photo(n=but_nr)
        elif network_nr == 5:
            failure = bot_1.like_IG_follow(n=but_nr)

        print(bool(failure), failure, failure - 1)
        if failure:
            # If failed to like the fb page; assume the popup is broken -> skip it
            sleep(5)
            try:
                list_of_skip_buttons[failure - 1].click()
                sleep(2)
            except WebDriverException as e:
                print('- ERROR: element is loading - not clickable\n', e)
                continue
        else:
            # Succesfully handled the popup; 'but_nr += 1' so handle the next but_nr popup
            but_nr += 1
            sleep(2)

        assume_finnished = False