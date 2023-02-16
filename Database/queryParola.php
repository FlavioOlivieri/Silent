<?php
$var_db="";
$filename="parola_trovata.txt";
$file=fopen($filename,"r") or die("Impossibile aprire il file");
while(!feof($file))
{
        $var_db = fread($file,1024); //1024 è il numero massimo di byte da leggere
}
fclose($file);

$var_db = str_replace(array("\n"), "", $var_db);

$con=mysqli_connect("127.0.0.1","silent","silent","silentDB");
mysqli_set_charset($con,"utf8");

$sql="SELECT nome FROM farmaco WHERE farmaco.nome LIKE '%".$var_db."%';";

$result=mysqli_query($con,$sql);
if(mysqli_num_rows($result) != "0")
{
        while($rs=mysqli_fetch_array($result,MYSQLI_ASSOC)){
                $json[]=$rs;
        }

        echo json_encode($json,JSON_UNESCAPED_UNICODE);                                                                                                                                                                                              mysqli_free_result($result);                                                                                                                                                                                                                 mysqli_close($con);                                                                                                                                                                                                                  }
else
{
        $str[] = array('parola' => $var_db);
        echo json_encode($str,JSON_UNESCAPED_UNICODE);
        mysqli_close($con);
}
?>