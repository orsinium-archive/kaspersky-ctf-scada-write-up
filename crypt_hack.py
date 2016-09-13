from custom_crypt import crc64_tab

#Начальная пара crc-результат
chains = [{
	'crc': 0xC84E20E52E25E5E8,
	's': '',
	}]

#Пароль явно только из печатных символов
from string import printable
printable = set(printable)

s = ''
#Мы можем разгадать только 8 итераций, т.к. на каждой итерации теряем по
#1 байту от CRC (из-за сдвига), длина которого 8 байт (из-за &) 
for it in range(8):
	
	new_chains = []
	for chain in chains:
		crc = chain['crc']
		
		#т.к. calc_hash использует << 8 для CRC, то 8 младших бит совпадут
		#для нового ззначения CRC и использемого значения из crc64_tab
		tmp_end = crc & 0xFF
		#перебираем все значения из crc64_tab
		for tmp2 in crc64_tab:
			#Выбираем лишь те, где совпали последние 8 бит.
			if tmp2 & 0xFF != tmp_end:
				continue
			
			tmp1 = crc64_tab.index(tmp2)
			#получем предыдущее значение CRC
			crp = (crc ^ tmp2) >> 8
			#получем ещё один байт искомой последовательности
			s = chr((tmp1 ^ crp) & 0xFF )
			
			new_chains.append({
				'crc': crp,
				's': s + chain['s']
				})
	
	chains = new_chains
	
	
#Выводим последовательности, которые состоят только из печатных символов
for chain in chains:
	if len(printable & set(chain['s'])) == len(set(chain['s'])):
		print(chain['s'])
