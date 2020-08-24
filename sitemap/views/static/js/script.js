const SiteMap = {};

/**
 * @param e: Event
 * Overrided submit event for form
 */
SiteMap.onsubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const response = await fetch(form.getAttribute('action'), {
        method: "POST",
        body: JSON.stringify({
            firstPage: form.firstPageOnly.checked,
            url: form.url.value,
            isSpa: form.isSpa.value
        }),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    SiteMap.longPolling(await response.json())

}
/**
 * Use long polling as we should fetch results from celery
 * (Can use websockets instead)
 * @param json
 */
SiteMap.longPolling = (json) => {
    const uuid = json.uuid
    SiteMap.interval = setInterval(async () => {
        const response = await fetch("/" + uuid);
        SiteMap.result = (await response.json());
        if (SiteMap.result.status === 'SUCCESS') {
            clearInterval(SiteMap.interval);
            SiteMap.buildGraph(SiteMap.result.results);
            SiteMap.showRaw();
        }
    }, 2000)
}

/**
 * Show response as json in textarea
 */
SiteMap.showRaw = () => {
    const textarea = document.getElementById('raw');
    textarea.style.display = 'block';
    textarea.value = JSON.stringify(SiteMap.result.results);
}

/**
 * We hide wrapper at first to avoid blank space, show it after click
 */
SiteMap.showWrapper = () => {
    const wrapper = document.querySelector('.wrapper');
    wrapper.style.display = "block";
}

/**
 * Change the structure from response to pass it to d3
 * @param json
 */
SiteMap.buildStructureForD3 = (json) => {
    clearInterval(SiteMap.interval);
    const nodesData = json.map(node => {
        return {
            id: node.page, label: node.page, group: 1,
        };
    });


    const edgesData = [];
    json.forEach(node => {
        node.links.forEach(link => {
            if (nodesData.findIndex(node => node.id === link) === -1)
                nodesData.push({
                    id: link,
                    label: link,
                    group: 1
                })
            edgesData.push({
                target: node.page,
                source: link
            })
        })
        node.css.forEach(css => {
            if (nodesData.findIndex(node => node.id === css) === -1)
                nodesData.push({
                    id: css,
                    label: css,
                    group: 2
                })
            edgesData.push({
                target: node.page,
                source: css
            })
        })
        node.js.forEach(js => {
            if (nodesData.findIndex(node => node.id === js) === -1)
                nodesData.push({
                    id: js,
                    label: js,
                    group: 3
                })
            edgesData.push({
                target: node.page,
                source: js
            })
        })

    })

    return [nodesData, edgesData];
}

/**
 * Build network graph base on server response, using d3
 * @param json: Object
 */
SiteMap.buildGraph = (json) => {

    // Do not show wrapper till button was clicked
    SiteMap.showWrapper();

    // If button was clicked and chart already exist, remove inner html
    document.querySelector('svg').innerHTML = "";

    const [nodesData, edgesData] = SiteMap.buildStructureForD3(json);

    // Working with d3

    var svg = d3.select("svg").call(d3.zoom().on("zoom", function () {
            svg.attr("transform", d3.event.transform)
        })),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody().strength(-1000))
        .force("center", d3.forceCenter(width / 2, height / 2));


    //add encompassing group for the zoom
    var g = svg.append("g")
        .attr("class", "everything");

    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(edgesData)
        .enter().append("line")
        .attr("stroke-width", 1);

    var node = g.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodesData)
        .enter().append("g")

    node.append("circle")
        .attr("r", 5)
        .attr("fill", function (d) {
            return color(d.group);
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("text")
        .text(function (d) {
            return d.id;
        })
        .attr('x', 6)
        .attr('y', 3);

    node.append("title")
        .text(function (d) {
            return d.id;
        });

    simulation
        .nodes(nodesData)
        .on("tick", ticked);

    simulation.force("link")
        .links(edgesData);

    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    //Zoom functions
    function zoom_actions() {
        g.attr("transform", d3.event.transform)
    }

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
    }


    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }


}

const form = document.querySelector('form');
form.addEventListener('submit', SiteMap.onsubmit);
