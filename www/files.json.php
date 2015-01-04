<?php

	$dir          = "img/";
	$return_array = array();

	if(is_dir($dir)){
	    if($dh = opendir($dir)){
	        while(($file = readdir($dh)) != false){
	            if($file != "." && $file != ".."){
	                $return_array[] = $file; // Add the file to the array
	            }
	        }
	    }
	}
	
	echo json_encode($return_array);

?>