import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import difflib
import shutil
from tqdm import tqdm
from openpyxl import load_workbook
from urllib.parse import urlparse

def scrap_urls(urls, folder_name):
    try:
        with tqdm(total=len(urls), desc="Scraping pages", position=0, leave=True) as pbar:
            for url in urls:
                scrap_url(url, folder_name)
                pbar.update(1)
    except Exception as e:
        return str(e)

def scrap_url(url, folder_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
                content += f"Titre de la page : {title}\n\n"
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                content += f"{paragraph.get_text()}\n"
            parsed_url = urlparse(url)
            filename = parsed_url.netloc + parsed_url.path.replace("/", "_") + ".txt"
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
        else:
            print(f"La requête pour {url} a échoué avec le code d'état: {response.status_code}")
    except Exception as e:
        print(str(e))

def compare_archives(archive_folder):
    try:
        archives = sorted([folder for folder in os.listdir(archive_folder) if os.path.isdir(os.path.join(archive_folder, folder))])
        if len(archives) < 2:
            return "Au moins deux archives sont nécessaires pour la comparaison."
        latest_archive = os.path.join(archive_folder, archives[-1])
        latest_files = os.listdir(latest_archive)
        latest_content = {}
        for file in latest_files:
            with open(os.path.join(latest_archive, file), 'r', encoding="utf-8") as f:
                latest_content[file] = f.readlines()
        previous_archive = os.path.join(archive_folder, archives[-2])
        previous_files = os.listdir(previous_archive)
        previous_content = {}
        for file in previous_files:
            with open(os.path.join(previous_archive, file), 'r', encoding="utf-8") as f:
                previous_content[file] = f.readlines()
        differences = {}
        with tqdm(total=len(latest_files), desc="Comparing files", position=0, leave=True) as pbar:
            for file in latest_files:
                if file in previous_files:
                    latest_content_lines = latest_content[file]
                    previous_content_lines = previous_content[file]
                    diff = difflib.unified_diff(previous_content_lines, latest_content_lines)
                    differences[file] = list(diff)
                else:
                    differences[file] = ["Le fichier n'existe pas dans l'archive précédente."]
                pbar.update(1)
        for file, diff in differences.items():
            if diff and not all(line.startswith(' ') for line in diff):
                print(f"Différences détectées dans le fichier : {file}")
                for line in diff:
                    if line.startswith('+'):
                        print(line.rstrip())
                    elif line.startswith('-'):
                        print(line.rstrip())
                print()
        else:
            return "Pas de différence détectée entre les archives."
    except Exception as e:
        return "Une erreur s'est produite lors de la comparaison des archives : " + str(e)

def main():
    try:
        archive_folder = "archives"
        if not os.path.exists(archive_folder) or len(os.listdir(archive_folder)) < 2:
            print("Création de deux archives initiales...")
            for i in range(2):
                folder_name = os.path.join(archive_folder, "3s2I_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                os.makedirs(folder_name)
                urls = read_urls_from_excel("urls.xlsx")  # Lecture des URLs depuis le fichier Excel
                scrap_urls(urls, folder_name)
        if len(os.listdir(archive_folder)) >= 2:
            oldest_archive = min(os.listdir(archive_folder))
            shutil.rmtree(os.path.join(archive_folder, oldest_archive))
        folder_name = os.path.join(archive_folder, "3s2I_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(folder_name)
        urls = read_urls_from_excel("urls.xlsx")  # Lecture des URLs depuis le fichier Excel
        scrap_urls(urls, folder_name)
        print(compare_archives(archive_folder))
    except Exception as e:
        print("Une erreur s'est produite :", str(e))

def read_urls_from_excel(filename):
    urls = []
    wb = load_workbook(filename)
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        urls.append(row[0])  # Supposant que les URLs sont dans la première colonne
    return urls

if __name__ == "__main__":
    main()
