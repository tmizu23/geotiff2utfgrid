var dataSet1 = {
        0: null,1: null,2: null,3: null,4: null,
        5: {dataId: "RELIEF"},
        6: {dataId: "RELIEF"},
        7: {dataId: "RELIEF"},
        8: {dataId: "RELIEF"},
        9: {dataId: "BAFD1000K2"},
        10: {dataId: "BAFD1000K2"},
        11: {dataId: "BAFD1000K2"},
        12: {dataId: "BAFD200K2"},
        13: {dataId: "BAFD200K2"},
        14: {dataId: "BAFD200K2"},
        15: {dataId: "DJBMM"},
        16: {dataId: "DJBMM"},
        17: {dataId: "DJBMM"}
    };

var map = new OpenLayers.Map('map', {
    controls: [    
        new OpenLayers.Control.TouchNavigation({
            dragPanOptions: {
             enableKinetic: true
            }
        }),
        new OpenLayers.Control.Navigation(),
	new OpenLayers.Control.Attribution(),
	new OpenLayers.Control.LayerSwitcher(),
	new OpenLayers.Control.Permalink()],
    projection: new OpenLayers.Projection("EPSG:900913"), //明示しないとTMSが表示されない!
});
cjp_layer = new webtis.Layer.BaseMap("電子国土", {
    dataSet: dataSet1,
    transitionEffect: 'resize'
});
map.addLayer(cjp_layer);

//////植生//////////
syokusei_layer = new OpenLayers.Layer.XYZ("syokusei", "http://www.ecoris.co.jp/map/data/syokusei/${z}/${x}/${y}.png", {
    sphericalMercator: true,
    isBaseLayer: false,
    opacity: 0.6,
    attribution: "環境省第6,7回自然環境保全基礎調査"
});
map.addLayer(syokusei_layer);

//////植生utfgrid//////////
var syokusei_utfgrid_layer = new OpenLayers.Layer.UTFGrid({
    url: "http://www.ecoris.co.jp/map/data/syokusei/${z}/${x}/${y}.json",
    utfgridResolution: 1, // default is 2
    displayInLayerSwitcher: false
});
map.addLayer(syokusei_utfgrid_layer);

//////標高//////////
dem_layer = new OpenLayers.Layer.XYZ("dem", "http://www.ecoris.co.jp/map/data/dem/${z}/${x}/${y}.png", {
    sphericalMercator: true,
    isBaseLayer: false,
    opacity: 0.6,
    attribution: "国土地理院（承認番号 平22業使、第133号）"
});
map.addLayer(dem_layer);


//////標高utfgrid//////////
var dem_utfgrid_layer = new OpenLayers.Layer.UTFGrid({
    url: "http://www.ecoris.co.jp/map/data/dem/${z}/${x}/${y}.json",
    utfgridResolution: 1, // default is 2
    displayInLayerSwitcher: false
});
map.addLayer(dem_utfgrid_layer);

//////絵地図//////////
mymap_layer = new OpenLayers.Layer.XYZ("mymap", "http://www.ecoris.co.jp/map/data/mymap/${z}/${x}/${y}.png", {
    sphericalMercator: true,
    isBaseLayer: false,
    opacity: 1.0,
    attribution: "(c)エコリス",
    ///クライアントズーム 
    ///タイルはレベル16までだけど、serverResolutionsを指定することによって電子国土の最大17まで拡大できる。
     serverResolutions: [156543.03390625, 78271.516953125, 39135.7584765625,
        19567.87923828125, 9783.939619140625,
        4891.9698095703125, 2445.9849047851562,
        1222.9924523925781, 611.4962261962891,
        305.74811309814453, 152.87405654907226,
        76.43702827453613, 38.218514137268066,
        19.109257068634033, 9.554628534317017,
        4.777314267158508],
        transitionEffect: 'resize'
});
map.addLayer(mymap_layer);

//////絵地図utfgrid//////////
var mymap_utfgrid_layer = new OpenLayers.Layer.UTFGrid({
    url: "http://www.ecoris.co.jp/map/data/mymap/${z}/${x}/${y}.json",
    utfgridResolution: 1, // default is 2
    displayInLayerSwitcher: false
});
map.addLayer(mymap_utfgrid_layer);



var callback = function (infoLookup, loc, pixel) {
    var msg = "";
    if (infoLookup) {
        var info;
        for (var idx in infoLookup) {
            // idx can be used to retrieve layer from map.layers[idx]
            info = infoLookup[idx];
            if (info && info.data.HANREI_N) {//植生
                document.getElementById("utfgrid")
                    .innerText = info.data.HANREI_C + ":" +info.data.HANREI_N + "：" + info.data.DAI_N;
		return
            }
	    else if (info && info.data.NAME) {//絵地図
                document.getElementById("utfgrid")
                    .innerText = info.data.NAME + ":" +info.data.DESCRIPTION;
		return
            }
	    else if (info && info.data.V) {//凡例がない場合にはラスタ値を表示、標高
                document.getElementById("utfgrid")
                    .innerText = "ラスタ値（凡例なし）：" + info.data.V;
		return
            }
            else {
                document.getElementById("utfgrid")
                    .innerText = "";
            }
        }
    }
};

map.addControl(new OpenLayers.Control.UTFGrid({
    callback: callback,
    handlerMode: "move"
}));


///////Permalinkを有効にするためコメントアウト
//map.setCenter(new OpenLayers.LonLat(141.46, 39.6).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 11);