import random
import faker


f = faker.Faker()

def gen_rand_files():
    rand_files = {}
    for i in range(random.randint(1,15)):
        rand_files[i] = f.file_name()
    return rand_files

print(gen_rand_files())
