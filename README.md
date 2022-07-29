# Gym-Reservation-Bot

Rohen Chawla

TLDR: This is a Gym Reservation Bot that uses Selenium to webscrape and sign up for gym times.

Last semester I started going to the gym but checking if any spots were open making reservations ahead of time was always a pain. Since I was doing the exact same steps over and over again everytime, I figured it woul be really cool (and look really cool) if I could automate that process instead. So, I researched how to create a webscraping bot and was able to create a program that could go to the USC myrecsports website and perform the actions below.

It first gathers all the gym data from the Village and Lyon Center gyms in a headless (invisible) browser.This takes a bit of time though so while that's going on a page opens that displays random images of cats and is periodically refreshed to keep the user entertained. Then the user is presented with menu options to do things like dipslay rservation info in an Ascii table format using the PrettyTable library, check if a time slot is available to book, or sign up for a specific time slot. All actions work from the terminal.
