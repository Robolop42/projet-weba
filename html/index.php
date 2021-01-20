<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="styles/chat.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" async>
    <title>Relevé Drive</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js" async></script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
    <div id='content'>
        <?php
        session_start();

        try {
            #PDO of the database containing scrapped data
            $proj = new PDO('mysql:host=172.28.100.14;port=3306;dbname=Project', 'chat', ']weCRJnL84');
        } catch (Exception $e) {
            die('Erreur : ' . $e->getMessage());
        }

        if (isset($_POST['logout'])) {
            session_destroy();
            header("Location: /index.php");
        }

        ?>

            <?php
            // include("header.php");
            if (isset($_SESSION['name'])) {
                echo ('<div id="top-header"><span id="hello">&#x1F44B Hello '.$_SESSION['name'].'</span>');
                echo("<form action='logging.php' method='post'>
                <input type='submit' value='logout' name='logout'>
            </form></div>");
            } else {header('Location: logging.php');}
            ?>
        <?php
        //Querying products table to get products info
        $query = $proj->query("SELECT id,nom FROM `Produits` WHERE (nom != 'shimmer') AND (nom LIKE '%bonduelle%')"); // Run your query

        echo '<select id="produit" name="produits">'; #Opening the select element 

        #Genereating an option for each query result 
        while ($row = $query->fetch()) {
            echo '<option value="' . $row[0] . '">' . $row[1] . '</option>'; #row[0]=product id; row[1]=product name
        }

        echo '</select>'; #Closing the select element
        ?>

        <div id="selectMag">
            <select id="magasins">
                <option value="" selected="selected">Tous les magasins</option> <!-- List of mags will be appended here -->
            </select>
        </div>
        <!--This div will receive the load.php content -->
        <div id="target"></div>
    </div>
</body>



<script src="package/dist/Chart.js"></script>
<script type="text/javascript">

    // AJAX call to load.php to get content
    var idprod = "";
    var idmag = "";
    $("select")
        .change(function() {
            $("select option:selected").each(function() {
                if ($("#produit").val() !== idprod) {
                $('#magasins').val("");}
                idprod = $("#produit").val(); //idprod get the 'produit' selected value
                idmag = $("#magasins").val();

                // Ajax call to load.php
                $.ajax({
                    type: "POST",
                    url: "load.php",
                    data: {
                        'idprod': idprod,
                        'idmag': idmag //Posting the id of the selected product
                    },
                    success: function(data) {
                        $('#target').html(data) //Appending load.php content to the target div
                        magarray.forEach(function(item, index, array) {
                            var opt = document.createElement('option');
                            opt.value = item[2];
                            opt.innerHTML = item[0] + " " + item[1];
                            $("#magasins").append(opt);
                            // recursiveAjax()
                        });
                    },
                    // Alert status code and error if fail
                    error: function(xhr, ajaxOptions, thrownError) {
                        alert(xhr.status);
                        alert(thrownError);
                    }
                });
            });
        })
        .trigger("change");
        

    // Small function to compute the average of an array
    // From https://stackoverflow.com/questions/10359907/how-to-compute-the-sum-and-average-of-elements-in-an-array
    const average = arr => arr.reduce((p, c) => p + c, 0) / arr.length;
</script>

</html>