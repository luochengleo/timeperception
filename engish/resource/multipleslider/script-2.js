$(function() {

  // function to create slider ticks
  var setSliderTicks = function() {

  };

  // create slider
  $('#slider').slider({
    // set min and maximum values
    // day hours in this example
    min: 0,
    max: 1000,
    // step
    // quarter of an hour in this example
    step: 1,
    // range
    // show tooltips
    tooltips: false,
    // current data
    handles: [{
      value: 250,
      type: "wake"
    }, {
      value: 500,
      type: "leave"
    }, {
      value: 750,
      type: "return"
    }],
    // display type names
    showTypeNames: true,
    typeNames: {
      'wake': 'Wake Up',
      'leave': 'Leave',
      'return': 'Return',
    },
    ticks: {
                // use default values
                // main tick is 1
                tickMain : 1,
                // side tick is 0.5
                tickSide : 0.5,
                // show main label
                tickShowLabelMain : false,
                // don't show side label
                tickShowLabelSide : false,
            },
    // main css class (of unset data)
    mainClass: 'wake',
    // time
    type: 'time',
    // slide callback
    slide: function(e, ui) {
      console.log(e, ui);
    },
    // handle clicked callback
    handleActivated: function(event, handle) {
      // get select element
      var select = $(this).parent().find('.slider-controller select');
      // set selected option
      select.val(handle.type);
    }

  });

  // button for adding new ranges
  $('.slider-controller button.add').click(function(e) {
      e.preventDefault();
      // get slider
      var $slider = $('#slider');
      // trigger addHandle event
      $slider.slider('addHandle', {
        value: 12,
        type: $('.slider-controller select').val()
      });
      return false;
    });

  // button for removing currently selected handle
  $('.slider-controller button.remove').click(function(e) {
      e.preventDefault();
      // get slider
      var $slider = $('#slider');
      // trigger removeHandle event on active handle
      $slider.slider('removeHandle', $slider.find('a.ui-state-active').attr('data-id'));

      return false;
    });

  // when clicking on handler
  $(document).on('click', '.slider a', function() {
    var select = $('.slider-controller select');
    // enable if disabled
    //select.attr('disabled', false);
    alert($(this).attr('data-type'));
    select.val($(this).attr('data-type'));
    /*if ($(this).parent().find('a.ui-state-active').length)
      $(this).toggleClass('ui-state-active');*/
  });
});