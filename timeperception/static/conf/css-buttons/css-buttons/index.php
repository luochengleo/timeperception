<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Papermashup.com | jQuery PHP Page Scape</title>
<link href="../style.css" rel="stylesheet" type="text/css" />  


<style>

#dark{
	background-color:#333;
	border:1px solid #000;
	padding:10px;
	margin-top:20px;}
	
#light{
	background-color:#FFF;
	border:1px solid #dedede;
	padding:10px;
	margin-top:20px;}	
	
li{ 
list-style:none;
	padding-top:10px;
	padding-bottom:10px;}	

.button, .button:visited {
	background: #222 url(overlay.png) repeat-x; 
	display: inline-block; 
	padding: 5px 10px 6px; 
	color: #fff; 
	text-decoration: none;
	-moz-border-radius: 6px; 
	-webkit-border-radius: 6px;
	-moz-box-shadow: 0 1px 3px rgba(0,0,0,0.6);
	-webkit-box-shadow: 0 1px 3px rgba(0,0,0,0.6);
	text-shadow: 0 -1px 1px rgba(0,0,0,0.25);
	border-bottom: 1px solid rgba(0,0,0,0.25);
	position: relative;
	cursor: pointer
}
 
	.button:hover							{ background-color: #111; color: #fff; }
	.button:active							{ top: 1px; }
	.small.button, .small.button:visited 			{ font-size: 11px}
	.button, .button:visited,
	.medium.button, .medium.button:visited 		{ font-size: 13px; 
												  font-weight: bold; 
												  line-height: 1; 
												  text-shadow: 0 -1px 1px rgba(0,0,0,0.25); 
												  }
												  
	.large.button, .large.button:visited 			{ font-size: 14px; 
													  padding: 8px 14px 9px; }
													  
	.super.button, .super.button:visited 			{ font-size: 34px; 
													  padding: 8px 14px 9px; }
	
	.pink.button, .magenta.button:visited		{ background-color: #e22092; }
	.pink.button:hover							{ background-color: #c81e82; }
	.green.button, .green.button:visited		{ background-color: #91bd09; }
	.green.button:hover						    { background-color: #749a02; }
	.red.button, .red.button:visited			{ background-color: #e62727; }
	.red.button:hover							{ background-color: #cf2525; }
	.orange.button, .orange.button:visited		{ background-color: #ff5c00; }
	.orange.button:hover						{ background-color: #d45500; }
	.blue.button, .blue.button:visited		    { background-color: #2981e4; }
	.blue.button:hover							{ background-color: #2575cf; }
	.yellow.button, .yellow.button:visited		{ background-color: #ffb515; }
	.yellow.button:hover						{ background-color: #fc9200; }
		</style> 



</head> 
	<body> 
	
    
    <?php include '../includes/header.php';
        $link = '| <a href="http://papermashup.com/pretty-css3-buttons/">Back To Tutorial</a>';
?>
    
    
 <div id="light">  		
       <ul>
        <li><a class="super button pink">Pink Button</a>
        <a class="large button green">Green Button</a></li>
       <li> <a class="large button blue">Blue Button</a>
        <a class="large button red">Red Button</a></li>
        <li><a class="large button orange">Orange Button</a>
        <a class="large button yellow">Yellow Button</a></li>
        </ul>
 </div>       
        
 <div id="dark">       
        <ul>
        <li><a class="super button pink">Pink Button</a>
        <a class="large button green">Green Button</a></li>
       <li> <a class="medium button blue">Blue Button</a>
        <a class="large button red">Red Button</a></li>
       <li> <a class="small button orange">Orange Button</a>
        <a class="medium button yellow">Yellow Button</a></li>
        </ul>
</div>     
      
      
      
        
        

<?php include '../includes/footer.php';?>

	</body> 
</html> 