
    var data_array=[];
 $( function() {



    //$("#exampleModal").on("show.bs.modal",function(exb){
     // alert("event registered");
    $( "#id_receiver" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
            getDataFromServer(request,response);
        },
        focus: function(event, ui) {

          return false;
        },
        select: function( event, ui ) {
          tagExist = function(c) {
            var e = $("#receiver_id").val().indexOf(c);
            return ( e>= 0);
          }

        if (!tagExist(ui.item.id)) {
          //alert(ui.item.id);
          add_tag(ui.item.label,ui.item.id);
          if ($("#receiver_id").val() != '') {
            $("#receiver_id").val($("#receiver_id").val() + ',' + ui.item.id);
          } else {
            $("#receiver_id").val(ui.item.id);
          }

        } else {

          //alert($("#receiver_id").val());
        }
        $("#id_receiver").val("");
        return false;
        }
      });
      //});
  } );
function getDataFromServer(request,response){

 // alert("data requested");
  $.getJSON( "/message/receive/", {
            term: request.term ,
          }, function(data){
              data_array=data;
              response(data_array);
          });
  //alert("data received");
}
function searchArray(nameKey, myArray) {
  for (var i = 0; i < myArray.length; i++) {
    if (myArray[i].label === nameKey) {
      return myArray[i].value;
    }
  }
  return "";
}

function add_tag( label,  id){
  var s = "<div class=\"tag\"><span class=\"label\">"+label+"</span><div class=\"tag_close\" data-id=\""+id+"\">x</div></div>";
  $("#tag_holder").append(s);
  if($(".tag").length >= 1){
    $(".tag_close").on("click",function(){
        var id = $(this).data("id");
        remove_tag(id);
        $(this).parent().fadeOut(100,function(){$(this.remove())});
    });

  }

}
function remove_tag(id){
  var e = $('#receiver_id').val().split(',');
  var index = e.indexOf(id.toString());
  if (index > -1) {
    e.splice(index, 1);
  }
  $('#receiver_id').val(e.join(','));

}
