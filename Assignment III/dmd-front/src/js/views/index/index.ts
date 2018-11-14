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
    const username = 'springsergio';

    fetch(`https://142.93.136.40:8000/assigmentIII/query_1/?username=${username}&color=${color}&plate_pattern=${plate_pattern}&date=${date}`).then((response) => {
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
    return false;
}
(window as any).runQuery2 = runQuery2;


export function runQuery3(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery3 = runQuery3;


export function runQuery4(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery4 = runQuery4;


export function runQuery5(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery5 = runQuery5;


export function runQuery6(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery6 = runQuery6;


export function runQuery7(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery7 = runQuery7;


export function runQuery8(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery8 = runQuery8;


export function runQuery9(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery9 = runQuery9;


export function runQuery10(e: Event) {
    e.preventDefault();
    return false;
}
(window as any).runQuery10 = runQuery10;
