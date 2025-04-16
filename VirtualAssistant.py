#import required packages
import datetime
import pyjokes
import wikipedia
import webbrowser
import time
import speech_recognition as sr
import random
import requests
import aiohttp
import asyncio

import pygame
import threading
import textwrap
import os
API_KEY = "6"


#define the user input and screen
user_input = ""
screen = None  

#initialize the pygame screen
def init_pygame():
  
    global screen
    pygame.init()
    pygame.display.set_caption("Albert Visual")
    screen = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.font.init()

#define the locaions of images used and display the image that alligns with paramiter "topic"
def display_image(topic):
    global screen
    images = {
        "joke": r"/home/alexashton/albert/laughing.png",
        "sunny": r"/home/alexashton/albert/sunny.png",
        "rainy": r"/home/alexashton/albert/rainy.png",
        "partly sunny": r"/home/alexashton/albert/partlycloudy.png",
        "cloudy": r"/home/alexashton/albert/cloudy.png"
  }
    try:
        image_path = images.get(topic)
        
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, (800, 600))
        screen.blit(img, (0, 0))
    except Exception as e:
        print("Error displaying image")
    pygame.display.flip()
  


#speaks out loud what is passed into the text parameter
def speak(text):
    os.system(f'espeak-ng -v mb-us2 "{text}"')

#listens for any input through the microphone
def listen_from_microphone(recognizer, source):
    global user_input
    try: 
        audio = recognizer.listen(source, timeout=5)  
        user_input = recognizer.recognize_google(audio).lower()
        print(f"You said: {user_input}")
    except sr.WaitTimeoutError:
        print("No speech detected.")
        user_input = ""
    except sr.UnknownValueError:
        print("Sorry, didn't catch that.")
        user_input = ""
    except sr.RequestError as e:
        print(f"Recognition error: {e}")
        user_input = ""
            
#main runner that recognizes when albert is said and calls any function that follows its name
async def run_maria():
    global user_input

    while True:
        #defines the exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                speak("Goodbye")
                pygame.quit()
                return

       
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            print("Say something...")
            await asyncio.to_thread(listen_from_microphone, recognizer, source)

        if "albert" in user_input:
            user_input = user_input.replace("albert", "").strip()
            print(f"You said: {user_input}")
            

            if "time" in user_input:
                await display_time()

            elif "joke" in user_input:
                await tell_joke()

            elif "play" in user_input:
                await play_youtube_video(user_input)

            elif "who is" in user_input or "what is" in user_input:
                await search_wikipedia(user_input)

            elif "exit" in user_input or "quit" in user_input:
                speak("Goodbye!")
                pygame.quit()
                break

            elif "weather" in user_input:
                await tell_weather(user_input)
            elif "hello" in user_input or "hi" in user_input:
                await greet_user()
            elif "quote" in user_input:
                await tell_quote()
            elif "random number" in user_input:
                await generate_random_number()
            else:
                speak("Sorry, I didn't understand that. Try asking for the time, a joke, or something else.")
            user_input = "" 
#clears the screen of any pictures after 5 seconds
async def clear_screen_after_delay():
    await asyncio.sleep(5)
    screen.fill((0, 0, 0))
    pygame.display.flip()

#gets the current time in 24 hour time
async def display_time():
    now = datetime.datetime.now()
    time_str = f"Current time: {now.strftime('%H:%M')}"
    print(time_str)

    #displays the text for time
    font = pygame.font.Font(None, 100)
    text_surface = font.render(time_str, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(1000, 300))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    speak(time_str)
    await clear_screen_after_delay()
#gets a random pyjoke
async def tell_joke():
    joke = pyjokes.get_joke()
    print("Here's a joke: ", joke)
    display_image("joke")
    #wrap the text and divide into lines to make easeir to fit on screen and render and then displays and says the joke
    font = pygame.font.Font(None, 50)
    wrapped_lines = textwrap.wrap(joke, width = 40)
    y = 250 - (len(wrapped_lines) *30)
    for l in wrapped_lines:
        text_surface = font.render(l, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = (1400, y))
        screen.blit(text_surface, text_rect)
        y+= 60
    pygame.display.flip()
    speak(joke)
    await clear_screen_after_delay()
