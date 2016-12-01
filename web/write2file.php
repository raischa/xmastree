<?php

if(isset($_POST['color1']) && isset($_POST['color2']) && isset($_POST['color3']) && isset($_POST['color4']) && isset($_POST['color5']) && isset($_POST['color6']) && isset($_POST['color7']) && isset ($_POST['color8']) && isset($_POST['color9']) && isset($_POST['color10'])) {
  $controlByte = 0;
  if(isset($_POST['play'])) {
    $playVal = $_POST['play'];
    if($playVal == 'blinking') { 
      $controlByte = $controlByte | 1;
    } else if($playVal == 'pulsing') { 
      $controlByte = $controlByte | 2;
    }
  }
  if(isset($_POST['entry'])) {
    $entryVal = $_POST['entry'];
    if($entryVal == 'fadein') { 
      $controlByte = $controlByte | 16;
    } else if($entryVal == 'roll') { 
      $controlByte = $controlByte | 32;
    } else if($entryVal == 'inout') { 
      $controlByte = $controlByte | 48;
    } else if($entryVal == 'random') { 
      $controlByte = $controlByte | 64;
    } 
  }
 
  $data = '';
  $data = $data . pack("C",0x01);
  $data = $data . pack("C",$controlByte); 
  $data = $data . pack("H*",$_POST['color1']);
  $data = $data . pack("H*",$_POST['color2']);
  $data = $data . pack("H*",$_POST['color3']);
  $data = $data . pack("H*",$_POST['color4']);
  $data = $data . pack("H*",$_POST['color5']);
  $data = $data . pack("H*",$_POST['color6']);
  $data = $data . pack("H*",$_POST['color7']);
  $data = $data . pack("H*",$_POST['color8']);
  $data = $data . pack("H*",$_POST['color9']);
  $data = $data . pack("H*",$_POST['color10']);
  $data = $data . "\n";
  $ret = file_put_contents('/var/www/html/data.dat', $data);
  if($ret === false) {
    die('error writing data.txt file');
  }
  exec('sudo python /var/www/html/loader.py -f /var/www/html/data.dat', $output, $return);
  if ($return) { echo "success to call loader"; }
  else { echo "failure to call loader"; }
}
else {
  die('form is not complete');
}

header("Location: http://192.168.1.87/index.html")
?>
