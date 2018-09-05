
$(document).ready(function(){
    $('#pros-select,#sems-select').on('change', function(){
        pro= $('#pros-select').val();
        sem= $('#sems-select').val();
        updateCourseList(pro,sem);
    });
  })

  function updateCourseList(pro,sem){
    $('#pros-select,#sems-select').attr("disabled","disabled").css("pointer","progress");
    $('.course-row').each(function(){
            myprog = $(this).data("program");
            mysem = $(this).data("sem");

            if(pro =="AllP" && sem == "AllS")
                $(this).show();
            else if(sem=="AllS" && (myprog.indexOf(pro)>=0))
                $(this).show();
            else if(pro=="AllP" && sem==mysem)
                $(this).show();
            else if(sem==mysem && (myprog.indexOf(pro)>=0)){
                $(this).show();
            }
            else $(this).fadeOut(200);

        });
    $('#pros-select,#sems-select').removeAttr("disabled").css("pointer","default");
  }
