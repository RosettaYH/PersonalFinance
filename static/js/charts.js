// Function to initialize Pie Chart
function initPieChart(chartId, dataLabels, dataValues) {
  var ctx = document.getElementById(chartId).getContext("2d");
  return new Chart(ctx, {
    type: "pie",
    data: {
      labels: dataLabels,
      datasets: [
        {
          data: dataValues
          // backgroundColor: [...], // Add different colors for each category
        }
      ]
    }
  });
}

// Function to initialize Line Chart
function initLineChart(chartId, dataLabels, dataExpenses, dataIncome) {
  var ctx = document.getElementById(chartId).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: dataLabels,
      datasets: [
        {
          label: "Expenses",
          data: dataExpenses,
          borderColor: "red",
          fill: false
        },
        {
          label: "Income",
          data: dataIncome,
          borderColor: "green",
          fill: false
        }
      ]
    }
  });
}

// Replace [...] with your actual data or logic to fetch data
