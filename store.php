<?php

$myfile = fopen("location.txt" , "w");
$txt = "Jane Doe\n";
fwrite($myfile, $txt);
fclose($myfile);

?>
