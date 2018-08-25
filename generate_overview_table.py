import csv
import os
import re

import xlwt,xlrd
from osgeo import gdal, osr



output_path = os.getcwd() +'/metadata/'

cities_path = os.getcwd()+'/_cities/'
cities_web_export_path = os.getcwd()+'/_cities_web_export/'

metadata_path = os.getcwd()+'/metadata/'
xls_name = '2016_2017_cities'


#processed_table = os.getcwd() + '/metadata/processed_table.xlsx'



def overview_tables(input_path, output_path, xls_name):
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)

    #spredsheet header
    processed_table = xlwt.Workbook()

    page_2017 = processed_table.add_sheet(xls_name)


    cols = ['id', 'filename', 'city','state','country','date','date_modified', 'width', 'height', 'print size', 'dpi', 'True Color','Infrared', 'RGB Relief','SAR_RGB','Sigma0_VV_db','Sigma0_VH_db','projectedLocalIncidenceAngle',\
            'top left coordinate','top right coordinate','bottom right coordinate', 'bottom left coordinate', 'WKT Polygon']

    for i,col in enumerate(cols):
        page_2017.write(0,i,str(col))


    processed_table.save(output_path+'/processed_'+xls_name+'_table.xls')



    cities_count = []
    for path, subdirs, files in os.walk(input_path):

            for file in files:
                if file.endswith('dim'):
                    cities_count.append(file)
    print len(cities_count)

    for i, elem in enumerate(cities_count):
        print i, elem
        id = str(100)+'-'+str(i + 1)
        page_2017.write(i + 1, 1, elem)
        page_2017.write(i + 1, 0, id)
        print id

    first_col = page_2017.col(1)
    first_col.width = 550 * 20


    city_name_list = []
    capture_date_list = []
    print_size_list = []
    dpi_list = []
    width_list =[]
    height_list = []

    true_color_list =[]
    infrared_list = []
    RGB_RELIEF_list = []
    SAR_RGB_list = []

    Sigma0_VV_db_list = []
    Sigma0_VH_db_list = []
    angle_list = []

    top_left_coordinate_list = []
    top_right_coordinate_list = []
    bottom_right_coordinate_list = []
    bottom_left_coordinate_list = []

    WKT_gtif_list = []



    for path, subdirs, files in os.walk(input_path):

        for dir in subdirs:
            for path, subdirs, files in os.walk(input_path+'/'+dir):
                for file in files:

                    if file.endswith('dim'):
                        city_name = file.split('_',1)[0]
                        city_name_list.append(city_name)
                        print city_name

                        capture_date = re.findall('\d{2}'+'-'+'\d{2}'+'-'+'\d{4}',file)[0]
                        capture_date_list.append(capture_date)
                        print capture_date


                        if 'SAR' in file and file.replace('.dim', '_RGB.tif') in files:
                            true_color = False
                            true_color_list.append(true_color)
                            print true_color
                        elif file.replace('.dim', '_RGB.tif') in files:
                            true_color = True
                            true_color_list.append(true_color)
                            print true_color
                        else:
                            true_color = False
                            true_color_list.append(true_color)
                            print true_color


                        if file.replace('.dim', '_INFRARED.tif') in files:
                            infrared = True
                            infrared_list.append(infrared)
                            print infrared
                        else:
                            infrared = False
                            infrared_list.append(infrared)
                            print infrared

                        if 'SAR' in file and file.replace('.dim', '_RGB.tif') in files:
                            SAR_RGB = True
                            SAR_RGB_list.append(SAR_RGB)
                            print SAR_RGB
                        else:
                            SAR_RGB = False
                            SAR_RGB_list.append(SAR_RGB)
                            print SAR_RGB

                        if 'SAR_Sigma0_VH' in file and file.replace('.dim', '_db.tif') in files:
                            Sigma0_VH_db = True
                            Sigma0_VH_db_list.append(Sigma0_VH_db)
                        else:
                            Sigma0_VH_db = False
                            Sigma0_VH_db_list.append(Sigma0_VH_db)

                        if 'SAR_Sigma0_VV' in file and file.replace('.dim', '_db.tif') in files:
                            Sigma0_VV_db = True
                            Sigma0_VV_db_list.append(Sigma0_VV_db)
                        else:
                            Sigma0_VV_db = False
                            Sigma0_VV_db_list.append(Sigma0_VV_db)


                        if  file.replace('.dim', '_projectedLocalIncidenceAngle.tif') in files:
                            angle = True
                            angle_list.append(angle)
                        else:
                            angle = False
                            angle_list.append(angle)


                        if  file.replace('.dim', '_RELIEF.tif') in files:
                            RGB_RELIEF = True
                            RGB_RELIEF_list.append(RGB_RELIEF)
                        else:
                            RGB_RELIEF = False
                            RGB_RELIEF_list.append(RGB_RELIEF)




                        print_size = file.split('_', 3)[1]
                        print_size_list.append(print_size)

                        dpi = None
                        bottom_left_coordinate = None
                        bottom_right_coordinate = None
                        top_left_coordinate = None
                        top_right_coordinate = None
                        WKT_gtif = None

                        if '.dim' in file and not((file.replace('.dim', '_RGB.tif') in files) or (file.replace('.dim', '_db.tif') in files)):
                            width = None
                            height = None
                            width_list.append(width)
                            height_list.append(height)


                        #BBox coordinates
                        elif (file.replace('.dim', '_RGB.tif') in files) or (file.replace('.dim', '_db.tif') in files):
                            if '_SAR_Sigma0_VV' in file:
                                file = file.replace('.dim', '_db.tif')
                            elif '_SAR_Sigma0_VH' in file:
                                file = file.replace('.dim', '_db.tif')
                            elif 'SAR' in file:
                                file = file.replace('.dim', '_RGB.tif')
                            else:
                                file = file.replace('.dim', '_RGB.tif')

                            gtif = gdal.Open(path+ '/' + file)

                            old_cs = osr.SpatialReference()
                            old_cs.ImportFromWkt(gtif.GetProjectionRef())

                            transform = osr.CoordinateTransformation(old_cs, new_cs)

                            width = gtif.RasterXSize
                            height = gtif.RasterYSize
                            gt = gtif.GetGeoTransform()

                            width_list.append(width)
                            height_list.append(height)

                            print width, height

                            minx = gt[0]
                            miny = gt[3] + width * gt[4] + height * gt[5]
                            maxx = gt[0] + width * gt[1] + height * gt[2]
                            maxy = gt[3]

                            top_left_coordinate = str(transform.TransformPoint(minx, maxy))
                            top_left_coordinate_list.append(top_left_coordinate)

                            top_right_coordinate = str(transform.TransformPoint(maxx, maxy))
                            top_right_coordinate_list.append(top_right_coordinate)

                            bottom_right_coordinate = str(transform.TransformPoint(maxx, miny))
                            bottom_right_coordinate_list.append(bottom_right_coordinate)

                            bottom_left_coordinate = str(transform.TransformPoint(minx, miny))
                            bottom_left_coordinate_list.append(bottom_left_coordinate)

                            coords = (
                            bottom_left_coordinate + bottom_right_coordinate + top_right_coordinate + top_left_coordinate + bottom_left_coordinate).replace(
                                '(', '')
                            coords = coords.replace(',', '')
                            coords = coords.replace(')', ', ')
                            coords = coords.replace(' 0.0', '')[0:-2]
                            print coords

                            WKT_gtif = 'POLYGON ((' + coords + '))'
                            WKT_gtif_list.append(WKT_gtif)

                            print WKT_gtif

                            if 'dpi' in file:
                                dpi = re.findall('\d{3}' + 'dpi', file)[0]
                                dpi_list.append(dpi)
                                print dpi
                            elif 8465<= width + height <= 8475:
                                dpi = str(300) + 'dpi'
                                dpi_list.append(dpi)
                                print dpi
                            elif 9446 <= width + height <= 9450:
                                dpi = str(200) + 'dpi'
                                dpi_list.append(dpi)
                                print dpi
                            elif 14170 <= width + height <= 14176:
                                dpi = str(300) + 'dpi'
                                dpi_list.append(dpi)
                                print dpi

                        #No-value dummies

                        if dpi == None:
                            dpi_list.append(dpi)

                        if bottom_left_coordinate == None:
                            bottom_left_coordinate_list.append(bottom_left_coordinate)
                        if bottom_right_coordinate == None:
                            bottom_right_coordinate_list.append(bottom_right_coordinate)
                        if top_left_coordinate == None:
                            top_left_coordinate_list.append(top_left_coordinate)
                        if top_right_coordinate == None:
                            top_right_coordinate_list.append(None)
                        if WKT_gtif == None:
                            WKT_gtif_list.append(WKT_gtif)






    #Write to spreadsheet

    for i, elem in enumerate(city_name_list):
        page_2017.write(i + 1, 2, elem)

    col = page_2017.col(2)
    col.width = 250 * 20

    for i, elem in enumerate(capture_date_list):
        page_2017.write(i + 1, 5, elem)

    col = page_2017.col(5)
    col.width = 200 * 20

    for i, elem in enumerate(width_list):
        page_2017.write(i + 1, 7, elem)

    for i, elem in enumerate(height_list):
        page_2017.write(i + 1, 8, elem)

    for i, elem in enumerate(print_size_list):
        page_2017.write(i + 1, 9, elem)

    for i, elem in enumerate(dpi_list):
        page_2017.write(i + 1, 10, elem)

    for i, elem in enumerate(true_color_list):
        page_2017.write(i + 1, 11, elem)

    for i, elem in enumerate(infrared_list):
        page_2017.write(i + 1, 12, elem)

    for i, elem in enumerate(RGB_RELIEF_list):
        page_2017.write(i + 1, 13, elem)

    for i, elem in enumerate(SAR_RGB_list):
        page_2017.write(i + 1, 14, elem)

    for i, elem in enumerate(Sigma0_VV_db_list):
        page_2017.write(i + 1, 15, elem)

    for i, elem in enumerate(Sigma0_VH_db_list):
        page_2017.write(i + 1, 16, elem)

    for i, elem in enumerate(angle_list):
        page_2017.write(i + 1, 17, elem)

    for i, elem in enumerate(top_left_coordinate_list):
        page_2017.write(i + 1, 18, elem)

    for i, elem in enumerate(top_right_coordinate_list):
        page_2017.write(i + 1, 19, elem)

    for i, elem in enumerate(bottom_right_coordinate_list):
        page_2017.write(i + 1, 20, elem)

    for i, elem in enumerate(bottom_left_coordinate_list):
        page_2017.write(i + 1, 21, elem)

    for i, elem in enumerate(WKT_gtif_list):
        page_2017.write(i + 1, 22, elem)





    processed_table.save(output_path+'/processed_'+xls_name+'_table.xls')


    def Excel2CSV(ExcelFile, SheetName, CSVFile):
        workbook = xlrd.open_workbook(ExcelFile)
        worksheet = workbook.sheet_by_name(SheetName)
        csvfile = open(CSVFile, 'wb')
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        for rownum in xrange(worksheet.nrows):
            wr.writerow(
                list(x.encode('utf-8') if type(x) == type(u'') else x
                     for x in worksheet.row_values(rownum)))

        csvfile.close()

    Excel2CSV(output_path+'/processed_'+xls_name+'_table.xls',  xls_name, output_path+'/processed_'+xls_name+'_table.csv')




overview_tables(input_path=cities_path, output_path=metadata_path, xls_name=xls_name)