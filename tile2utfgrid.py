# -*- coding: utf-8 -*-
from osgeo import gdal, gdalconst
import codecs
import os
import sys
import csv
import simplejson as json

keys=[] #keys：文字コード32～(34,92は飛ばす)
data={} #dataのリスト：ハッシュキーはkeys、バリューはラスタ値
invdata={} #dataの逆：ハッシュキーはラスタ値、バリューはkeys

k=32

#####
# ラスタの値xが引数。
# xが初めて出る値だったらinvdataに登録。
# 新規文字コードをkeysに登録。
# 文字コードをutf-8に変換してgrid値としてreturn
# xが既出であれば、invdataから引数xに対応する文字コードをutf-8に変換してgrid値としてreturn

def Raster2grid(x):

  if not(invdata.has_key(x)):
   global k
   n = k
   if n == 34 or n == 92:
    n = n+1
   k = n+1
   invdata[x]=n
   keys.append(n)
   return unichr(n)
  return unichr(invdata[x])

def RGBRaster2grid(r,g,b):
  x = str(r)+str(g)+str(b)
  if not(invdata.has_key(x)):
   global k
   n = k
   if n == 34 or n == 92:
    n = n+1
   k = n+1
   invdata[x]=n
   keys.append(n)
   return unichr(n)
  return unichr(invdata[x])

#####
# keysの値xが引数。
# keysの値に対応するdataを文字列として返す
# ラスタ値はval


def Keys2data(x):
  global data
  global legend
  
  ####凡例がない場合ラスタの値をvalで返す
  if not(legend.has_key(data[x])):
   return '"' +  str(x) + '":' + '{"V":"' + str(data[x]) +'"}'
  ####凡例がある場合、日本語の処理をしてから返す。参考 http://taichino.com/programming/1599
  orig = json.dumps(legend[data[x]], indent=4)
  return '"' +  str(x) + '":' + eval("u'''%s'''" % orig).encode('utf-8')

def tile2json(file):
	global data
	_root,_ext = os.path.splitext(file)
        jsonfile = _root + ".json"

	dataset = gdal.Open(file, gdalconst.GA_ReadOnly)
	band    = dataset.GetRasterBand(1)
	dat_matrix = band.ReadAsArray()

	f = codecs.open(jsonfile, "w",'utf-8')
	######## grid,keys,data作成、grid書き込み
	f.write('{"grid":[')
	for i in range(0,band.YSize - 2): #for last comma remove
	 text = "".join(map(Raster2grid,dat_matrix[i,:]))
	 f.write ('"' + text + '",\n')
	text = "".join(map(Raster2grid,dat_matrix[band.YSize - 1,:]))
        f.write ('"' + text + '"\n')
	f.write('],\n')
	######## keys書き込み
	text = '","'.join(map(str, keys))
	f.write('"keys":["' + text + '"],\n')
	f.close
	######## data書き込み
	f = codecs.open(jsonfile, "a")###utf-8で開くと凡例の日本語処理をした関係で上手くいかないため。
	data = dict((value, key) for key, value in invdata.iteritems()) ##ハッシュキーと値を入れ替え
	text = ','.join(map(Keys2data,keys))
	f.write('"data":{' + text + '}\n')
	f.write('}')
	f.close()

def RGBtile2json(file):
	global data
	_root,_ext = os.path.splitext(file)
        jsonfile = _root + ".json"

	dataset = gdal.Open(file, gdalconst.GA_ReadOnly)
	bandR    = dataset.GetRasterBand(1)
	bandG    = dataset.GetRasterBand(2)
	bandB    = dataset.GetRasterBand(3)
	dat_matrixR = bandR.ReadAsArray()
        dat_matrixG = bandG.ReadAsArray()
        dat_matrixB = bandB.ReadAsArray()

	f = codecs.open(jsonfile, "w",'utf-8')
	######## grid,keys,data作成、grid書き込み
	f.write('{"grid":[')
	for i in range(0,bandR.YSize - 2): #for last comma remove
	 text = "".join(map(RGBRaster2grid,dat_matrixR[i,:],dat_matrixG[i,:],dat_matrixB[i,:]))
	 f.write ('"' + text + '",\n')
	text = "".join(map(RGBRaster2grid,dat_matrixR[bandR.YSize - 1,:],dat_matrixG[bandR.YSize - 1,:],dat_matrixB[bandR.YSize - 1,:]))
        f.write ('"' + text + '"\n')
	f.write('],\n')
	######## keys書き込み
	text = '","'.join(map(str, keys))
	f.write('"keys":["' + text + '"],\n')
	f.close
	######## data書き込み
	f = codecs.open(jsonfile, "a")###utf-8で開くと凡例の日本語処理をした関係で上手くいかないため。
	data = dict((value, key) for key, value in invdata.iteritems()) ##ハッシュキーと値を入れ替え
	#print "#####\n"
	#print data
	text = ','.join(map(Keys2data,keys))
	f.write('"data":{' + text + '}\n')
	f.write('}')
	f.close()

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])


def usage():
    print 'Usage: # tile2utfgrid dir [csv type("color"|"raster")]'
    quit()

################### main #########################
#
# タイルのルートディレクトリと凡例ファイルを引数にして実行
# "使い方"
# python tile2utfgrid.py tiledir legend.csv type("color"|"raster")
#
# ※tiledirはXYZ(TMSではない)、legend.csvの文字コードはutf-8
##################################################
legend={}
type = "raster"

argc = len(sys.argv)
if(argc < 2):
 usage()
search_root = sys.argv[1]

##凡例ファイルがある場合
if(argc == 4):
 legend_csv = sys.argv[2]
 type = sys.argv[3]
 csvfile = UnicodeDictReader(open(legend_csv,'rb'))
 ##凡例をラスタ値で判定する場合
 if(type=="raster"):
  for row in csvfile:
   legend[float(row['raster'])]=row
 ##凡例を色で判定する場合
 elif(type=="color"):
  for row in csvfile:
   Rs = row['R'].split("-")
   Gs = row['G'].split("-")
   Bs = row['B'].split("-")
   if len(Rs)==1:
    Rs.append(Rs[0])
   if len(Gs)==1:
    Gs.append(Gs[0])
   if len(Bs)==1:
    Bs.append(Bs[0])
   for R in range(int(Rs[0]),int(Rs[1])):
    for G in range(int(Gs[0]),int(Gs[1])):
     for B in range(int(Bs[0]),int(Bs[1])):
   	legend[str(R)+str(G)+str(B)]=row
 else:
  usage()
elif(argc != 2):
 usage()
  
for root,dirs,files in os.walk(search_root):
 print root
 for name in files:
  _root,_ext = os.path.splitext(name)
  abs_name = os.path.join(root,name)
  if(_ext == ".tif" and type=="raster"):
    tile2json(abs_name)
  elif(_ext == ".png" and type=="color"):
    RGBtile2json(abs_name)