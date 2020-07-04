import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def connect_chrome():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    driver.maximize_window()
    time.sleep(2)
    return driver


def scrolldown(self, type_of_page='users'):
    last_height = self.page_source
    attempt = 0
    print('Scrolling down to get all answers...')
    # Scroll down loop until page not changing
    i = 0
    while i < 10:
        if i % 100 == 0:
            print(f'Scrolled {i} times')
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = self.page_source
        if new_height == last_height:
            attempt += 1
            if attempt == 3:  # In the third attempt we end the scrolling
                break
        else:
            attempt = 0
            i += 1
        last_height = new_height
    print('Done scrolling!')


def scrape_user(user, file_path='q_a.txt'):
    browser = connect_chrome()

    url = f'https://www.quora.com/profile/{user}/answers'
    browser.get(url)
    time.sleep(1)

    scrolldown(browser)

    # Find and click on all (more)  to load full text of answers
    more_buttons = browser.find_elements_by_xpath(
        "//div[contains(text(), '(more)')]")
    print(f'Pressing {len(more_buttons)} (more) buttons...')
    for idx, button in enumerate(more_buttons):
        ActionChains(browser).move_to_element(button).click(button).perform()
        if idx % 100 == 0:
            print(f'Pressed {idx} buttons')
    print('Done pressing buttons!')

    # Get the actual answer text
    print('Getting answers...')
    try:
        questionsText = browser.find_elements_by_xpath(
            "//div[@class='q-text puppeteer_test_question_title']")
        questionsText = [' '.join(question.text.split('\n')[:]).replace(
            '\r', '').replace('\t', '').strip() for question in questionsText]

        answersText = browser.find_elements_by_xpath(
            "//div[@class='q-relative spacing_log_answer_content']")
        answersText = [' '.join(answer.text.split('\n')[:]).replace(
            '\r', '').replace('\t', '').strip() for answer in answersText]
    except Exception as eans:
        print('Can\'t get answers :(')
    print(f'{len(answersText)} answers got!')

    with open(file_path, 'w') as out:
        for i in range(len(questionsText)):
            out.write('{\n\t"Question": "' + questionsText[i] + '",\n')
            out.write('\t"Answer": "' + answersText[i] + '"\n},\n')

    browser.quit()


scrape_user('Tom-Stagliano')
