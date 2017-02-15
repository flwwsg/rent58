<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />

	<title>map</title>
	<style type="text/css">
		body, html{width: 100%;height: 100%;margin:0;font-family:"微软雅黑";}
		#l-map{height:90%;width:100%;}
	</style>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=7r5lNHNGvNja5KPYAfQRfTafFrVYZXrV"></script>
	<script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>

</head>
<body>
	<div id="l-map"></div>
	<div id="r-result">
		<input type="button" value="<1001" onclick="sendAjax(1)" />
		<input type="button" value="<1501" onclick="sendAjax(2)" />
		<input type="button" value="<2001" onclick="sendAjax(3)" />
		<input type="button" value="<3001" onclick="sendAjax(4)" />
		<input type="button" value=">3000" onclick="sendAjax(5)" />

	</div>
</body>
</html>
<script type="text/javascript">
	// 百度地图API功能
	var map = new BMap.Map("l-map");
	map.centerAndZoom(new BMap.Point(121.5485476569462,31.252018949493948), 13);
	map.enableScrollWheelZoom(true);
	var opts = {
		title : "detail infomation" , // 信息窗口标题
		enableMessage:true//设置允许信息窗发送短息
	  };
	var myGeo = new BMap.Geocoder();
	$(document).ready(sendAjax(1));
	function drawmap( data){
		map.clearOverlays()

		for (var i = 0; i < data.length; i++) {
			record = data[i];
			lnglat = record[3];
			if(!lnglat){
				continue;
			}
			lnglat = lnglat.split(',');
			id = record[0];
			url = record[1];
			money = record[2];
			point = new BMap.Point(lnglat[0], lnglat[1])
			var marker = new BMap.Marker(point);
			map.addOverlay(marker);
			marker.setLabel(new BMap.Label('money '+money,{offset:new BMap.Size(20,-10)}));
			link = '<a href="'+url+'" target="_blank">link</a>';
			addClickHandler(link,marker);
		}

	}

	function addClickHandler(content,marker){
		marker.addEventListener("click",function(e){
			openInfo(content,e)}
		);
	}

	function openInfo(content,e){
		var p = e.target;
		var pt = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
		myGeo.getLocation(pt, function(rs){
			var addComp = rs.addressComponents;
			var addr = "商圈(" + rs.business + ")<br />(" + addComp.province + ", " + addComp.city + ", " + addComp.district + ", " + addComp.street + ", " + addComp.streetNumber + ")<br />";
			var infoWindow = new BMap.InfoWindow(addr + content,opts);  // 创建信息窗口对象 
			map.openInfoWindow(infoWindow,pt); //开启信息窗口
		});
	}

	function sendAjax(dtype){
		var url = 'updatearea.php?type='+dtype;
		$.ajax({
			url:url,
			type:'GET',
			data:'',
			dataType:'json',
			success: function(data){
			  drawmap(data)
			}
		});
	  
	}
		
	
</script>