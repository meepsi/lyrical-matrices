import os
import argparse
import pandas as pd
from re import sub as s
from matplotlib import pyplot as plt
from glob import glob
import math


# Version Number
vers = "0.1"


# Description
desc = (
    f"""This python 3 script takes lyrics in the form of .txt files and """
    f"""plots them correlation matrices. A correlation matrix is """
    f"""a table showing correlation coefficients between sets of variables """
    f"""(in our case words in a given song). Each word in the table is """
    f"""correlated with each of the other words in the table. This allows """
    f"""us to observe which pairs have the highest correlation (which pairs """
    f"""of words match). In our case, we are using this correlation matrix """
    f"""to give a visual representation of repetition and patterns found """
    f"""in a given song. For formatted title option, lyrics .txt files must """
    f"""be named in the following format: """
    f"""'##_Artist-Name_Album-Name_Song-Name.txt' (## is track number). For """
    f"""example '19_Pink-Floyd_The-Wall_Comfortably-Numb.txt'""")


# Default names and directories
root = os.path.dirname(os.path.abspath(__file__))
default_dir = os.path.join(root, 'lyrics')
default_image = 'lyrical_matrices.png'


# CLI Arguements
parser = argparse.ArgumentParser(description=desc)
parser.add_argument(
    "-V", "--version", help="show program version", action="store_true")
parser.add_argument(
    "-c", "--columns", help="sets column count of output image (default = 4)")
parser.add_argument(
    "-d", "--directory",
    help=f"sets lyrics directory (default is {default_dir})")
parser.add_argument(
    "-o", "--output",
    help=f"sets filepath (default is {os.path.join(root, default_image)})")
parser.add_argument(
    "-dpi", "--dots-per-inch",
    help="effects resolution of output image (default is 100)")
parser.add_argument(
    "-F", "--formatted-title", help="use formatted title for subplot name",
    action="store_true")


# CLI Arguement Actions
args = parser.parse_args()
if args.version:
    print(f"Lyrical Matrices v.{vers}")
if args.columns:
    col_count = int(args.columns)
else:
    col_count = 4
if args.directory:
    lyrics_dir = args.directory
else:
    lyrics_dir = default_dir
if args.output:
    images = args.output
else:
    images = os.path.join(root, default_image)
if args.dots_per_inch:
    dpi = int(args.dots_per_inch)
else:
    dpi = 100
if args.formatted_title:
    formatted_title = True
else:
    formatted_title = False


# List of lyrics .txt files to be processed
file_list = glob(os.path.join(lyrics_dir, '*.txt'))


# Printing parameter information
print(f"Looking for lyrics .txt files in {lyrics_dir}")
print(f"Files Found: {len(file_list)}")
print(f"Column count set to {col_count}\n")


# Using file count and column count to derive subplot parameters
if len(file_list) > col_count:
    height = math.ceil(len(file_list) / col_count)
else:
    height = 1
if len(file_list) <= col_count:
    width = len(file_list)
else:
    width = col_count


# Generating matrix subplots
i = 0
os.chdir(lyrics_dir)
plt.figure(figsize=(10 * width, 11 * height), dpi=dpi)
for file in glob('*.txt'):
    i += 1
    lyrics_1 = open(file)
    wordlist = []
    for word in lyrics_1:
        wordlist.append(word.split(' '))

    lyrics = []
    for line in wordlist:
        for word in line:
            lyrics.append(s('[^a-zA-Z0-9_]+', '', word.lower()))

    matrix = []
    for y in lyrics:
        row = []
        for x in lyrics:
            if x == y:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)

    if formatted_title is True:
        track_no, artist, album, title = file.split('_')
        artist = s('-', ' ', artist)
        album = s('-', ' ', album)
        title = s('.txt', '', title)
        title = s('-', ' ', title)
        print(f"\nArtist: {artist}\nAlbum: {album}\nTitle: {title}\n")
        subplot_title = f"{artist} - {title}"
    else:
        print(f"{file}")
        subplot_title = f"{file}"
    print(
        f"Unique Words: {len(set(lyrics))}\n"
        f"Total Words: {len(lyrics)}\n"
        f"Proportion of Unique Words: {len(set(lyrics)) / len(lyrics)}")

    df_matrix = pd.DataFrame(matrix)

    print(height, width, i)

    plt.subplot(height, width, i)
    plt.imshow(df_matrix.corr())
    plt.title(subplot_title, fontsize=24)
    plt.xlabel(
        f"Repetitiveness: {len(set(lyrics)) / len(lyrics)}", fontsize=24)
    plt.tick_params(
        which='both', bottom=False, top=False, left=False, right=False,
        labeltop=False, labelleft=False, labelright=False, labelbottom=False)


# Rendering output image
print(f"\nSaving {images}")
plt.tight_layout()
plt.savefig(images)
