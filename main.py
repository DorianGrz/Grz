import random
a = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

password = ""

lenght = int(input('jaka długość hasła?'))
for i in range(lenght):
    password += random.choice(a)
print(f'twojehasło: - {password}')
