import 'file-loader!./index.html';
import './index.scss';

document.addEventListener("DOMContentLoaded", function () {
});

function prepareResult(result: { [ s: string ]: any }[]) {
    // {
    //     id: 1,
    //     name: 'Item 1',
    //     price: '$1'
    // }, ...

}
function clearResults() {
    $('.bootstrap-table').remove();
    $('.nothing-found').remove();
}

export function runQuery1(e: Event) {
    e.preventDefault();

    const form = $(e.target).closest('form');
    const color = $('#q1-color').val();
    const plate_pattern = $('#q1-plate').val();
    const date = $('#q1-date').val();
    const username = $('#q1-name').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_1/?username=${username}&color=${color}&plate_pattern=${plate_pattern}&date=${date}`).then((response) => {
        response.json().then((result) => {
            $('<table id="result-1"></table>').insertAfter('#query-1 form');
            clearResults();
            // @ts-ignore
            $('#result-1').bootstrapTable({
                columns: [{
                    field: 'Car license plate',
                    title: 'Car license plate'
                }, {
                    field: 'Car type',
                    title: 'Car type'
                }, {
                    field: 'color:',
                    title: 'Color'
                }],
                data: result
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-1 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });


    return false;
}
(window as any).runQuery1 = runQuery1;


export function runQuery2(e: Event) {
    e.preventDefault();
    const date = $('#q2-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_2/?date=${date}`).then((response) => {
        response.json().then((result) => {
            const data = [];
            for (const prop in result) {
                data.push({
                    time: prop,
                    amount: result[prop],
                });
            }
            $('<table id="result-2"></table>').insertAfter('#query-2 form');
            clearResults();
            // @ts-ignore
            $('#result-2').bootstrapTable({
                columns: [{
                    field: 'time',
                    title: 'Time'
                }, {
                    field: 'amount',
                    title: 'Amount'
                }],
                data: data
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-2 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery2 = runQuery2;


export function runQuery3(e: Event) {
    e.preventDefault();
    const start_date = $('#q3-start-date').val();
    const end_date = $('#q3-end-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_3/?start_date=${start_date}&end_date=${end_date}`).then((response) => {
        response.json().then((result) => {
            const data = [];
            for (const prop in result) {
                data.push({
                    time_of_the_day: prop,
                    percentage: result[prop],
                });
            }
            $('<table id="result-3"></table>').insertAfter('#query-3 form');
            clearResults();
            // @ts-ignore
            $('#result-3').bootstrapTable({
                columns: [{
                    field: 'time_of_the_day',
                    title: 'Time of the day'
                }, {
                    field: 'percentage',
                    title: 'Percentage'
                }],
                data: data
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-3 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery3 = runQuery3;


export function runQuery4(e: Event) {
    e.preventDefault();
    const start_date = $('#q4-start-date').val();
    const end_date = $('#q4-end-date').val();
    const username = $('#q4-name').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_4/?username=${username}&start_date=${start_date}&end_date=${end_date}`).then((response) => {
        response.json().then((result) => {
            $('<table id="result-4"></table>').insertAfter('#query-4 form');
            clearResults();
            // @ts-ignore
            $('#result-4').bootstrapTable({
                columns: [{
                    field: 'car_order_id',
                    title: 'car_order_id',
                }, {
                    field: 'cost_of_ride',
                    title: 'cost_of_ride',
                    },{
                    field: 'creating_time',
                    title: 'creating_time',
                    },{
                    field: 'payment_id',
                    title: 'payment_id',
                    },{
                    field: 'username',
                    title: 'username',
                    }],
                data: result
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-4 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery4 = runQuery4;


export function runQuery5(e: Event) {
    e.preventDefault();
    const date = $('#q5-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_5/?date=${date}`).then((response) => {
        response.json().then((result) => {

            $('<table id="result-5"></table>').insertAfter('#query-5 form');
            clearResults();
            // @ts-ignore
            $('#result-5').bootstrapTable({
                columns: [{
                    field: 'Average distance',
                    title: 'Average Distance',
                },{
                    field: 'Average duration',
                    title: 'Average Duration',
                }],
                data: [result]
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-5 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery5 = runQuery5;


export function runQuery6(e: Event) {
    e.preventDefault();
    fetch(`http://142.93.136.40:8000/assigmentIII/query_6/`).then((response) => {
        response.json().then((result) => {
            const data = [];
            for (const prop in result) {
                for (const el of result[prop]) {
                    data.push({
                        ...el,
                        time_of_the_day: prop,
                    });
                }
            }
            $('<table id="result-6"></table>').insertAfter('#query-6 form');
            clearResults();
            // @ts-ignore
            $('#result-6').bootstrapTable({
                columns: [{
                    field: 'time_of_the_day',
                    title: 'Time of the day'
                }, {
                    field: 'City:',
                    title: 'City',
                },{
                    field: 'Counter:',
                    title: 'Counter',
                },{
                    field: 'Street',
                    title: 'Street',
                },{
                    field: 'ZIP-Code',
                    title: 'ZIP-Code',
                }],
                data,
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-6 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery6 = runQuery6;


export function runQuery7(e: Event) {
    e.preventDefault();

    const date = $('#q7-percent').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_7/?date=${date}`).then((response) => {
        response.json().then((result) => {

            $('<table id="result-7"></table>').insertAfter('#query-7 form');
            clearResults();
            // @ts-ignore
            $('#result-7').bootstrapTable({
                columns: [{
                    field: 'Car license plate',
                    title: 'Car license plate',
                },{
                    field: 'Car type:',
                    title: 'Car type',
                },{
                    field: 'Order counter',
                    title: 'Order counter',
                }],
                data: result
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-7 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });

    return false;
}
(window as any).runQuery7 = runQuery7;


export function runQuery8(e: Event) {
    e.preventDefault();
    const start_date = $('#q8-start-date').val();
    const end_date = $('#q8-end-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_8/?start_date=${start_date}&end_date=${end_date}`).then((response) => {
        response.json().then((result) => {
            const data = [];
            for (const prop in result) {
                data.push({
                    username: prop,
                    amount: result[prop],
                });
            }
            $('<table id="result-8"></table>').insertAfter('#query-8 form');
            clearResults();
            // @ts-ignore
            $('#result-8').bootstrapTable({
                columns: [{
                    field: 'username',
                    title: 'Username'
                }, {
                    field: 'amount',
                    title: 'Amount of charging stations'
                }],
                data: data
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-8 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery8 = runQuery8;


export function runQuery9(e: Event) {
    e.preventDefault();
    const start_date = $('#q9-start-date').val();
    const end_date = $('#q9-end-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_9/?start_date=${start_date}&end_date=${end_date}`).then((response) => {
        response.json().then((result) => {
            $('<table id="result-9"></table>').insertAfter('#query-9 form');
            clearResults();
            // @ts-ignore
            $('#result-9').bootstrapTable({
                columns: [{
                    field: 'Workshop_id',
                    title: 'Workshop id'
                }, {
                    field: 'Part_name',
                    title: 'Part name'
                }, {
                    field: 'Average_per_week',
                    title: 'Average per week'
                }],
                data: result
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-9 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });
    return false;
}
(window as any).runQuery9 = runQuery9;


export function runQuery10(e: Event) {
    e.preventDefault();

    const start_date = $('#q10-start-date').val();
    const end_date = $('#q10-end-date').val();

    fetch(`http://142.93.136.40:8000/assigmentIII/query_10/?start_date=${start_date}&end_date=${end_date}`).then((response) => {
        response.json().then((result) => {
            $('<table id="result-10"></table>').insertAfter('#query-10 form');
            clearResults();
            // @ts-ignore
            $('#result-10').bootstrapTable({
                columns: [{
                    field: 'Car type',
                    title: 'Car type'
                }, {
                    field: 'Cost_per_week',
                    title: 'Cost per week'
                }],
                data: result
            });

        }).catch(() => {
            clearResults();
            $('<div class="nothing-found">Nothing found</div>').insertAfter('#query-10 form');
        });
    }).catch(() => {
        alert('Could not connect to server');
    });

    return false;
}
(window as any).runQuery10 = runQuery10;
