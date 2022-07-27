from multiprocessing.sharedctypes import Value
from PIL import Image, ImageDraw, ImageFont
import argparse
import os

ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI:,\"^`'. "
unicode_chars = "M@¶WØÆÑæ®%Õ&ÔBQNÐ¾ÓÒmÖ©þDÛÃßÂg#wRÊOÅHÚÙ8ÜÁÀGðÄÉÈp$bË¼øãqdKâåê½U¥õA§9ûô06Eñ£4áàPÇéÞèµýäëZhúXóùòküöV5S3Ýaey2FuoÎCnY±ÍÌç][TÏxf7¢¤zs}vLI{tJj1*)|c¿?×(î»«l=+írì<>^³ï\\/÷i¦¡²!ª°¬º\"¯~_¹:¸,\'\xad-´`·.¨\xa0 "

program_dir = os.path.dirname(os.path.realpath(__file__)) + '/'

class Converter:
	def __init__(self):
		self.verbose = False
		self.invert = False
		self.colored = False

		self.src_image = None
		self.input_file = ''
		self.output_file = ''
		self.padding_right = 0
		self.padding_bottom = 0
		self.chars = ascii_chars

		self.font_size = 16
		self.scale = 100

	def get_output_filename(self):
		dot = self.input_file.rindex('.')
		ext = self.input_file[dot:]
		name = self.input_file[:dot]

		return name + '_chars' + ext

	def load_from_args(self, args):
		self.input_file = args['input-file']
		self.output_file = args['output-file'] or self.get_output_filename()
		self.verbose = args['verbose']
		self.colored = args['colored']
		self.chars = unicode_chars if args['unicode'] else ascii_chars
		self.scale = args['scale'] / 100.0
		self.padding_bottom = self.padding_right = args['padding']
		self.padding_bottom = args['padding_bottom'] or self.padding_bottom
		self.padding_right = args['padding_right'] or self.padding_right

	def convert(self):
		print('Saving to file: ' + self.output_file)

		self.src_image = Image.open(self.input_file)

		blockW = int(self.font_size + self.font_size * (self.padding_right / 100))
		blockH = int(self.font_size + self.font_size * (self.padding_bottom / 100))

		self.src_image.thumbnail((self.src_image.width * self.scale, self.src_image.height * self.scale), Image.ANTIALIAS)
		font = ImageFont.truetype(program_dir + 'monospace.ttf', self.font_size)

		if self.colored:
			output_image = Image.new('RGB', (self.src_image.width * blockW, self.src_image.height * blockH), (255, 255, 255))
		else:
			self.src_image = self.src_image.convert('L')
			output_image = Image.new('L', (self.src_image.width * blockW, self.src_image.height * blockH), 255)

		draw = ImageDraw.Draw(output_image)

		full = self.src_image.width * self.src_image.height

		for i in range(self.src_image.height):
			for j in range(self.src_image.width):
				col = self.src_image.getpixel((j, i))

				avg = col
				if self.colored:
					avg = (col[0] + col[1] + col[2]) / 3

				index = int((len(self.chars) - 1) * (avg / 255.0)) 

				current = i * self.src_image.width + j + 1
				percent = int(current / full * 100)

				if self.verbose:
					print('\r', end='')
					print('Processing: ' + str(percent) + '%', end='')
				
				draw.text((j * blockW, i * blockH), self.chars[index], font=font, fill=col)

		print()
		output_image.save(self.output_file)

def scale_arg_type(val):
	val = float(val)
	if val <= 0:
		raise argparse.ArgumentTypeError("Scale must be positive value")
	return val

def help():
	print('''Usage: python main.py input file [output file] [options]

Options:
	-v or --verbose       enable verbose output
	-c or --colored       make characters colored
	-u or --unicode       use unicode characters instead of ascii 

	-s [float] or --scale [float]             set source image scaling (default value: 100 or one character for any pixel)
	
	-f [integer] or --font-size [integer]     set font size (default value: 16)
	
	-p [float] or --padding [float]           set characters padding from right and bottom (distance between characters). Default value: 0. Can take negative values.
	
	-pr [float] or --padding-right [float]    set characters padding only from right. Default value: 0. Can take negative values.
	
	-pb [float] or --padding-bottom [float]   set characters padding only from bottom. Default value: 0. Can take negative values.'''
)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input-file', metavar='input file')
	parser.add_argument('output-file', metavar='output file', nargs='?', default=None)
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-c', '--colored', action='store_true')
	parser.add_argument('-u', '--unicode', action='store_true')
	parser.add_argument('-s', '--scale', type=scale_arg_type, nargs='?', default=100)
	parser.add_argument('-f', '--font-size', type=int, nargs='?', default=16)
	parser.add_argument('-p', '--padding', type=float, nargs='?', default=0)
	parser.add_argument('-pr', '--padding-right', type=float, nargs='?', default=None)
	parser.add_argument('-pb', '--padding-bottom', type=float, nargs='?', default=None)

	args = vars(parser.parse_args())

	converter = Converter()
	converter.load_from_args(args)
	converter.convert()

if __name__ == '__main__':
	main()