
import os
import csv
from string import Template
import re
import urllib, urllib2

from HTMLParser import HTMLParser
import BeautifulSoup

csv_source = os.getcwd()+ '/metadata/'
html_output_file = os.getcwd()+'/website/Global_overview.html'

html_file = os.getcwd()+'/website/index.html'

html = urllib2.urlopen('file:///'+html_file).read()




#html_part01 = html.split('polygonA')[0]
#html_part02 = html.split('polygonA')[2]


for file in os.listdir(csv_source):
    if file.endswith('.csv'):
        file = csv_source+ file

        with open(file) as csvfile:
            reader =  csv.reader(csvfile)
            top_left =  [18]
            top_right = [19]
            bottom_right = [20]
            bottom_left = [21]
            names = [2]

            next(reader)
            for row in reader:
                if not row[18] == '':
                    html_split = len(list(html.split('polygon')))

                    #if html_split > :
                    html_part011 = html.split('addTo(earth);')[0]

                    html_part01 = html_part011
                    html_part012 = html.split('addTo(earth);')[1:-1]

                    if len(html_part012)<2:
                        html_part01 = html_part011 + 'addTo(earth);\n'

                    else:
                        for k in html_part012:
                            html_part01 = html_part01+'addTo(earth);' +k

                    html_part02 = html.split('addTo(earth);')[-1]

                    #else:
                    #    html_part01 = html.split('addTo(earth);')[0]
                     #   html_part02 = html.split('addTo(earth);')[-1]


                    if not top_left == '':
                        coordinates = [top_left, top_right, bottom_right, bottom_left]
                        coord_final = []


                        for i in coordinates:
                            c = list(row[j] for j in i)
                            c = str(c)

                            c = c.replace(', 0.0)', '')
                            m01 = c.split(', ')[0]
                            m02 = c.split(', ')[1]

                            c = m02 +', '+m01


                            c = c.replace("['(", '')
                            c = c.replace("']", '')

                            coord_final.append(c)



                        name = list(row[i] for i in names)
                        name = str(name).replace("['", '')
                        name = str(name).replace("']", '')
                        name = name.replace(',', '')
                        name = name.replace(' ', '')




                        current_polygon = 'WE.polygon([['+coord_final[0]+'], ['+coord_final[1]+'], ['+coord_final[2]+'], ['+coord_final[3]+'], ['+coord_final[0]+']]);'


                    html = html_part01+'addTo(earth);\n'+ '\t\tpolygon'+ name +' = '+current_polygon + '\n' +'\t\tpolygon'+ name +'.addTo(earth);' + html_part02



                    out_file = open(html_output_file, "wb+")
                    out_file.write(html)
                    out_file.close()


f = open(html_output_file,"r")
lines = f.readlines()
f.close()

f = open(html_output_file,"wb+")

for line in lines:
  if line!="addTo(earth);"+"\n":
    f.write(line)
f.close()