<?php
echo "got called";

if(isset($_POST['color1']) && isset($_POST['color2']) && isset($_POST['color3']) && isset($_POST['color4']) && isset($_POST['color5']) && isset($_POST['color6']) && isset($_POST['color7']) && isset ($_POST['color8']) && isset($_POST['color9']) && isset($_POST['color10'])) {
  $controlByte = 0x00;
  if(isset($_POST['fadein'])) { $controlByte = 0x02; }
  if(isset($_POST['blinking'])){ $controlByte = $controlByte & 0x01; }
  $data = '';
  $data = chr(1);
  $data .= chr($controlByte); 
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
  $ret = file_put_contents('/home/pi/code/control/data.txt', $data);
  if($ret === false) {
    die('error writing data.txt file');
  }
  exec('python /home/pi/code/control/loader.py -f /home/pi/code/control/data.txt -l DEBUG', $output, $return);
  if ($return) { echo "success to call loader"; }
  else { echo "failure to call loader"; }
}
else {
  die('form is not complete');
}

header("Location: http://192.168.1.87/index.html")
?>
