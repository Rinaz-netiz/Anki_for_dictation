import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from tqdm import tqdm
from rich.prompt import Prompt
from rich.console import Console

from typing import AnyStr, List
import csv


def req_to_site(url: str) -> AnyStr:
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return ""


def parse_words(text: str) -> List[list]:
    soup = BeautifulSoup(text, "lxml")
    bodies = soup.find_all(class_="box_heading2")[1:]
    words = []
    for body in bodies:
        ul = body.find(class_="pt_spacer")

        if ul:
            for li in ul.find_all("li"):
                words.append(li.text.split(" – "))

    return words


def write_to_csv(data: List[list]) -> None:
    file_name = "words.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)
    print(f"{file_name} is ready")


def create_voice(data: List[list]) -> List[list]:
    res = []
    for word in tqdm(data, desc="Creating voice files"):
        try:
            tts = gTTS(word[1])
            tts.save(f"voices/{word[1].replace('/', ' ')}.mp3")
            res.append([f"[sound:{word[1].replace('/', ' ')}.mp3]", word[0]])
        except FileNotFoundError:
            print(f"Couldn't create  sound for: {word[0]}: {word[1]}")

    print("Media is ready")
    return res


def main(url: str) -> None:
    content = req_to_site(url)
    data = parse_words(content)
    res = create_voice(data)
    write_to_csv(res)


if __name__ == "__main__":
    console = Console()
    url = Prompt.ask("[bold green]Please enter the URL[/bold green]:", default="https://")
    console.print(f"You entered: [bold blue]{url}[/bold blue]")
    main(url)