document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("#chart") != undefined) {
    google.charts.load("current", { packages: ["corechart", "bar"] });
    google.charts.setOnLoadCallback(drawBasic);

    function drawBasic() {
      fetch("/chart")
        .then((response) => response.json())
        .then((data) => {
          var chartData = [];

          data.chartData.forEach((item) => {
            chartData.push([item.Subject, item.Score, item.Score]);
          });

          var data = new google.visualization.DataTable();
          data.addColumn("string", "Subject");
          data.addColumn("number", "Score");
          data.addColumn({ type: "number", role: "annotation" });
          data.addRows(chartData);

          var options = {
            title: "Average Score Per Level by Categories",
            titleTextStyle: {
              color: "#FFF",
            },
            chartArea: { width: "60%", height: "90%" },
            backgroundColor: "none",
            hAxis: {
              textStyle: { color: "#FFF" },
              viewWindow: {
                min: 0,
              },
            },
            vAxis: {
              textStyle: { color: "#FFF" },
            },
            legend: { position: "none" },
          };

          var chart = new google.visualization.BarChart(
            document.getElementById("chart")
          );

          chart.draw(data, options);
        });
    }
  }
});