#gets a greeting and displays it and says it out loud
async def greet_user():
    greetings = ["Hello!", "Hi there!", "Hey! How can I help?"]
    greeting = random.choice(greetings)
    font = pygame.font.Font(None, 150)
    text_surface = font.render(greeting, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = (900, 500))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    speak(greeting)
    await clear_screen_after_delay()
    
#displays and says a quote using a random quote from the list below
async def tell_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "Do or do not. There is no try. - Yoda",
    ]
    quote = random.choice(quotes)
    font = pygame.font.Font(None, 75)
    text_surface = font.render(quote, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = (1000, 300))
    
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    speak("Quote:"+quote)
    await clear_screen_after_delay()

#displays and says a randomly generated number
async def generate_random_number():
    num = str(random.randint(0, 1000))
    font = pygame.font.Font(None, 400)
    text_surface = font.render(num, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = (900, 300))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    speak("Your random number is: "+num)
    await clear_screen_after_delay()

#opens a query on youtube through the browswer. As of right now I don't know how I can get to play video besides clicking on it.
async def play_youtube_video(user_input):
    video_query = user_input.replace("play", "").strip()
    if video_query:
        query = f"https://www.youtube.com/results?search_query={video_query}"
        webbrowser.open(query)
        speak(f"Opening YouTube for: {video_query}")
    else:
        speak("Please specify a video to search for.")
    display_image("random")
    await clear_screen_after_delay()

#takes the information found from the get_wikipedia_summary and says the infromation found
async def search_wikipedia(user_input):
    search_term = user_input.replace("who is", "").replace("what is", "").strip()
    if search_term:
        
        result = await get_wikipedia_summary(search_term)
        print(f"From Wikipedia: {result}")
        speak(result)
            
        
    else:
        speak("Please specify a person or topic to search for.")
    
    await clear_screen_after_delay()

#seperated from rest of wikipedia function due to error handling, searches wikipedia for information on the query
async def get_wikipedia_summary(query):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, wikipedia.summary, query, 1)
    except Exception as e:
        print("Could not retrieve the information")
        speak("Could not retrieve the information")

#gets the weather from an online weather API and displays the information found as well as a picture of the weather type. It also says the weather
async def tell_weather(user_input):
    display_image("weather")
    city = ""
    if "in" in user_input:
        city = user_input.split("in")[-1].strip().lower().replace("today", "").replace("right now", "").strip()
    print(f"Looking up weather for city: '{city}'")
    if not city:
        speak("Please specify a city for the weather report.")
        return
  
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("error"):
                speak(f"City not found. Please try again.")
            else:
                temperature = data["current"]["temperature"]
                temperature = str((float(temperature)*1.8)+32)+ "  Fahrenheit"

                weather_description = data["current"]["weather_descriptions"][0]
                weather_report = f"The Weather in {city} is {weather_description} with a temperature of {temperature}"
                #creates and displays the text for weather on the window
                font_temp = pygame.font.Font(None,150)
                font_city = pygame.font.Font(None,80)
                temp_surface = font_temp.render(f"{temperature:}", True, (255, 255, 255))
                city_surface = font_city.render(city, True, (255, 255, 255))
                print(weather_report)
                temp_rect = temp_surface.get_rect(center=(1600, 250))
                city_rect = city_surface.get_rect(center=(1600, 380))
                screen.blit(temp_surface, temp_rect)
                screen.blit(city_surface, city_rect)
                #displays the correct image for weather
                if "Partly cloudy" in weather_description:
                    display_image("partly sunny")
                elif "cloudy" in weather_description:
                    display_image("cloudy")
                elif "sunny" in weather_description:
                    display_image("sunny")
                
                elif "rainy" in weather_description:
                    display_image("rainy")
                pygame.display.flip()
                speak(weather_report)

    
    await clear_screen_after_delay()

#initzializes the code and starts albert
def main():
    init_pygame()  
    asyncio.run(run_maria()) 

#starts the function that starts the rest of albert
if __name__ == "__main__":
    main()
