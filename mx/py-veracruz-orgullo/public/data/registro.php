<?php

#: Helper
#: =============================================================================

    function get_json_response($eid, $eme, $res="", $die=true){
        header('Cache-Control: no-cache, must-revalidate');
        header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
        header('Content-type: application/json');
        
        $result = array(
            'error' => array(
                'id' => $eid,
                'message' => $eme 
            ),
            'response' => $res
        );
        
        echo json_encode($result);

        if($die){
            die();
                
        }
    }

    $isPost = (sizeof($_POST) > 0);

#: Actions (proxy)
#: =============================================================================

    if(!$isPost){
        get_json_response(1, 'El método es incorrecto.');

    }else if(!isset($_POST["recaptcha_response_field"])){
        get_json_response(1, 'No se enviaron los parámetros del CAPTCHA.');

    }

    require_once ("recaptchalib.php");
    $publickey = "6LfepdsSAAAAAHrEWqqAgSHj2Xy8MZsgtoMz9gBo";
    $privatekey = "6LfepdsSAAAAACzG3wLYZeUFUZ9lPNAx4091NKIb";

    $resp = recaptcha_check_answer(
        $privatekey, 
        $_SERVER["REMOTE_ADDR"], 
        $_POST["recaptcha_challenge_field"], 
        $_POST["recaptcha_response_field"]
    );

    if(!$resp->is_valid){
        get_json_response(1, 'El CAPTCHA es incorrecto.');

    }

    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL,'http://127.0.0.1/register');
    curl_setopt($curl, CURLOPT_PORT, 8001);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_TIMEOUT, 0);
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLINFO_HEADER_OUT, true);

    $vars = '';

    foreach($_POST as $key => $value) {
        $vars .= $key.'='.$value.'&';

    }

    $vars = substr($vars,0,strlen($vars)-1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $vars);
    curl_setopt($curl, CURLOPT_POST, 1);

    $result = curl_exec($curl);

    if(curl_errno($curl)){
        get_json_response(1, curl_error($curl), '', false);

    }else{
        echo $result;

    }

    curl_close($curl);

?>