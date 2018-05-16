

function buildPie(sample) {
    var url = "/samples/" + sample;

    Plotly.d3.json(url, function(error, response) {
        if (error) throw error;

        console.log(response);

        var vals = response.sample_values;
        var labs = response.otu_ids;

        if ((vals.length > 10) & (labs.length > 10)) {
            vals = vals.slice(0,10);
            labs = labs.slice(0,10);
        };

        var trace1 = {
            values: vals,
            labels: labs,
            type: "pie",
        };

        var data = [trace1];

        var layout = {
            title: "Microbe Makeup for " + sample
        };

        // attempted to add event listener to restyle plot, ran out of time

        // Plotly.restyle("plot", data, layout);

        // document.getElementById("sel1").addEventListener("click", function() {
        //     var sample = this.value;
        //     buildPie(sample);
        // });
        Plotly.newPlot("plot", data, layout);

    });
}

var sample = "bb_940";
buildPie(sample);


function fillDrop(){
    var select = document.getElementById("sel1");
    var url = "/names"
    Plotly.d3.json(url, function(error, response) {
        for(var i = 0; i < response.length; i++) {
            var opt = response[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
        };
    });
}

fillDrop();
