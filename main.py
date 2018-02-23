from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from time import sleep
import itertools, re, pickle, json

with open('config.json') as data_file:
    data = json.load(data_file)

browser = webdriver.Chrome(data['webdriver_filepath'])
#browser.set_window_position(1100,5)

# Cookie filenames:
# ytCookies.pkl
# fbCookies.pkl
# igCookies.pkl

class KingdomLikesBot:
    def __init__(self):
        self.FINNISHED = False
        self.main_window = browser.window_handles[0]
        self.popup = None

        self.wait = WebDriverWait(browser, 10)
        
    def collect_cookies(self, filename):
        """This function collects cookies for later use."""
        with open(filename, 'wb') as file:
            pickle.dump(browser.get_cookies(), file)
            print('INFO: Cookies collected')
            
    def load_cookies(self, filename):
        """Loads cookies from .pkl file, this is needed so that we dont'
        have to retype the username and pwd in every popup. """
        cookies = pickle.load(open(filename, 'rb'))
        for c in cookies:
            browser.add_cookie(c)
            print('INFO: Loaded cookies')
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
        selector = '#formlogin > div:nth-child(1) > input.button.blue'
        browser.find_element_by_css_selector(selector).click()

    def like_YT_video(self, n : int):
        """Finds and presses the like button and closes the popup window when done."""
        failure = n + 1
        try:
            # Like the video
            selector = ('ytd-video-primary-info-renderer > div > div > div > div >' 
                        'ytd-menu-renderer > div > ytd-toggle-button-renderer > a')
            likeBut = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
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
            sleep(2)
            # Close the popup asking you to download the IG app; it makes the like button unclickable.
            popup = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span._lilm5')))

            # like the photo
            likeBut = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a._eszkz._l9yih')))
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

    def switch_to_popup(self, max_retries=10):
        """Waits for the popup to be presence, before switching focus to the popup."""
        # Wait for the popup to be selectable
        while len(browser.window_handles) == 1:
            print(len(browser.window_handles), browser.window_handles)
            sleep(1)
            if max_retries == 0:
                return
            else:
                max_retries -= 1
        print('Popup located')
        # Switch focus to the popup window
        self.popup = browser.window_handles[1]
        browser.switch_to_window(self.popup)
        print('Succesfully switched to popup.')
        return 'succes'

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
            return

    def click_on_button(self, button, max_retries=40):
        """Keeps trying to click on the given 'but_nr' button, until it is succesful"""
        print('Starting to spam the button..')
        while max_retries:
            # Keep trying to click on the button, until it's loaded and clickable
            try:
                button.click()
                print('--> Succesfully clicked the button')
                return
            except WebDriverException as e:
                # The button is loading (blue loading screen over it) - not clickable
                print('- ERROR: element is loading - not clickable. Could be a result of the window being resized.')
                sleep(0.2)
                continue
            except TypeError:
                print("'NoneType' object is not subscriptable'\n - Unclear why this error is gotten\n")
            finally:
                max_retries -= 1

    def prepare_network(self, network_name, cookies_filename, action_func):
        """Runs one ad in order to prepare for future ads on the specific network.
        Example:
        	click on the like button; switch to popup; load cookies; like it; close popup.
        """
        print(network_name, type(network_name))
        # Click on the new network (eg. Youtube likes)
        but = self.wait.until(EC.presence_of_element_located(
            (By.LINK_TEXT, network_name)
        ))
        but.click()
        print(f'Succesfully clicked on the network: {network_name}')

        # Wait for any button to appear
        self.list_of_like_buttons = self.get_list_of_like_buttons()

        # If there was not found any buttons (ads)
        if not self.list_of_like_buttons:
            return self.change_network(n + 1)

        # Keep clicking on the ad button until it is clickable (it reacts)
        self.click_on_button(button=self.list_of_like_buttons[0])

        # Switch to the popup; load cookies; like/follow/dislike (do the action on it); close popup.
        if self.switch_to_popup():
            self.load_cookies(filename=cookies_filename)
            action_func(n=0)
        else:
            # If failed to switch to popup, re-run the entire function
            return self.prepare_network(network_name, cookies_filename, action_func)

    def change_network(self, n):
        """This changes the network and prepares the network.
        Example:
        	Change network eg. change from FB page like to YT Dislikes.
        	run -> prepare_network function
        """

        if n == 1:
            var1 = 'YouTube Likes'
            var2 = 'ytCookies.pkl'
            var3 = self.like_YT_video
            print(f'Changing network to {var1}')
        elif n == 2:
            var1 = 'YouTube disLikes'
            var2 = 'ytCookies.pkl'
            var3 = self.dislike_YT_video
            print(f'Changing network to {var1}')
        elif n == 3:
            var1 = 'Facebook Likes'
            var2 = 'fbCookies.pkl'
            var3 = self.like_FB_page
            print(f'Changing network to {var1}')
        elif n == 4:
            var1 = 'Instagram Likes'
            var2 = 'igCookies.pkl'
            var3 = self.like_IG_photo
            print(f'Changing network to {var1}')
        elif n == 5:
            var1 = 'Instagram Followers'
            var2 = 'igCookies.pkl'
            var3 = self.like_IG_follow
            print(f'Changing network to {var1}')
        elif n >= 6:
            quit()

        self.prepare_network(network_name=var1,
                             cookies_filename=var2,
                             action_func=var3
                             )

    def add_to_recentlyCompletedNames(self, but_nr, name):
        global recently_done_names
        try:
            # If the name already has been noted, assume it has been completed before (or broken) and SKIP IT'
            recently_done_names[name]
            print('HAS ALREADY DONE THIS BEFORE, SKIPPING IT !!!!!!!!')
            self.click_on_button(button=list_of_skip_buttons[but_nr])
        except KeyError:
            # add it to the dict
            recently_done_names[name] = True
            # If the dict is longer than 20 names, clean it.
            if len(recently_done_names) > 20:
                recently_done_names = {}


