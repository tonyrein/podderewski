
import string

# From http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
# method renamed and modified slightly, to substitute '-' for invalid characters.

def remove_invalid_filename_chars(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in validFilenameChars else '-' for c in filename)