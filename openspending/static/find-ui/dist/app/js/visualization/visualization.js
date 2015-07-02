(function() {

    /**
     * Start the Wiard mode
     **/
    window.clickedIndicator = false;
    window.expandedCategory = false;

    var mapCreated = false;
    window.map;
    window.geoJsonLayers = {};

    window.modalTitle = "";
    window.modalMessage = "";

    $('#modal').modal({
        show: false,
        keyboard: false
    }); // initialized with defaults


    $('#modal').on('show.bs.modal', function(event) {
        var modal = $(this)
        modal.find('.modal-title').text(window.modalTitle);
        modal.find('.modal-body').text(window.modalMessage);
    });

    $(function() {
        // $('#vizTabs a:first').tab('show')
    });

    var geoJSONHandler = function(response, type) {

        function onEachFeature(feature, layer) {

            if (feature.properties) {
                layer.bindPopup(feature.properties.sovereignt);
            }
        }

        window.countriesJson = response;

        if (!geoJsonLayers[type]) {
            //debugger;
            geoJsonLayers[type] = L.geoJson(response, {
                style: {
                    weight: 2,
                    opacity: 1,
                    color: 'white',
                    dashArray: '3',
                    fillOpacity: 0.5,
                    fillColor: '#FF0000'
                },
                onEachFeature: onEachFeature
            });

        }



        for (var _type in geoJsonLayers) {
            if (type == _type) {
                map.addLayer(geoJsonLayers[_type]);
            } else {
                map.removeLayer(geoJsonLayers[_type]);
            }
        }


        //geoJsonLayers[type].addTo(map);
        //debugger;
        // geoJsonLayer = L.geoJson(this.collection.toJSON(), {
        //     onEachFeature: _self.onEachFeature
        // });

    }

    window.changeGroup = function(groupId) {
        if (groupId == "all") {
            groupId = "sovereignt";
        }
        window.loadGeoJSON(groupId, geoJSONHandler);
    }

    window.createMap = function() {

        var defaultType = "sovereignt";

        if (!mapCreated) {
            mapCreated = true;
            map = L.map('map').setView([0, 0], 1);
            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                id: 'examples.map-i875mjb7',
                accessToken: 'pk.eyJ1Ijoid2lzZWd1eSIsImEiOiI5N2IxYWYxMzU2YmZhOTU3ZjM4ZDRjZDBlMzNkYzU0NSJ9._T6Dz2ZFA4p9VZMdT2SmjA'
            }).addTo(map);

            //load geojson
            window.loadGeoJSON(defaultType, geoJSONHandler);
        }

    }


    var eventBind = function() {

        $(".list-group-item").popover({
            trigger: "hover"
        });

        //var val = $('#filter-years').slider("option", "value");
        flipCardEvent();

        // $('.dropdown-toggle').dropdown();


    }







    //KNOCKOUT MODEL

    var model = window.vizModel;



    var countriesListLoadHandler = function(response) {

        window.bindCountries(response, model);
    }



    var indicatorListLoadHandler = function(response) {

        window.bindIndicators(response, model);


        //enable knockout
        ko.applyBindings(model);

        eventBind();

    }

    window.loadIndicatorList(window.config.server + window.config.services.categories, indicatorListLoadHandler);
    window.loadCountries("", countriesListLoadHandler);

    // Under Five mortality rate

    // GDP, per capita

    // Poverty headcount ratio at $1.25 a day (PPP)

    // Literacy rate

    // Control of corruption

    var indicatorDataLoadHandler = function(response) {



        var highChartsJson = window.prepareHighchartsJson(response, model.activeChart(), model.activeIndicators(), model.activeGroup(), model.activeRegion());

        model.activeData(highChartsJson);

        var highChartsJson = model.activeData();
        highChartsJson.title.text = model.activeIndicator();
        highChartsJson.chart.type = model.activeChart();
        highChartsJson.yAxis.title.text = "";
        //highChartsJson.subtitle.text = type;
        $('#viz-container').highcharts(model.activeData());
        $("#loading").hide();


        // $('#viz-container').highcharts(highChartsJson, model.activeIndicator(), model.activeChart());

    }





    //startUI(); //this should be the last function in this function


}())