<?php
$conn  = mysqli_connect("localhost:23306","wdj","wdj654321");
if (!$conn)
	die('Failing to connect database '.mysqli_connect_error());


$type = $_GET['type'];
if (!$type){
	$type = 1;
}
// echo "type is ".$type;
$data = ['money<1001', 'money>1000 and money<1501', 
		 'money>1500 and money<2001', 'money>2000 and money<3001','money>3000'];
$sql = "select id, url, money, lnglat from rent58 where ".$data[$type-1];
mysqli_select_db($conn, 'rent58');
mysqli_set_charset($conn,'utf8');
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_all($result);
// echo $sql;
echo json_encode($row);
mysqli_close($conn);