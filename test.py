import random
import string

blog_title = "create new appplication"
random_words =

blog_slug = blog_title.replace(' ', '-') + "-" + ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
print(blog_slug)
