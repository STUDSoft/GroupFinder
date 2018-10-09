from dataset_parser import *
from serializer import *

try:
    userlist = read("dataset.gfd")
    print("Welcome back!")
except FileNotFoundError:
    print(
        "Welcome! This is your first time here, so we'll need a couple of minutes to load your dataset.\nPlease wait...")
    userlist = get_dataset()
    save(userlist, "dataset.gfd")
    print("Finished! Have fun!")
