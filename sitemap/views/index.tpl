<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>SiteMapper</title>
    <link href="https://fonts.googleapis.com/css2?family=Russo+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="http://cdn.graphalchemist.com/alchemy.min.css"/>

</head>
<body>
    <div class="main">

        <h1>SiteMapper</h1>
        <form action="/generate" method="POST">
            <div>
                <label for="url">URL:</label>
                <input type="text" class="form-control" id="url" name="url"/>
            </div>
            <div class="checkbox">
                <input id="firstPageOnly" type="checkbox"  name="firstPageOnly"/>
                <label>Run only for first page</label>
            </div>
            <div class="checkbox">
                <input id="isSpa" type="checkbox"  name="isSpa"/>
                <label>Is site SPA or use reactive framework ?</label>
            </div>
            <div>
                <button id="generateBtn" type="submit">Generate</button>
            </div>
        </form>
        <div>
            <textarea id="raw"></textarea>
        </div>
    </div>

    <div class="wrapper">
        <svg width="1024" viewbox="0,0,1200,800" height="900" id="mountNosde"></svg>
    </div>
    <div id="container">
    </div>

</body>
    <script src="https://d3js.org/d3.v4.js"></script>
    <script type="application/javascript" src="/static/js/script.js"></script>
</html>