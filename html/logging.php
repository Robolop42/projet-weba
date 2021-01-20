<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="styles/chat.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" async>
    <title>Connexion</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js" async></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <?php
    session_start();
    try {
        #PDO of the database containing user informations
        $base = new PDO('mysql:host=172.28.100.14;port=3306;dbname=Project', 'chat', ']weCRJnL84');
    } catch (Exception $e) {
        die('Erreur : ' . $e->getMessage());
    }

    $log = isset($_POST['name']) ? $_POST['name'] : NULL;
    $pass = isset($_POST['password']) ? $_POST['password'] : NULL;



    #querying user table with logging info
    $sql = "SELECT * FROM `usertable` WHERE (login='$log');";
    $reponse = $base->query($sql);
    $donnees = $reponse->fetch();
    if (is_array($donnees)) #If response
    {
        if (password_verify($pass, $donnees['password'])) #AND password verified
        {
            $_SESSION['name'] = $log;
            header('Location: index.php'); #Creating a session for the user
        } else {
            $password_incorrect = True;
        }
    } elseif (isset($_POST['connect'])) {
        $username_incorrect = True;
    }

    echo ("<div id='logging'><div id='form' class=''>
        <form action='' method='post'>
            <label>Connexion</label><br>
            <input type='text' name='name'>");
    if (isset($username_incorrect)) {
        echo (' username incorrect');
    }
    echo ("<br>
            <input type='password' name='password'>");
    if (isset($password_incorrect)) {
        echo (' password incorrect');
    }
    echo ("<br>
            <input type='submit' name='connect' value='Se connecter'>
        </form>
        </div>");

    $reponse->closeCursor(); ?>
</body>