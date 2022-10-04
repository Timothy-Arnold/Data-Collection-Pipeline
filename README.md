# Data-Collection-Pipeline

This is a project to make a...

## Milestone 1

I chose the Amazon website to scrape laptop data from, since it shows a wide variety of brands of laptop and gives a varied dataset. Using Selenium I created methods within a class to navigate Amazon's pages, while collecting the links to each product on display (Around 300 links).
  
```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, URL = "https://www.amazon.co.uk/"):
        self.driver = webdriver.Chrome()
        self.URL = URL
        self.link_list = []
    def open_webpage(self):
        self.driver.get(self.URL)
        time.sleep(2)
    def input_search(self, search_string):
        search = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search.send_keys(search_string)
        search.send_keys(Keys.RETURN)
        time.sleep(1)
    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(By.ID, "sp-cc-accept")
            accept_cookies_button.click()
        except:
            pass
    def get_links(self):
        product_container = self.driver.find_element(By.XPATH, '//div[@class = "s-main-slot s-result-list s-search-results sg-row"]')
        product_list = product_container.find_elements(By.XPATH, '//div[@class = "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"]')
        for product in product_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        time.sleep(1)
    def next_page(self):
        next_button = self.driver.find_element(By.XPATH, '//a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        next_button.send_keys(Keys.RETURN)
        time.sleep(1)

def scrape():
    scrape = Scraper()
    scrape.open_webpage()
    scrape.accept_cookies()
    scrape.input_search("laptop")
    # Get first page's links
    scrape.get_links()
    for page in range(18):
        scrape.next_page()
        scrape.get_links()
    print(scrape.link_list)
    print(f'There are {len(scrape.link_list)} properties in this page')
    time.sleep(60)

if __name__ == '__main__':
    scrape()
```

## Milestone 2

For this milestone I 

```python

```

## Milestone 3

In milestone 3 I built the check_letter and check_word methods which would be called by the ask_letter method upon receiving a valid input. For incorrect inputs I reduced the num_lives attribute by 1, and for correct inputs I either reduced the num_letters attribute by 1, or all the way down to 0 in the case of a correct word (signifying a win). In the ask_letter method I used a for loop to replace blank spaces with the inputed letter if said letter was in the word.

```python
    def check_letter(self, letter) -> None:
        '''
        Checks if the letter is in the word.
        If it is, it replaces the '_' in the word_guessed list with the letter.
        If it is not, it reduces the number of lives by 1.

        Parameters:
        ----------
        letter: str
            The letter to be checked

        '''
        if letter in self.word:
            print(f"Nice! {letter} is in the word!")
            self.number_letters -= 1
            for index in range(len(self.word)):
                if self.word[index] == letter:
                    self.word_guessed[index] = letter
            print(self.word_guessed)
        else:
            self.num_lives -= 1
            print(f'Sorry, {letter} is not in the word.\nYou have {self.num_lives} lives left.')
            print(Hangman_images[self.num_lives])
        if self.number_letters != 0:
            print(f"You have already tried: {self.list_letters}")

    def check_word(self, word) -> None:
        '''
        Checks if the word guessed is correct.
        If it is, it replaces all of the '_' in the word_guessed list with the correct letters.
        If it is not, it reduces the number of lives by 1.

        Parameters:
        ----------
        word: str
            The word to be checked

        '''
        if word == self.word:
            print(f"Nice! {word} is the word!")
            self.number_letters = 0
            print(list(word))
        else:
            self.num_lives -= 1
            print(f'Sorry, {word} is not the word.\nYou have {self.num_lives} lives left.')
            print(Hangman_images[self.num_lives])
        if self.number_letters != 0:
            print(f"You have already tried: {self.list_letters}")
```

## Milestone 4

For the final milestone I defined a function which would start an instance of the game by iteratively asking the user for a letter. I also coded the winning / losing conditions of the game which would break the while loop of asking for letters and print a winning / losing statement.

```python
def play_game(word_list):
    game = Hangman(word_list)
    while True:
        game.ask_letter()
        if game.num_lives == 0:
            print(f"You ran out of lives. The word was {game.word}.")
            break
        if game.number_letters == 0:
            if game.num_lives == 5:
                print("Congratulations, you won without losing any lives!")
            else:
                print("Congratulations, you won!")
            break

if __name__ == '__main__':
    word_list = ['apple', 'banana', 'orange', 'pear', 'strawberry', 'watermelon']
    play_game(word_list)
```

## Conclusions

Writing this hangman project involved using loops, game logic etc. in order to define functions, all within the framework of a class to help carry out each instance of the game. In the future I would consider making a front end GUI for the game using Tkinter which would make it more accessible to the user.