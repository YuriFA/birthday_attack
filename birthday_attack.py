import string
import random
import sys

BIT_COUNT = 32
KEYS_COUNT = pow(2, BIT_COUNT//2)
PATH = 'keys.txt'
HASHED_PATH = 'hashed_keys.txt'
READ = True

def main():
	rand_keys = gen_keys(KEYS_COUNT)
	rk_hashes = get_hash(rand_keys)

	if len(sys.argv) > 1 or READ:
		with open(PATH, 'r') as handle:
			keys = handle.read().splitlines()
		with open(HASHED_PATH, 'r') as handle:
			k_hashes = handle.read().splitlines()
		k_hashes = list(map(int, k_hashes))
		print('readed...')
	else:
		keys = gen_keys(KEYS_COUNT)
		k_hashes = get_hash(keys)
		with open(PATH, 'w') as handle:
			handle.write('\n'.join(key for key in keys))
		with open(HASHED_PATH, 'w') as handle:
			handle.write('\n'.join(str(khash) for khash in k_hashes))
		print('writed...')

	conflicts = set(rk_hashes).intersection(k_hashes)
	for hash in conflicts:
		print('{0} and {1} have one hash {2}'.format(rand_keys[rk_hashes.index(hash)], keys[k_hashes.index(hash)], hash))

def get_hash(keys=[]):
	ret = []
	for key in keys:
		ret.append(hash37(key, BIT_COUNT))
	return ret

def gen_keys(cnt=1):
	ret = []
	for i in range(cnt):
		ret.append(k_generator())
	return ret

def k_generator(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def pjw_hash(key):
	BitsInUnsignedInt = BIT_COUNT
	ThreeQuarters = int((BitsInUnsignedInt  * 3) / 4)
	OneEighth = int(BitsInUnsignedInt / 8)
	HighBits = (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
	hash = 0
	test = 0

	for i in key:
		hash = (hash << OneEighth) + ord(i)
		test = hash & HighBits
		if test != 0:
			hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));
	return (hash & 0x7FFFFFFF)

def hash37(str, bit_len=32):
	cur_hash = 2139062143
	for ch in str:
		c_ch = int(ch) if ch.isnumeric() else ord(ch)
		cur_hash = ((1 << bit_len) - 1) & 37 * cur_hash + c_ch
	return cur_hash

if __name__ == '__main__':
	main()