browser.get('http://kingdomlikes.com/free_points/facebook-likes')
bot_1 = KingdomLikesBot()
bot_1.login_KingdomLikes(email=data['email'], pwd=data['pwd'])

for network_nr in range(1, 6):
    if network_nr == 4:
        continue # Skip liking IG photos - THERE IS AN ERROR

    assume_finnished = False # If two buttons in succession are taking too long to load -> change network
    bot_1.FINNISHED = False
    bot_1.change_network(n=network_nr)
    but_nr = 1
    failed_clicks = 0 # Counts the number of time a button has been clicked on while unclickable (blue loading screen)
    recently_done_names = {}  # To make sure, it doesn't retries the same names several times
    # When the bot (think) it has completed one, temp save it in this dict, if it later reappears
    # don't try to complete it - skip it instead.

    while not bot_1.FINNISHED:
        try:
            print('BUTTON_NR ->', but_nr)
            list_of_like_buttons = WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".button.blue")))
            list_of_skip_buttons = WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, "[Skip]")))
            list_of_names = [x.text for x in browser.find_elements_by_css_selector("div > div.container > div.containertitle.remove > h6")]
            print('Found: like buttons: {}\tskip buttons: {}\t names: {}'.format(len(list_of_like_buttons), len(list_of_skip_buttons), list_of_names))
        except TimeoutException as e:
            print('There is not more points to be earned on this network. Error:', e)
            bot_1.FINNISHED = True
            continue
        try:
            list_of_like_buttons[but_nr].click()
        except IndexError:
            # There isn't a eg. fifth button, set but_nr to click to -> 0
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
            else:
                continue

        failed_clicks = 0 # Counts the number of time a button has been clicked on while unclickable (blue loading screen)

        # Wait for the popup to appear and then switch to it
        if bot_1.switch_to_popup():
            # succesfully switched to popup
            pass
        else:
            # Failed to switch to popup
            continue

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

        print("failure:", bool(failure), failure, failure - 1)
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
            print('but_nr: {}, name: "{}" of type: {}'.format(but_nr, list_of_names[but_nr], type(list_of_names[but_nr])))
            # Check if it is in 'recently_done_names'; if it is SKIP IT; else add it to the dict.
            bot_1.add_to_recentlyCompletedNames(but_nr=but_nr, name=list_of_names[but_nr])

            # Succesfully handled the popup; 'but_nr += 1' so handle the next but_nr popup
            but_nr += 1
            sleep(2)

        assume_finnished = False