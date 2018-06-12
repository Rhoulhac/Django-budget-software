var ctx = document.getElementById('myChart').getContext('2d');

// 12 color options - should be enough
var background = [
'rgba(127, 191, 63, 0.2)',
'rgba(255, 99, 132, 0.2)',
'rgba(54, 162, 235, 0.2)',
'rgba(255, 206, 86, 0.2)',
'rgba(140, 114, 127, 0.2)',
'rgba(191, 63, 191, 0.2)',
'rgba(153, 102, 255, 0.2)',
'rgba(75, 192, 192, 0.2)',
'rgba(191, 63, 63, 0.2)',
'rgba(227, 225, 93, 0.2)',
'rgba(63, 191, 191, 0.2)',
'rgba(191, 127, 63, 0.2)',
]
var border = [
'rgba(127, 191, 63, 1)',
'rgba(255,99,132,1)',
'rgba(54, 162, 235, 1)',
'rgba(255, 206, 86, 1)',
'rgba(140, 114, 127, 1)',
'rgba(191, 63, 191, 1)',
'rgba(153, 102, 255, 1)',
'rgba(75, 192, 192, 1)',
'rgba(191, 63, 63, 1)',
'rgba(227, 225, 93, 1)',
'rgba(63, 191, 191, 1)',
'rgba(191, 127, 63, 1)',
]

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