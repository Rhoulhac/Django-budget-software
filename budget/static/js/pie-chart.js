var ctx = document.getElementById('myChart').getContext('2d');

var labels = []
var data = []
var backgroundColor = []
var borderColor = []
var item = 0

if (category) {
    var text = category + ' Spending'
    for (var key in filterGraphSet) {
        // Find a way to combine amounts from the same store
        labels.push(key);
        data.push(filterGraphSet[key]);
        backgroundColor.push(background[item]);
        borderColor.push(border[item]);
        item++
    }
} else {
    var text = 'Category Spending'
    for (var key in categories) {
        labels.push(key);
        data.push(categories[key]);
        backgroundColor.push(background[item]);
        borderColor.push(border[item]);
        item++
    }
}

var myChart = new Chart(ctx, {
    // The type of chart
    type: 'doughnut',

    // The data for categories
    data: {
        labels: labels,
        datasets: [{
            data: data,
            label: text,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            borderWidth: 1,
        }]
    },

    // Configuration options go here
    options: {
        cutoutPercentage: 35,
        title: {
            display: true,
            text: text,
            position: 'bottom',
            fontSize: 20
        },
        legend: {
            labels: {
                fontSize: 16
            }
        }
    }
});