#!/usr/bin/python
import os

pin_sets = set()
out_wave = ""
pins = {}

def get_pin_name(line_str):
	return line_str[6: line_str.find("=")]

def get_pin_status(line_str):
	return (line_str.split("=")[1]).split("\n")[0]

def get_delay_time_us(line_str):
	return ((line_str.split("=")[1]).split("us")[0]).strip()

def continue_wave_point():
	global out_wave
	for ss in pin_sets:
		out_wave += pins[ss] + ','
	out_wave += '\n'

def add_wave_point(pin, status):
	pints[pin] = status
	continue_wave_point()

def wavelog_parser(src_file, dst_file):
	# Find all pins
	for line in src_file:
		if line.startswith("@@PIN:"):
			pin_sets.add(get_pin_name(line))
	# Add pins
	for pin in pin_sets:
		pins[pin] = "0"
	src_file.seek(0)
	for line in src_file:
		if line.startswith("@@PIN:"):
			add_wave_point(get_pin_name(line, get_pin_status(line)))
		elif line.startswith("@@DELAY"):
			for i in range(5 * int(get_delay_time_us(line))):
				continue_wave_point()
	print("####################")
	print(pin_sets)
	print("####################")
	for ss in pin_sets:
		dst_file.write(ss + ',')
	dst_file.write('\n')
	dst_file.write(out_wave)


if __name__ == "__main__":
	print("go convert!")
	wave_src_file = open("log1.wavelog", "r")
	wave_dst_file = open("log1.csv", "w")

	wavelog_parser(wave_src_file, wave_dst_file)

	wave_src_file.close()
	wave_dst_file.close()
	print("convert done!")
