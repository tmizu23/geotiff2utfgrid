GeoTiff2UTFGrid
======================
GeoTiffをUTFGridに変換するプログラムです。  
試しに作ってみました。

作成例
------
標高の例
http://www.ecoris.co.jp/map/utfgrid_test.html?zoom=13&lat=4823548.9824&lon=15744694.52498&layers=BTTTTTT

植生の例
http://www.ecoris.co.jp/map/utfgrid_test.html?zoom=13&lat=4799872.6129&lon=15744694.52498&layers=BTTTTTT

絵地図の例
http://www.ecoris.co.jp/map/utfgrid_test.html?zoom=16&lat=4607129.48013&lon=15683405.16591&layers=BTTTTTT

プログラム
------
- `gdal2tilesXYZ1band.py`  
 1バンドのGeoTIFFを1バンドのXYZタイルに変換します。gdal2tilesは強制的に3バンドに変換するので、1バンドのデータをそのまま1バンドのままタイルにします。また、その際にTMS形式ではなくXYZ形式で出力します。
- `gdal2tilesXYZ.py`  
 3バンドのGeoTIFFを3バンドのXYZタイルに変換します。gdal2tilesの出力はTMS形式なので、それをXYZ形式にしたものです。ただし、gdal2tilesが出力するメタデータやhtmlは出力しません。
- `tile2utfgrid.py`  
 タイル画像からUTFGridファイル(.json)を作成します。
- `tile2utfgrid.bat`  
 OSGeo4Wのためのファイルです。上記プログラムを呼び出すだけです。
- `gdal2tilesXYZ1band.bat`  
 OSGeo4Wのためのファイルです。上記プログラムを呼び出すだけです。
- `gdal2tilesXYZ.bat`  
 OSGeo4Wのためのファイルです。上記プログラムを呼び出すだけです。

使い方
------
### インライン ###
インラインのコードは、**バッククォート** (`` ` ``) で囲みます。
 
### ブロックレベル ###
    function f () {
        alert(0);  /* 先頭に4文字のスペース、
                      もしくはタブを挿入します */
    }
 
パラメータの解説
----------------
リストの間に空行を挟むと、それぞれのリストに `<p>` タグが挿入され、行間が
広くなります。
 
    def MyFunction(param1, param2, ...)
 
+   `param1` :
    _パラメータ1_ の説明
 
+   `param2` :
    _パラメータ2_ の説明
 
関連情報
--------
### リンク、ネストしたリスト
1. [リンク1](http://example.com/ "リンクのタイトル")
    * ![画像1](http://github.com/unicorn.png "画像のタイトル")
2. [リンク2][link]
    - [![画像2][image]](https://github.com/)
 
  [link]: http://example.com/ "インデックス型のリンク"
  [image]: http://github.com/github.png "インデックス型の画像"
 
### 引用、ネストした引用
> これは引用です。
>
> > スペースを挟んで `>` を重ねると、引用の中で引用ができますが、
> > GitHubの場合、1行前に空の引用が無いと、正しくマークアップされません。
 
ライセンス
----------
Copyright &copy; 2011 xxxxxx
Licensed under the [Apache License, Version 2.0][Apache]
Distributed under the [MIT License][mit].
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html