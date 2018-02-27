$(document).ready(function() {
    var table = $('#database').DataTable( {
        "ajax": '/database',
        "paging": false,
        "searching": false,
        "info": false,
        "order": [[1, "desc"]],
        "columnDefs": [{
            "targets": -1,
            "data": null,
            "defaultContent": "<button class='btn btn-sm btn-outline-secondary'>Revome</button>"
        }]
    } );



     $('#database tbody').on( 'click', 'button', function () {
        var data = table.row($(this).parents('tr')).data();
        console.log(data);
        $.ajax({
            url: "/delete/"+data[0],
            type: "POST",
            success: function(){}
            });
        table.row($(this).parents('tr')).remove().draw(false);
    } );

    setInterval(function() {
        table.ajax.reload();
    }, 10000 );
} );
