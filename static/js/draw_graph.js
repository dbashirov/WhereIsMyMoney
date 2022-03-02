function drawMainGraph(startDate, income_list, expense_list, balance_list) {

    // Руссифицурем
    // var colors = ['#33CC33', '#FF3333', '#3333CC', '#E80C7A', '#E80C7A'];
    var colors = ['#33CC33', '#FF6737', '#00BBBB', '#FF3333', '#3333CC', '#E80C7A', '#E80C7A'];
    translateGraph(Highcharts);
    
    // Рисуем диаграмму
    Highcharts.chart('overall_balance', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Динамика за 3 месяца, остаток: ' + balance_list[balance_list.length - 1].toLocaleString() + ' руб.'
        },
        xAxis: {
            type: 'datetime',
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' рублей'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            spline: {
                lineWidth: 3,
                states: {
                    hover: {
                        lineWidth: 4
                    }
                },
                marker: {
                    enabled: false
                },
                pointInterval: 24 * 3600000, // one day
                pointStart: startDate
            }
        },
        colors: colors,
        series: [{
            name: 'Доходы',
            data: income_list
        },
        {
            name: 'Расходы',
            data: expense_list

        },
        {
            name: 'Остаток',
            data: balance_list
        }
        ],
        navigation: {
            buttonOptions: {
                enabled: false
            }
        }
    });
}

function drawGraphWallet(list_wallets, startDate) {
    list_wallets.forEach(wallet => {

        balance_list = wallet.balance_list.map(Number);

        // Руссифицурем
        // var colors = ['#33CC33', '#FF3333', '#3333CC', '#E80C7A', '#E80C7A'];
        var colors = ['#33CC33', '#FF6737', '#00BBBB', '#FF3333', '#3333CC', '#E80C7A', '#E80C7A'];
        translateGraph(Highcharts);

        // Рисуем диаграмму
        Highcharts.chart('wallet_container' + wallet.id, {
            chart: {
                type: 'spline',
                height: 250,
            },
            title: {
                text: wallet.title + ', остаток: ' + balance_list[balance_list.length - 1].toLocaleString() + ' руб.',
                style: {
                    fontSize: '16px'
                }
            },
            xAxis: {
                type: 'datetime',
            },
            yAxis: {
                title: {
                    text: ''
                },
            },
            tooltip: {
                shared: true,
                valueSuffix: ' рублей'
            },
            credits: {
                enabled: false
            },
            plotOptions: {
                spline: {
                    lineWidth: 2,
                    states: {
                        hover: {
                            lineWidth: 3
                        }
                    },
                    marker: {
                        enabled: false
                    },
                    pointInterval: 24 * 3600000, // one day
                    pointStart: startDate
                }
            },
            colors: colors,
            series: [
            // {
            //     name: 'Доходы',
            //     showInLegend: false,
            //     data: wallet.income_list.map(Number)
            // },
            // {
            //     name: 'Расходы',
            //     showInLegend: false,
            //     data: wallet.expense_list.map(Number)

            // },
            {
                name: 'Остаток',
                showInLegend: false,
                data: balance_list
            }
            ],
            navigation: {
                buttonOptions: {
                    enabled: false
                }
            }
        });

    });
}

function translateGraph(Highcharts) {
    Highcharts.setOptions({
        lang: {
            loading: 'Загрузка...',
            months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            weekdays: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
            shortMonths: ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сент', 'Окт', 'Нояб', 'Дек'],
            exportButtonTitle: "Экспорт",
            printButtonTitle: "Печать",
            rangeSelectorFrom: "С",
            rangeSelectorTo: "По",
            rangeSelectorZoom: "Период",
            downloadPNG: 'Скачать PNG',
            downloadJPEG: 'Скачать JPEG',
            downloadPDF: 'Скачать PDF',
            downloadSVG: 'Скачать SVG',
            printChart: 'Напечатать график'
        }
    });   
}