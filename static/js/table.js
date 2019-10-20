$(document).ready(function() {

    $.getJSON("../../output.json", function(data) {
        var arrItems = [];
        $.each(data, function(index, value) {
            arrItems.push(value);
        });

        function append_json(data){
            var table = document.getElementById('gable');
            data.forEach(function(object) {
                var tr = document.createElement('tr');
                tr.innerHTML = '<td>' + object.COUNTRY + '</td>' +
                '<td>' + object.LoC + '</td>' +
                '<td>' + object.BALANCE + '</td>' +
                '<td>' + object.DATE + '</td>';
                table.appendChild(tr);
            });
        }*/