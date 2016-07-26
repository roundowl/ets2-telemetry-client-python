function displayAccounts() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      var jsonResponse = JSON.parse(xhttp.response);
      var accountTable;
      accountTable = '<table style="border-collapse: collapse; width:100%;"><style scoped>tr:nth-child(4n) {background-color: #ddd}</style><tr><th>Vehicle</th><th>Start</th><th>Stop</th><th>Odometer</th>';
      accountTable +='<th>Distance<br>(km)</th><th>Total fuel<br>consumption<br>(litres)</th>';
      accountTable +='<th>Average fuel<br>consumption<br>(l/100 km)</th><th>Average speed<br>(km/h)</th>';
      accountTable +='<th>Rating</th></tr>';
      for (var key in jsonResponse) {
        accountTable += '<tr onclick="displayData(\'' + jsonResponse[key]['id'] + '\')">';
        accountTable += '<td>' + jsonResponse[key]['id'] + '</td>';
        accountTable += '<td>' + jsonResponse[key]['start'] + '</td>';
        accountTable += '<td>' + jsonResponse[key]['stop'] + '</td>';
        accountTable += '<td align="center">' + Math.round(jsonResponse[key]['odometer']) + '</td>';
        accountTable += '<td align="center">' + Math.round(jsonResponse[key]['distance']) + '</td>';
        accountTable += '<td align="center">' + Math.round(jsonResponse[key]['totalFuel']) + '</td>';
        accountTable += '<td align="center">' + Math.round(jsonResponse[key]['averageFuel']*10)/10 + '</td>';
        accountTable += '<td align="center">' + Math.round(jsonResponse[key]['averageSpeed']*10)/10 + '</td>';
        accountTable += '<td align="center">' + jsonResponse[key]['rating'] + '</td></tr>';
        accountTable += '<tr><td style="display:none" colspan="9" id="' + jsonResponse[key]['id'] + '"></td></tr>';
      };
      accountTable += '</table>';
      document.getElementById('truckList').innerHTML = accountTable;
    }
  };
  xhttp.open("GET", './accountList.json', true);
  xhttp.send();
}

function displayData(id) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      var jsonResponse = JSON.parse(xhttp.response);
      var dataElement = document.getElementById(id);
      if (dataElement.style.display == "none") {
        var dataTable = "<table style='width:100%;'><style scoped>tr {background-color:#eee}</style><tr><td>"
        dataTable += "<table><tr><td style='text-align:right;'><b>Transport work, average (tonne-km/l)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.averageTransportWork*10)/10 + "</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Average fuel consumption (l/100km)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.averageFuelConsumption*10)/10 + "</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Idling (% of engine running time)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.idling*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Engine overspeed (% of engine running time)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.engineOverspeed*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Speeding (% of engine running time)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.speeding*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Driving outside optimum engine speed band<br>(% of engine running time)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.outsideEngineSpeed*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Brake applications (#/100 km)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.brakeAppsPer100km*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Harsh brake applications (#/100 km)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.harshBrakeAppsPer100km*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Harsh accelerations (#/100 km)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.harshAccelPer100km*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Coasting (% of distance)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.coasting*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Driving with vehicle warning (% of distance)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.drivingWithWarning*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:right'><b>Driver support (Average score in %)</b></td><td style='text-align:left'>"+Math.round(jsonResponse.averageDriverScore*10)/10+"</td></tr></table>";
        dataTable += "</td><td>"
        dataTable += "<table style='border-left: 1px solid black;'><style scoped>tr:nth-child(2n) {background-color:#ddd} tr {width:100%}</style><tr><td style='text-align:left'>"
        dataTable += "Engine running time</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.engineRunningTime)+":"+Math.round((jsonResponse.engineRunningTime%1)*60)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Engine running time, idling</td><td style='text-align:left; width:20%'>"
        dataTable += Math.round(jsonResponse.engineIdlingTime)+":"+Math.round((jsonResponse.engineIdlingTime%1)*60)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Total fuel consumption</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.fuelUsed)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Fuel consumption per hour</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.fuelUsedPerHour*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Distance with trailer</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.distanceWithTrailer)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Average weight</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.averageWeight*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Transport work</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.transportWork)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Maximum vehicle speed</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.maxVehicleSpeed*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Maximum engine speed</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.maxEngineSpeed*10)/10+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Distance with cruise control</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.distanceWithCC)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Coasting distance</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.coastingDistance)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Brake applications</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.brakeApps)+"</td></tr>";
        dataTable += "<tr><td style='text-align:left'>Harsh brake applications</td><td style='text-align:left; width:20%'>"+Math.round(jsonResponse.harshBrakeApps)+"</td></tr></table>";
        dataTable += "</td></tr></table>"

        dataElement.innerHTML=dataTable;
        dataElement.style.display = "table-cell";
      } else {
        dataElement.style.display = "none";
      };
    }
  };
  xhttp.open("GET", './' + id + '.json', true);
  xhttp.send();
}

function downloadJSON(link) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
        var jsonResponse = JSON.parse(xhttp.response);
        return jsonResponse;
    }
  };
  xhttp.open("GET", link, true);
  xhttp.send();
} 