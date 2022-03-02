function drawMainPie(namePie, expenses, titlePie) {

    // var colors = ['#A0DE96', '#FF6737', '#00BBBB', '#ED756E', '#B4EDF0', '#4A3870', '#9f'];

    sum_expenses = 0
    expenses.forEach(expense => {
        expense['y'] = Number(expense['y']);
        sum_expenses = sum_expenses + expense['y']
        // console.log(expense);   
    });
    // console.log(expenses);
    Highcharts.chart(namePie, {
        chart: {
            type: 'variablepie',
            // width: 400,
            height: 300,
        },
        title: {
            text: titlePie + ": " + sum_expenses.toLocaleString() + ' руб.',
            style: {
                fontSize: '14px'
            }
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '',
            pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>' +
                'Сумма расходов: <b>{point.y}</b><br/>'
        },
        // colors: colors,
        series: [{
            minPointSize: 0,
            innerSize: '20%',
            zMin: 0,
            name: 'Категории',
            data: expenses
        }],
        navigation: {
            buttonOptions: {
                enabled: false
            }
        }
    });
}