from PIL import Image, ImageDraw, ImageFont
import sys

asciiChars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
unicodeChars = "M@¶WØÆÑæ®%Õ&ÔBQNÐ¾ÓÒmÖ©þDÛÃßÂg#wRÊOÅHÚÙ8ÜÁÀGðÄÉÈp$bË¼øãqdKâåê½U¥õA§9ûô06Eñ£4áàPÇéÞèµýäëZhúXóùòküöV5S3Ýaey2FuoÎCnY±ÍÌç][TÏxf7¢¤zs}vLI{tJj1*)|c¿?×(î»«l=+írì<>^³ï\\/÷i¦¡²!ª°¬º\"¯~;_¹:¸,\'\xad-´`·.¨\xa0 ";
programDir = __file__[:__file__.rindex('/') + 1];

class Converter:
	def __init__(self):
		self.verbose = False;
		self.writeTxt = False;
		self.invert = False;
		self.colored = False;

		self.srcImage = None;
		self.inputFilename = '';
		self.outputFilename = '';
		self.paddingRight = 0;
		self.paddingBottom = 0;
		self.chars = asciiChars;

		self.fontSize = 16;
		self.scale = 100;

	def getOutputFilename(self):
		dot = self.inputFilename.rindex('.');
		ext = self.inputFilename[dot:];
		name = self.inputFilename[:dot];

		self.outputFilename = name + '_chars' + ext;

	def convert(self):
		if self.outputFilename == '':
			self.getOutputFilename();

		print('Saving to file: ' + self.outputFilename);

		if self.writeTxt:
			txt = open('output.txt', 'w');

		blockW = int(self.fontSize + self.fontSize * (self.paddingRight / 100));
		blockH = int(self.fontSize + self.fontSize * (self.paddingBottom / 100));

		self.srcImage.thumbnail((self.srcImage.width * self.scale, self.srcImage.height * self.scale), Image.ANTIALIAS);
		font = ImageFont.truetype(programDir + 'monospace.ttf', self.fontSize);

		if self.colored:
			outputImage = Image.new('RGB', (self.srcImage.width * blockW, self.srcImage.height * blockH), (255, 255, 255));
		else:
			self.srcImage = self.srcImage.convert('L');
			outputImage = Image.new('L', (self.srcImage.width * blockW, self.srcImage.height * blockH), 255);

		draw = ImageDraw.Draw(outputImage);

		full = self.srcImage.width * self.srcImage.height;

		for i in range(self.srcImage.height):
			for j in range(self.srcImage.width):
				col = self.srcImage.getpixel((j, i));

				avg = col;
				if self.colored:
					avg = (col[0] + col[1] + col[2]) / 3;

				index = int((len(self.chars) - 1) * (avg / 255.0)); 

				current = i * self.srcImage.width + j + 1;
				percent = int(current / full * 100);

				if self.verbose:
					print('\r', end='');
					print('Processing: ' + str(percent) + '%', end='');

				if self.writeTxt:
					txt.write(self.chars[index]);
				
				draw.text((j * blockW, i * blockH), self.chars[index], font=font, fill=col);
			
			if self.writeTxt:
				txt.write('\n');

		print();
		outputImage.save(self.outputFilename);

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def checkFilename(name):
	try:
	    f = open(name);
	    f.close()
	    # Do something with the file
	except IOError:
	    return False;

	return True;

def main():
	argv = sys.argv[1:];
	argc = len(argv);

	if '--help' in argv or '-h' in argv:
		print('Help!');
		exit();

	if argc < 1:
		print("Error!")
		exit();

	converter = Converter();
	if argc >= 1:
		converter.inputFilename = argv[0];
		converter.srcImage = Image.open(argv[0]);

	if argc >= 2:
		if checkFilename(argv[1]):
			converter.outputFilename = argv[1];

		if '--verbose' in argv or '-v' in argv:
			converter.verbose = True;
		if '--output-txt' in argv or '-o' in argv:
			converter.writeTxt = True;
		if '--invert' in argv or '-i' in argv:
			converter.invert = True;
		if '--colored' in argv or '-c' in argv:
			converter.colored = True;
		if '--unicode' in argv or '-u' in argv:
			converter.chars = unicodeChars;

		for i in range(argc):

			if argv[i] == '--scale' or argv[i] == '-s':
				if i == (argc - 1) or not isfloat(argv[i + 1]):
					print('Error!');
					exit();
				else:
					converter.scale = float(argv[i+1]) / 100.0;

			if argv[i] == '--font-size' or argv[i] == '-f':
				if i == (argc - 1) or not isint(argv[i + 1]):
					print('Error!');
					exit();
				else:
					converter.fontSize = int(argv[i+1]);

			if argv[i] == '--padding-right' or argv[i] == '-pr':
				if i == (argc - 1) or not isfloat(argv[i + 1]):
					print('Error!');
					exit();
				else:
					converter.paddingRight = float(argv[i+1]);

			if argv[i] == '--padding-bottom' or argv[i] == '-pb':
				if i == (argc - 1) or not isfloat(argv[i + 1]):
					print('Error!');
					exit();
				else:
					converter.paddingBottom = float(argv[i+1]);

			if argv[i] == '--padding' or argv[i] == '-p':
				if i == (argc - 1) or not isfloat(argv[i + 1]):
					print('Error!');
					exit();
				else:
					converter.paddingRight = float(argv[i+1]);
					converter.paddingBottom = float(argv[i+1]);


	converter.convert();

if __name__ == '__main__':
	main()