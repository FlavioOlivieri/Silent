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

$sql="SELECT nome,data_scadenza,prezzo,uso,nome_c,descrizione,".
                " quantita,nome_cf,citta_cf,via_cf,".
                " cap_cf,nome_f,via_f,citta_f,cap_f,numero_f".
                " FROM farmacia join venduto on (farmacia.id_farmacia=venduto.id_farmacia)".
                " join farmaco on (venduto.id_farmaco=farmaco.id_farmaco)".
                " join contiene on (farmaco.id_farmaco = contiene.id_farmaco)".
                " join componente on (contiene.id_componente=componente.id_componente)".
                " join casa_farmaceutica on (farmaco.id_casa_farmaceutica=casa_farmaceutica.id_casa_farmaceutica)".
                " WHERE farmaco.nome LIKE '%".$var_db."%';";
                                                                                                                                                                                                                                             $result=mysqli_query($con,$sql);                                                                                                                                                                                                             if(mysqli_num_rows($result) != "0")                                                                                                                                                                                                          {
        while($rs=mysqli_fetch_array($result,MYSQLI_ASSOC)){
                $json[]=$rs;
        }

        echo json_encode($json,JSON_UNESCAPED_UNICODE);
        mysqli_free_result($result);
        mysqli_close($con);
}
?>