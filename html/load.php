<?php
$proj = new PDO('mysql:host=172.28.100.14;port=3306;dbname=Project', 'chat', ']weCRJnL84');


$idprod = $_POST['idprod']; //Receiving selected product id

if (!empty($_POST['idmag'])) {
    $idmag = "AND idMagasin = " . $_POST['idmag'];
} else {
    $idmag = "";
};

if (!empty($_POST['chart'])) {
    $chart_type = 'counts';
} else {
    $chart_type = 'prices';
};
$qrel = $proj->query("SELECT * FROM `Relations` WHERE carrefour = " . $idprod . " OR chronodrive = " . $idprod); //
$query1 = $proj->query("SELECT DISTINCT(DATE_FORMAT(date, '%Y%m%d')) as ladate, enseigne, AVG(Prix) as prixmoyen, COUNT(DISTINCT idArticle,date,enseigne,Prix) as volume FROM `Relevés` WHERE idArticle = " . $idprod . " " . $idmag . " GROUP BY ladate, enseigne");
// while ($resp=$query->fetch()) {
//  echo("\n".$resp[0]." ".$resp[1]);
// };

$result1 = $query1->fetchAll();
// SELCT id In Relations 
foreach ($result1 as $row) {
    // settype($row[0],"integer");
    settype($row[2], "float");
    $dates[] = $row[0];
    $prix[] = round($row[2], 2);
    $enseigne = $row[1];
    $comptes[] = $row[3];
    //  [(int)$row->ladate,(float)$row->prixmoyen];
}

$dates = json_encode($dates);
$prix = json_encode($prix);
$comptes = json_encode($comptes);
if ($enseigne == 'Carrefour') {
    $chart_col = "#89D1FE";
    $enseigne2 = 'Chronodrive';
} else {
    $chart_col = "#DE1738";
    $enseigne2 = 'Carrefour';
}

if ($qrel->rowCount() > 0) {
    $rel = $qrel->fetch();

    if ($enseigne == 'Carrefour') {
        $id2 = $rel[1];
        $chart_col = "#89D1FE";
        $chart_col2 = "#DE1738";
    } else {
        $id2 = $rel[2];
        $chart_col = "#DE1738";
        $chart_col2 = "#89D1FE";
    }

    if ($idmag == "") {
        $query2 = $proj->query("SELECT DISTINCT(DATE_FORMAT(date, '%Y%m%d')) as ladate, enseigne, AVG(Prix) as prixmoyen, COUNT(DISTINCT idArticle,date,enseigne,Prix) as volume FROM `Relevés` WHERE idArticle = " . $id2 . " GROUP BY ladate, enseigne");
        $result2 = $query2->fetchAll();
        // SELCT id In Relations 
        foreach ($result2 as $row) {
            // settype($row[0],"integer");
            settype($row[2], "float");
            $dates2[] = $row[0];
            $prix2[] = round($row[2], 2);
            $enseigne2 = $row[1];
            $comptes2[] = $row[3];
            //  [(int)$row->ladate,(float)$row->prixmoyen];
        }
        $dates2 = json_encode($dates2);
        $prix2 = json_encode($prix2);
        $comptes2 = json_encode($comptes2);
    };
};

$mags = $proj->query("SELECT enseigne,ville,id FROM `Magasins` where id IN (SELECT idMagasin from `Relevés` WHERE idArticle = " . $idprod . ")"); // Run your query
$resultMags = $mags->fetchAll();
foreach ($resultMags as $row) {
    // settype($row[0],"integer");
    $maglist[] = [$row[0], $row[1], $row[2]];
}

$maglist = json_encode($maglist);
?>

<!-- Indicators (avg price)-->
<div id="indicators">
    <div id="div_carrefour" class="div_mag">
        <p>Carrefour</p>
        <div class="kpi_mags">
            <span id="Carrefour_ind"></span>€
        </div>
    </div>
    <div id="div_chronodrive" class="div_mag">
        <p>Chronodrive</p>
        <div class="kpi_mags">
            <span id="Chronodrive_ind"></span>€
        </div>
    </div>
</div>

<!-- Change chart type button -->
<button id='button_chart' value='count'>Afficher le compte</button>

<!-- Div containing the chart -->
<div id='chart-container' style=''>
    <canvas id="line-chart" width="400" height="100"></canvas>&nbsp
</div>
<script src="package/dist/Chart.js"></script>
<script type="text/javascript">
    console.log([<?php echo ($dates); ?>])

    $("#button_chart").click(function() {
        console.log($(this).val())
        var btn_option = $(this).val()
        if (btn_option == 'count') {
            addData(config, 'Nombre de relevés', [<?php echo ($comptes);
                                                    if (!empty($comptes2)) {
                                                        echo (',');
                                                        echo ($comptes2);
                                                    } ?>]);
            $(this).val('prix');
            $(this).html('Afficher le prix')
        } else if (btn_option == 'prix') {
            addData(config, 'Prix moyen relevé (€)', [<?php echo ($prix);
                                                        if (!empty($prix2)) {
                                                            echo (',');
                                                            echo ($prix2);
                                                        } ?>]);
            $(this).val('count');
            $(this).html('Afficher le compte')
        }

    });

    function addData(chart, label, data) {
        //     chart.data.datasets.forEach((dataset) => {
        //     dataset.data.pop();
        // });
        console.log(data)
        i = 0
        chart.options.title.text = label
        chart.data.datasets.forEach((dataset) => {

            console.log(data[i])
            dataset.data = data[i];
            console.log(i)
            i += 1
        });
        new Chart(document.getElementById("line-chart"), config)
    }



    //             if (isset($prix2)) {
    //                 echo (",{
    //                     data: " . $prix2 . ",
    //                     steppedLine: true,
    //                     label: '" . $enseigne2 . "',
    //                     borderColor: '" . $chart_col2 . "',
    //                     lineTension:0,
    //                     fill:false
    //                 }");
    //             }; 

    //         ]
    //     },
    //     options: {
    //         title: {
    //             display: true,
    //             offset: true,
    //             text: 'Prix moyen relevé (€)'
    //         }
    //     }
    // });
    console.log(<?php echo ($maglist); ?>)
    var magarray = <?php echo ($maglist); ?>;
    var config = {
        type: 'line',
        data: {
            labels: <?php echo ($dates); ?>,
            datasets: [{
                    data: <?php echo ($prix); ?>,
                    steppedLine: true,
                    label: "<?php echo ($enseigne); ?>",
                    borderColor: "<?php echo ($chart_col); ?>",
                    lineTension: 0,
                    fill: false
                }
                <?php
                if (isset($prix2)) {
                    echo (",{
                        data: " . $prix2 . ",
                        steppedLine: true,
                        label: '" . $enseigne2 . "',
                        borderColor: '" . $chart_col2 . "',
                        lineTension:0,
                        fill:false
                    }");
                }; ?>
            ]
        },
        options: {
            title: {
                display: true,
                offset: true,
                text: 'Prix moyen relevé (€)'

            }
        }
    };

    new Chart(document.getElementById("line-chart"), config)
    $('#<?php echo ($enseigne . "_ind"); ?>').html(parseFloat(average(<?php echo ($prix) ?>)).toFixed(2))
    <?php if (isset($prix2)) {
        echo ("$('#" . $enseigne2 . "_ind').html(parseFloat(average(" . $prix2 . ")).toFixed(2))");
    } else {
        echo ("$('#" . $enseigne2 . "_ind').html('0.00')");
    } ?>
    // $('#chronodrive_ind').html(parseFloat(average([2,3]).toFixed()
</script>