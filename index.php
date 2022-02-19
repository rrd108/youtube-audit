<?php
function generateData($type, $exclude)
{
    $youtubers = [];
    $fileName = $type == 'subs' ? 'Subscribers' : 'Views';
    if (($handle = fopen('./analytics' . $fileName . '.csv', 'r')) !== false) {
        while (($data = fgetcsv($handle, 1000, ',')) !== false) {
            if (in_array($data[0], $exclude)) {
                continue;
            }
            foreach ($data as $i => $d) {
                if ($i > 0) {
                    $youtubers[$data[0]][] = ['x' => $i, 'y' => (int) $d];
                }
            }
        }
        fclose($handle);
    }

    // sort by subscribers descending
    uasort($youtubers, function ($a, $b) {
        return end($b)['y'] <=> end($a)['y'];
    });
    return $youtubers;
}


$exclude = [];
$youtubersSubs = generateData('subs', $exclude);
$youtubersViews = generateData('views', $exclude);



?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prédikátorok</title>
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js" defer></script>
    <script>
        const defaults = {
            animationEnabled: true,
            theme: "light2",
            legend: {
                cursor: "pointer",
                verticalAlign: "top",
                horizontalAlign: "center",
                dockInsidePlotArea: true,
                fontSize: 12,
            },
            toolTip: {
                shared: true
            }
        }

        window.onload = () => {
            const chartViews = new CanvasJS.Chart("chartContainerViews", {
                ...defaults,
                title: {
                    text: "M Views",
                    fontSize: 16,
                },
                data: [<?php
                        foreach ($youtubersViews as $youtuber => $data) {
                            echo '{
                    type: "line",
                    axisYType: "secondary",
                    name: "' . $youtuber . '",
                    showInLegend: true,
                    markerSize: 0,
                    dataPoints: JSON.parse(\'' . json_encode($data) . '\')
                },';
                        }
                        ?>]
            });
            chartViews.render();

            const chartSubs = new CanvasJS.Chart("chartContainerSubs", {
                ...defaults,
                title: {
                    text: "Subscribers",
                    fontSize: 16,
                },
                data: [<?php
                        foreach ($youtubersSubs as $youtuber => $data) {
                            echo '{
                    type: "line",
                    axisYType: "secondary",
                    name: "' . $youtuber . '",
                    showInLegend: true,
                    markerSize: 0,
                    dataPoints: JSON.parse(\'' . json_encode($data) . '\')
                },';
                        }
                        ?>]
            });
            chartSubs.render();
        }
    </script>
</head>

<body>
    <div id="chartContainerViews" style="height: 670px; width: 100%;"></div>
    <div id="chartContainerSubs" style="height: 670px; width: 100%;"></div>
</body>

</html>