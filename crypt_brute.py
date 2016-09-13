from custom_crypt import calc_hash

from itertools import product
from string import ascii_letters
variants = ascii_letters + '0123456789'

prev = ''
for cnt in range(1, 4):
	for cmd in product(variants, repeat=cnt):
		cmd = ''.join(cmd)
		for i in range(1, cnt):
			#разбиваем тестируемую строку на логин и пароль
			#и прибавляем постфикс
			tmp_cmd = cmd[:i] + ':' + cmd[i:] + 'VOplmH2n'
			
			#если хэш совпал - выводим команду и завершаем
			if calc_hash(0, tmp_cmd) == 0xC84E20E52E25E5E8:
				print('!!! login', tmp_cmd.replace(':', ' '))
				exit()
		
		#показываем прогресс
		if len(cmd) > 3 and cmd[-4] != prev:
			print(cmd)
			prev = cmd[-4]
