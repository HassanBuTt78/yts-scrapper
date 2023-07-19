import json

with open('lists/movie_links.json' ,  'r') as file:
    file = json.load(file)
    new_list = file


with open('lists/movie_pages.json' ,  'r') as file:
    file = json.load(file)
    old_list = file


new_list = set(new_list)
old_list = set(old_list)

update_list =  list(new_list - old_list)

with open('lists/update_list.json', 'w') as file:
    to_update = json.dumps(update_list)
    file.write(to_update)

print("file Written")


