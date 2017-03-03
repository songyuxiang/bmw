# Start reading in the data
path_in = "./"
filename=raw_input("csv file name : ")
input_fn = path_in + "/%s.csv"%filename

path_out = path_in + "./"
output_fn = path_out + "%s_out.xodr"%filename

# Top
OpenDRIVE = Element('OpenDRIVE')

# header
header = SubElement(OpenDRIVE, "header")
geoReference = SubElement(header, "geoReference")