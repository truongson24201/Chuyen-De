# Thành viên:
# 1. Lê Thành Trung - N19DCCN214
# 2. Đinh Trường Sơn - N19DCCN159
# 3. Trần Quang Ngọc Huỳnh - N19DCCN075
def unary_encode(number):
  return '1' * number + '0'


def to_binary(x):
	s = bin(x).removeprefix('0b')
	return s


def gamma_encode(number):
	binary_str = to_binary(number)
	offset = binary_str[binary_str.index('1') + 1:]
	length = unary_encode(len(offset))
	return length + offset

def gamma_decode(binary):
	first_bit_0 = binary.index('0')
	count = len(binary[:first_bit_0])
	binary_str = '1' + binary[first_bit_0 + 1 : first_bit_0 + 1 + count]
	number = int(binary_str, 2)
	return number

if __name__ == '__main__':
	number = 10
	gamma_code = gamma_encode(number)
	gamma_code_decimal = int(gamma_code, 2)
	gamma_decode = gamma_decode(gamma_code)
	print(f'{gamma_code=} {gamma_code_decimal=} {gamma_decode=}')

