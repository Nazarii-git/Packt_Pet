import pyscreenshot
import random
import string


def Screenshot():
    im = pyscreenshot.grab()
    random_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    file_name = 'img/{}.png'.format(random_id)
    im.save(file_name)


