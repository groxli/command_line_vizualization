# -*- coding: utf-8 -*-

# Word cloud visualization of command line usage.
from os.path import expanduser # More reliable way to get user directory.
from wordcloud import WordCloud # For word cloud viz.
import matplotlib.pyplot as plt # For outputting the visualizations.
import time # For output filename.

home = expanduser("~") # Get user directory.

def clean_string(s):
    '''
    Function for removing extraneous characters
    '''
    remove_chars = {"./":"", "'":"", "\"":""}
    for x, y in remove_chars.items():
        s = s.replace(x, y)
    return s

def parse_alias(s):
    '''
    Function for parsing aliases that may contain multiple commands.
    
    in: alias string
    out: list of commands contained in alias string
    '''
    commands = []
    splits = s.split("; ")
    for split in splits:
        commands.append(split.split(" ")[0])
    return commands

# Load in any command aliases that exist:
f = open("%s/.bash_profile" % home, "r") # Open bash profile.
bash_lines = f.read().splitlines() # Read in bash profile.
f.close()

# Create a dictionary of aliases that can be looked up when looping
# through the command line history:
aliases = {}
for i in bash_lines:
    if 'alias' in i:
        i = clean_string(i)
        i = i.replace("alias ", "") # Strip out alias text.
        alias = i.split("=")[0] # Get the alias command.
        right_string = i.split("=")[1] # Get the command string for the alias.
        aliases[alias] = right_string # Add alias and command string to dict.

# Load in command history:
f = open("%s/.bash_history" % home, "r") # Open bash history.
command_history = f.read().splitlines() # Read in bash history.
f.close()

# Loop through command history and get first parts:
command_count = {}
all_commands = []
for i in command_history:
    command_list = [] # For holding 1 or more commands.
    command = clean_string(i.split(" ")[0])
    if command in aliases:
        # An alias was used.
        for c in parse_alias(aliases[command]):
            command_list.append(c)
    else:
        command_list.append(command)
    
    # Update dictionary by incrementing command counts:
    for c in command_list:
        if c in command_count:
            command_count[c] = command_count[c] + 1
        else:
            command_count[c] = 1
        all_commands.append(c)

text = ' '.join(all_commands) # Convert from list to string/text for wordcloud.

# Generate a word cloud object.
wordcloud = WordCloud(width=1200, height=800, background_color='white',
                      max_font_size=320, collocations = False).generate(text)
    
output_file = "wordcloud_%s.pdf" % time.strftime("%Y-%m-%d-%H%M%S")

# Display the generated image:
f = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

f.set_size_inches(9, 6)
f.savefig(output_file, dpi=300)